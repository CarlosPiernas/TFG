import sqlite3
from database.db_manager import get_connection


class PityRepo:

    def get_pity(self, banner: str) -> int:
        #Devuelve el contador de pity actual de un banner.
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT contador FROM contadores_pity WHERE banner = ?", (banner,)
            ).fetchone()
            return row["contador"] if row else 0
        finally:
            conn.close()

    def set_pity(self, banner: str, valor: int):
        #Guarda el contador de pity de un banner.
        conn = get_connection()
        try:
            conn.execute(
                "INSERT OR REPLACE INTO contadores_pity (banner, contador) VALUES (?, ?)",
                (banner, valor)
            )
            conn.commit()
        finally:
            conn.close()

    def reset_pity(self, banner: str):
        #Resetea el contador de pity de un banner a 0.
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE contadores_pity SET contador = 0 WHERE banner = ?", (banner,)
            )
            conn.commit()
        finally:
            conn.close()