import sqlite3
from database.db_manager import get_connection


class EquipamientoRepo:

    def get_equipo_de_personaje(self, personaje_inv_id: int) -> list[dict]:
        #Devuelve los ítems equipados en un personaje.
        #Cada dict tiene: personaje_inv_id, slot, item_inv_id
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM equipamiento_activo WHERE personaje_inv_id = ?",
                (personaje_inv_id,)
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def equipar(self, personaje_inv_id: int, slot: str, item_inv_id: int):
        # Si es slot de arma, valida restricción S antes de equipar
        if slot == "arma":
            arma_row = get_connection().execute(
                "SELECT catalogo_id FROM inventario_jugador WHERE id = ?",
                (item_inv_id,)
            ).fetchone()
            if arma_row and not self.validar_arma_s(personaje_inv_id, arma_row["catalogo_id"]):
                raise ValueError("Este arma S no puede equiparla este personaje.")
        conn = get_connection()
        try:
            conn.execute("""
                INSERT OR REPLACE INTO equipamiento_activo
                    (personaje_inv_id, slot, item_inv_id)
                VALUES (?, ?, ?)
            """, (personaje_inv_id, slot, item_inv_id))
            conn.commit()
        finally:
            conn.close()

    def desequipar(self, personaje_inv_id: int, slot: str):
        #Elimina el ítem equipado en un slot de un personaje.
        conn = get_connection()
        try:
            conn.execute("""
                DELETE FROM equipamiento_activo
                WHERE personaje_inv_id = ? AND slot = ?
            """, (personaje_inv_id, slot))
            conn.commit()
        finally:
            conn.close()

    def desequipar_todo(self, personaje_inv_id: int):
        #Elimina todo lo equipado.
        conn = get_connection()
        try:
            conn.execute(
                "DELETE FROM equipamiento_activo WHERE personaje_inv_id = ?",
                (personaje_inv_id,)
            )
            conn.commit()
        finally:
            conn.close()
    
    def validar_arma_s(self, personaje_inv_id: int, arma_catalogo_id: int) -> bool:
        # Comprueba que un arma S puede ser equipada por el personaje.
        # Si el arma no es S o no tiene restricción devuelve True directamente.
        # Si tiene personaje_s_id, comprueba que coincide con el personaje.
        conn = get_connection()
        try:
            # Obtenemos la rareza y la restricción del arma
            arma = conn.execute(
                "SELECT rareza, personaje_s_id FROM armas_catalogo WHERE id = ?",
                (arma_catalogo_id,)
            ).fetchone()
            if arma is None:
                return False
            # Si no es S no hay restricción
            if arma["rareza"] != "S":
                return True
            # Si es S pero no tiene personaje asignado la puede equipar cualquiera
            if arma["personaje_s_id"] is None:
                return True
            # Obtenemos el catalogo_id del personaje desde su id de inventario
            personaje = conn.execute(
                "SELECT catalogo_id FROM inventario_jugador WHERE id = ?",
                (personaje_inv_id,)
            ).fetchone()
            if personaje is None:
                return False
            return personaje["catalogo_id"] == arma["personaje_s_id"]
        finally:
            conn.close()