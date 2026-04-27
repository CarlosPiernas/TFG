import sqlite3
from database.db_manager import get_connection


class InventarioRepo:

    def get_inventario(self) -> list[dict]:
        #Devuelve todos los ítems del inventario del jugador.
        #Cada dict tiene: id, tipo, catalogo_id
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM inventario_jugador"
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_inventario_by_tipo(self, tipo: str) -> list[dict]:
        #Devuelve los ítems del inventario filtrados por tipo.
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM inventario_jugador WHERE tipo = ?", (tipo,)
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def agregar_item(self, jugador_id: int, catalogo_id: int, tipo: str) -> bool:
        #Añade un ítem al inventario si el jugador no lo tiene ya.
        #Devuelve True si es nuevo, False si es duplicado.
        #gacha.py usa este retorno para saber si generar fragmento.
        conn = get_connection()
        try:
            #Primero comprobamos si ya existe
            row = conn.execute(
                "SELECT id FROM inventario_jugador WHERE tipo = ? AND catalogo_id = ?",
                (tipo, catalogo_id)
            ).fetchone()
            if row is not None:
                #Duplicado — no insertamos nada
                return False
            #Es nuevo — lo insertamos
            conn.execute(
                "INSERT INTO inventario_jugador (tipo, catalogo_id) VALUES (?, ?)",
                (tipo, catalogo_id)
            )
            conn.commit()
            return True
        finally:
            conn.close()

    def existe_en_inventario(self, tipo: str, catalogo_id: int) -> bool:
        #Devuelve True si el jugador ya tiene ese ítem del catálogo.
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT id FROM inventario_jugador WHERE tipo = ? AND catalogo_id = ?",
                (tipo, catalogo_id)
            ).fetchone()
            return row is not None
        finally:
            conn.close()
    def eliminar_item(self, inv_id: int) -> bool:
        # Elimina un ítem del inventario por su id de inventario.
        # También borra cualquier equipamiento activo que lo referencie.
        # Devuelve True si se eliminó, False si no existía.
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT id FROM inventario_jugador WHERE id = ?", (inv_id,)
            ).fetchone()
            if row is None:
                return False
            # Primero limpiar equipamiento_activo para no violar la FK
            conn.execute(
                "DELETE FROM equipamiento_activo WHERE item_inv_id = ?", (inv_id,)
            )
            conn.execute(
                "DELETE FROM inventario_jugador WHERE id = ?", (inv_id,)
            )
            conn.commit()
            return True
        finally:
            conn.close()