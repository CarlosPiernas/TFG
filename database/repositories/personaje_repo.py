import sqlite3
from database.db_manager import get_connection

class PersonajeRepo:

    def get_catalogo(self) -> list[dict]:
        #Devuelve todos los personajes del catálogo en un diccionario.
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM personajes_catalogo").fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_by_faccion(self, faccion: str) -> list[dict]:
        #Devuelve todos los personajes de una facción.
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM personajes_catalogo WHERE faccion = ?", (faccion,)
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_by_id(self, personaje_id: int) -> dict | None:
        #Devuelve un personaje del catálogo por su id. Devuelve None si no existe.
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT * FROM personajes_catalogo WHERE id = ?", (personaje_id,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def get_by_rareza(self, rareza: str) -> list[dict]:
        #Devuelve todos los personajes de una rareza.
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM personajes_catalogo WHERE rareza = ?", (rareza,)
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_by_rareza_y_faccion(self, rareza: str, faccion: str) -> list[dict]:
        #Devuelve los personajes de una rareza y facción concretas.
        #gacha.py usa esto para filtrar el pool del banner por facción del jugador.
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM personajes_catalogo WHERE rareza = ? AND faccion = ?",
                (rareza, faccion)
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()
# Devuelve la ruta al sprite de un personaje dado su faccion, clase, rareza y tipo de animacion
def get_sprite_path(faccion: str, clase: str, rareza: str, tipo: str) -> str:
    import os
    base = f"{faccion.lower()}_{clase.lower()}_{rareza.lower()}"
    for ext in ("png", "jpg", "jpeg"):
        ruta = f"assets/characters/{base}/{base}_{tipo}.{ext}"
        if os.path.exists(ruta):
            return ruta
    # Si no encuentra ninguno, devuelve el png por defecto (Kivy mostrará placeholder)
    return f"assets/characters/{base}/{base}_{tipo}.png"
    #Cosas para que tengáis en cuenta:
    #1. Siempre se cierra la conexión con el finally, así se evitan errores de seguridad
    #2. Las consultas que devuelven más de un resultado se ordenan en una lista de diccionarios (cada diccionario es una fila de la bdd)