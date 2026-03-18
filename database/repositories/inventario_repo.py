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

    def add_item(self, tipo: str, catalogo_id: int) -> int:
        #Añade un ítem al inventario. Devuelve el id asignado al nuevo ítem, para poder usarlo en el inventario.
        conn = get_connection()
        try:
            cursor = conn.execute(
                "INSERT INTO inventario_jugador (tipo, catalogo_id) VALUES (?, ?)",
                (tipo, catalogo_id)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def existe_en_inventario(self, tipo: str, catalogo_id: int) -> bool:
        #Devuelve True si el jugador ya tiene ese ítem del catálogo.
        #Útil para saber si el jugador tiene duplicados.
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT id FROM inventario_jugador WHERE tipo = ? AND catalogo_id = ?",
                (tipo, catalogo_id)
            ).fetchone()
            return row is not None
        finally:
            conn.close()