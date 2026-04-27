import sqlite3
from database.db_manager import get_connection


class RunaRepo:

    def get_catalogo(self) -> list[dict]:
        #Devuelve todas las runas del catálogo.
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM runas_catalogo").fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_by_id(self, runa_id: int) -> dict | None:
        #Devuelve una runa del catálogo por su id. Devuelve None si no existe.
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT * FROM runas_catalogo WHERE id = ?", (runa_id,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def get_by_rareza(self, rareza: str) -> list[dict]:
        #Devuelve todas las runas de una rareza.
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM runas_catalogo WHERE rareza = ?", (rareza,)
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()
            
    def get_by_nombre(self, nombre: str) -> dict | None:
        # Busca una runa en el catálogo por nombre exacto
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT * FROM runas_catalogo WHERE nombre = ?", (nombre,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()
