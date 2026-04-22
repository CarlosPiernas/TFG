import sqlite3
from database.db_manager import get_connection


class ArmaRepo:

    def get_catalogo(self) -> list[dict]:
        #Devuelve todas las armas del catálogo.
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM armas_catalogo").fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_by_id(self, arma_id: int) -> dict | None:
        #Devuelve un arma del catálogo por su id. Devuelve None si no existe.
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT * FROM armas_catalogo WHERE id = ?", (arma_id,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def get_by_rareza(self, rareza: str) -> list[dict]:
        #Devuelve todas las armas de una rareza.
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM armas_catalogo WHERE rareza = ?", (rareza,)
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_arma_de_personaje_s(self, personaje_id: int) -> dict | None:
        #Devuelve el arma S vinculada a un personaje S. Devuelve None si no tiene.
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT * FROM armas_catalogo WHERE personaje_s_id = ?", (personaje_id,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()