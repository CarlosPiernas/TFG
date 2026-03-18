import sqlite3
from database.db_manager import get_connection

#DATOS EJEMPLO

#(nombre, faccion, clase, rareza, atk_base, magia_base, pv_base, destreza_base, sprite_id)
PERSONAJES = [
    #Guardianes
    ("Guardian_Guerrero_B",  "guardian", "guerrero", "B", 80,  20,  200, 30,  None),
    ("Guardian_Mago_B",      "guardian", "mago",     "B", 20,  90,  150, 40,  None),
    ("Guardian_Asesino_B",   "guardian", "asesino",  "B", 60,  30,  160, 80,  None),
    ("Guardian_Guerrero_A",  "guardian", "guerrero", "A", 100, 25,  240, 35,  None),
    ("Guardian_Mago_A",      "guardian", "mago",     "A", 25,  110, 180, 45,  None),
    ("Guardian_Asesino_S",   "guardian", "asesino",  "S", 90,  40,  200, 120, None),
    #Anomalías
    ("Anomalia_Guerrero_B",  "anomalia", "guerrero", "B", 85,  15,  210, 25,  None),
    ("Anomalia_Mago_B",      "anomalia", "mago",     "B", 15,  95,  145, 35,  None),
    ("Anomalia_Asesino_B",   "anomalia", "asesino",  "B", 65,  25,  155, 85,  None),
    ("Anomalia_Guerrero_A",  "anomalia", "guerrero", "A", 105, 20,  250, 30,  None),
    ("Anomalia_Mago_A",      "anomalia", "mago",     "A", 20,  115, 175, 40,  None),
    ("Anomalia_Asesino_S",   "anomalia", "asesino",  "S", 95,  35,  195, 125, None),
]

#(nombre, rareza, bonus_atk, bonus_magia, bonus_pv, bonus_destreza, personaje_s_id, efecto_especial)
#personaje_s_id usa el índice del personaje S en personajes (base 1): Guardian_Asesino_S=6, Anomalia_Asesino_S=12
ARMAS = [
    ("Espada_Basica",    "basica", 20, 0,  0,  0,   None, None),
    ("Baston_Basico",    "basica", 0,  25, 0,  0,   None, None),
    ("Daga_Basica",      "basica", 15, 0,  0,  20,  None, None),
    ("Espada_Basica_2",  "basica", 22, 0,  10, 0,   None, None),
    ("Baston_Basico_2",  "basica", 0,  28, 5,  0,   None, None),
    #personaje_s_id se actualiza cuando tengamos los ids reales para el seed
    ("Hoja_Guardian_S",  "S",      40, 0,  0,  50,  6,    "TODO: efecto especial"),
    ("Hoja_Anomalia_S",  "S",      45, 0,  0,  55,  12,   "TODO: efecto especial"),
]

#(nombre, rareza, bonus_atk, bonus_magia, bonus_pv, bonus_destreza, efecto_especial)
RUNAS = [
    #Genéricas
    ("Runa_Ataque",    "generica", 15, 0,  0,   0,  None),
    ("Runa_Magia",     "generica", 0,  15, 0,   0,  None),
    ("Runa_Vida",      "generica", 0,  0,  40,  0,  None),
    ("Runa_Destreza",  "generica", 0,  0,  0,   15, None),
    ("Runa_Mixta",     "generica", 8,  8,  0,   0,  None),
    #Únicas S — efectos especiales pendientes de decisión del equipo
    ("Runa_Guardian_S_1", "unica_S", 0, 0, 0, 0, "TODO: efecto especial"),
    ("Runa_Guardian_S_2", "unica_S", 0, 0, 0, 0, "TODO: efecto especial"),
    ("Runa_Anomalia_S_1", "unica_S", 0, 0, 0, 0, "TODO: efecto especial"),
    ("Runa_Anomalia_S_2", "unica_S", 0, 0, 0, 0, "TODO: efecto especial"),
]

#FUNCIONES DE SEED

def _tabla_vacia(cursor: sqlite3.Cursor, tabla: str) -> bool:
    #Devuelve True si la tabla no tiene filas.
    count = cursor.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]
    return count == 0


def seed_personajes(cursor: sqlite3.Cursor):
    if not _tabla_vacia(cursor, "personajes_catalogo"):
        print("personajes_catalogo ya tiene datos.")
        return
    cursor.executemany("""
        INSERT INTO personajes_catalogo
            (nombre, faccion, clase, rareza, atk_base, magia_base, pv_base, destreza_base, sprite_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, PERSONAJES)
    print(f"{len(PERSONAJES)} personajes insertados.")


def seed_armas(cursor: sqlite3.Cursor):
    if not _tabla_vacia(cursor, "armas_catalogo"):
        print("armas_catalogo ya tiene datos.")
        return
    cursor.executemany("""
        INSERT INTO armas_catalogo
            (nombre, rareza, bonus_atk, bonus_magia, bonus_pv, bonus_destreza, personaje_s_id, efecto_especial)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ARMAS)
    print(f"{len(ARMAS)} armas insertadas.")


def seed_runas(cursor: sqlite3.Cursor):
    if not _tabla_vacia(cursor, "runas_catalogo"):
        print("runas_catalogo ya tiene datos.")
        return
    cursor.executemany("""
        INSERT INTO runas_catalogo
            (nombre, rareza, bonus_atk, bonus_magia, bonus_pv, bonus_destreza, efecto_especial)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, RUNAS)
    print(f"{len(RUNAS)} runas insertadas.")


def seed_recursos(cursor: sqlite3.Cursor):
    if not _tabla_vacia(cursor, "recursos_jugador"):
        print("recursos_jugador ya tiene datos.")
        return
    cursor.execute("""
        INSERT INTO recursos_jugador
            (id, tickets_personaje, tickets_arma, moneda_premium, pociones, pociones_max, ultima_regen)
        VALUES (1, 10, 5, 100, 5, 5, NULL)
    """)
    print("Recursos iniciales insertados.")


def seed_pity(cursor: sqlite3.Cursor):
    if not _tabla_vacia(cursor, "contadores_pity"):
        print("contadores_pity ya tiene datos.")
        return
    cursor.executemany(
        "INSERT INTO contadores_pity (banner, contador) VALUES (?, ?)",
        [("personajes", 0), ("armas", 0)]
    )
    print("Contadores de pity insertados.")


def seed_mapa(cursor: sqlite3.Cursor):
    if not _tabla_vacia(cursor, "progreso_mapa"):
        print("progreso_mapa ya tiene datos.")
        return
    nodos = [
        (1, "disponible", 0, 0),  # El nodo 1 empieza desbloqueado
        (2, "bloqueado",  0, 0),
        (3, "bloqueado",  0, 0),
        (4, "bloqueado",  0, 0),
        (5, "bloqueado",  0, 0),
    ]
    cursor.executemany("""
        INSERT INTO progreso_mapa (nodo_id, estado, estrellas, intentos)
        VALUES (?, ?, ?, ?)
    """, nodos)
    print(f"{len(nodos)} nodos insertados.")


def run_seed():
    print("Ejecutando seed...")
    conn = get_connection()
    try:
        cursor = conn.cursor()
        seed_personajes(cursor)
        seed_armas(cursor)
        seed_runas(cursor)
        seed_recursos(cursor)
        seed_pity(cursor)
        seed_mapa(cursor)
        conn.commit()
        print("Seed completado.")
    except sqlite3.Error as e:
        print(f"[ERROR] Fallo en el seed: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    run_seed()