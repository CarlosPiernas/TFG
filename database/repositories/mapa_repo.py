import sqlite3
from database.db_manager import get_connection


class MapaRepo:

    def get_nodo(self, nodo_id: int) -> dict | None:
        #Devuelve el estado de un nodo. Devuelve None si no existe.
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT * FROM progreso_mapa WHERE nodo_id = ?", (nodo_id,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def get_todos_nodos(self) -> list[dict]:
        #Devuelve el estado de todos los nodos del mapa.
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM progreso_mapa ORDER BY nodo_id"
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def completar_nodo(self, nodo_id: int, estrellas: int):
        #Marca un nodo como completado y desbloquea el siguiente.
        #Guarda las estrellas solo si son mejores que las anteriores.
        conn = get_connection()
        try:
            conn.execute("""
                UPDATE progreso_mapa
                SET estado = 'completado', estrellas = MAX(estrellas, ?)
                WHERE nodo_id = ?
            """, (estrellas, nodo_id))
            conn.execute("""
                UPDATE progreso_mapa SET estado = 'disponible'
                WHERE nodo_id = ? AND estado = 'bloqueado'
            """, (nodo_id + 1,))
            conn.commit()
        finally:
            conn.close()

    def incrementar_intentos(self, nodo_id: int):
        #Suma 1 al contador de intentos de un nodo.
        conn = get_connection()
        try:
            conn.execute("""
                UPDATE progreso_mapa SET intentos = intentos + 1
                WHERE nodo_id = ?
            """, (nodo_id,))
            conn.commit()
        finally:
            conn.close()