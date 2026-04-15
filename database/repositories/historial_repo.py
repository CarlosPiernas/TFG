import sqlite3
from datetime import datetime
from database.db_manager import get_connection


class HistorialRepo:

    def registrar_tirada(self, jugador_id: int, banner: str, tipo: str,
                         catalogo_id: int, rareza: str, es_nuevo: bool):
        # Guarda una tirada en el historial.
        conn = get_connection()
        try:
            conn.execute("""
                INSERT INTO historial_gacha
                    (jugador_id, banner, tipo, catalogo_id, rareza, es_nuevo, fecha)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                jugador_id, banner, tipo, catalogo_id, rareza,
                1 if es_nuevo else 0,
                datetime.now().isoformat()
            ))
            conn.commit()
        finally:
            conn.close()

    def get_historial(self, jugador_id: int, banner: str = None) -> list[dict]:
        # Devuelve el historial del jugador, opcionalmente filtrado por banner.
        conn = get_connection()
        try:
            if banner:
                rows = conn.execute(
                    "SELECT * FROM historial_gacha WHERE jugador_id = ? AND banner = ? ORDER BY id DESC",
                    (jugador_id, banner)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM historial_gacha WHERE jugador_id = ? ORDER BY id DESC",
                    (jugador_id,)
                ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_ultimas_tiradas(self, jugador_id: int, cantidad: int = 10) -> list[dict]:
        # Devuelve las últimas N tiradas del jugador.
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM historial_gacha WHERE jugador_id = ? ORDER BY id DESC LIMIT ?",
                (jugador_id, cantidad)
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()