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
        #Equipa un ítem en un slot de un personaje.
        #Si ya había algo en ese slot lo reemplaza automáticamente.
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