import sqlite3
from database.db_manager import get_connection


class RecursosRepo:

    def get_recursos(self) -> dict | None:
        #Devuelve los recursos actuales del jugador como diccionario.
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT * FROM recursos_jugador WHERE id = 1"
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def add_recurso(self, tipo: str, cantidad: int):
        #Suma cantidad al recurso indicado. Usar cantidad negativa para restar.
        conn = get_connection()
        try:
            conn.execute(
                f"UPDATE recursos_jugador SET {tipo} = {tipo} + ? WHERE id = 1",
                (cantidad,)
            )
            conn.commit()
        finally:
            conn.close()

    def get_pociones(self) -> dict | None:
        #Devuelve el número de pociones actuales del jugador.
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT pociones, pociones_max FROM recursos_jugador WHERE id = 1"
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def set_ultima_regen(self, timestamp: str):
        #Guarda el timestamp de la última regeneración de pociones.
        #timestamp formato : '2024-01-15 10:30:00'
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE recursos_jugador SET ultima_regen = ? WHERE id = 1",
                (timestamp,)
            )
            conn.commit()
        finally:
            conn.close()