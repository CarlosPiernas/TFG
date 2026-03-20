import sqlite3
from database.db_manager import get_connection


class PityRepo:

    def get_pity(self, jugador_id: int, banner: str) -> dict | None:
        #Devuelve el pity actual de un banner como dict con "pity_count".
        #Devuelve None si el jugador nunca ha tirado en ese banner.
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT contador FROM contadores_pity WHERE jugador_id = ? AND banner = ?",
                (jugador_id, banner)
            ).fetchone()
            if row is None:
                return None
            return {"pity_count": row["contador"]}
        finally:
            conn.close()

    def actualizar_pity(self, jugador_id: int, banner: str, valor: int):
        #Guarda el contador de pity de un banner.
        #Si no existe la fila la crea, si existe la sobreescribe.
        conn = get_connection()
        try:
            conn.execute(
                """INSERT INTO contadores_pity (jugador_id, banner, contador)
                   VALUES (?, ?, ?)
                   ON CONFLICT(jugador_id, banner)
                   DO UPDATE SET contador = excluded.contador""",
                (jugador_id, banner, valor)
            )
            conn.commit()
        finally:
            conn.close()

    def reset_pity(self, jugador_id: int, banner: str):
        #Resetea el contador de pity de un banner a 0.
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE contadores_pity SET contador = 0 WHERE jugador_id = ? AND banner = ?",
                (jugador_id, banner)
            )
            conn.commit()
        finally:
            conn.close()