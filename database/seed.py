import sqlite3
from database.db_manager import get_connection

#DATOS REALES

#(nombre, faccion, clase, rareza, atk_base, defensa_base, magia_base, pv_base, destreza_base, sprite_id, icono)
#Stats por clase y rareza según tabla 1.1 del GDD
PERSONAJES = [
    #Guardianes — B: Guerrero + Mago | A: Guerrero + Mago | S: Asesino + Mago
    ("Guardian_Guerrero_B",  "guardian", "guerrero", "B", 130, 100, 0,   600, 0,
        None,
        "assets/logos/IconoGerreroBGuardian.png"),
    ("Guardian_Mago_B",      "guardian", "mago",     "B", 50,  80,  100, 400, 0,
        None,
        "assets/logos/IconoMagoBGuardian.png"),
    ("Guardian_Guerrero_A",  "guardian", "guerrero", "A", 156, 120, 0,   720, 0,
        None,
        "assets/logos/GuerreroAGuardian.png"),
    ("Guardian_Mago_A",      "guardian", "mago",     "A", 60,  96,  120, 480, 0,
        None,
        "assets/logos/IconoMagoAGuardian.png"),
    ("Guardian_Asesino_S",   "guardian", "asesino",  "S", 198, 165, 0,   920, 90,
        None,
        "assets/logos/IconoAsesinoSGuardian.png"),
    ("Guardian_Mago_S",      "guardian", "mago",     "S", 90,  200, 185, 750, 0,
        None,
        "assets/logos/IconoMagoGuardianS.png"),
    #Anomalías — B: Guerrero + Asesino | A: Asesino + Mago | S: Guerrero + Mago
    ("Anomalia_Guerrero_B",  "anomalia", "guerrero", "B", 130, 100, 0,   600, 0,
        None,
        "assets/logos/IconoGuerreroBAnomalia.png"),
    ("Anomalia_Asesino_B",   "anomalia", "asesino",  "B", 110, 90,  0,   500, 50,
        None,
        "assets/logos/IconoAsesinoBAnomalia.png"),
    ("Anomalia_Asesino_A",   "anomalia", "asesino",  "A", 132, 108, 0,   600, 60,
        None,
        "assets/logos/IconoAsesinoAAnomaliaA.png"),
    ("Anomalia_Mago_A",      "anomalia", "mago",     "A", 60,  96,  120, 480, 0,
        None,
        "assets/logos/IconoMagoAAnomaliaA.png"),
    ("Anomalia_Guerrero_S",  "anomalia", "guerrero", "S", 240, 195, 0,   1100, 0,
        None,
        "assets/logos/IconoGuerreroAnomaliaS.png"),
    ("Anomalia_Mago_S",      "anomalia", "mago",     "S", 90,  200, 185, 750, 0,
        None,
        "assets/logos/IconoMagoAnomalia.png"),
]

#(nombre, rareza, bonus_atk, bonus_magia, bonus_pv, bonus_def, bonus_destreza, personaje_s_id, efecto_especial, icono)
#personaje_s_id: Guardian_Asesino_S=5, Anomalia_Mago_S=12 (ids por orden de inserción)
#Armas según tabla 1.5 del GDD
ARMAS = [
    #Básicas — una por clase
    ("Mandoble",            "B", 20, 0,  0, 0,  0,  None, None, "assets/logos/IconoMandobleB.jpg"),
    ("Baston",              "B", 0,  20, 0, 0,  0,  None, None, "assets/logos/IconoBastonB.jpg"),
    ("Daga",                "B", 20, 0,  0, 0,  0,  None, None, "assets/logos/IconoDagaB.jpg"),
    #S únicas — efectos especiales pendientes hasta Sprint 4
    ("Hambre Voraz",        "S", 55, 0,  0, 55, 0,  None, "TODO: efecto especial", "assets/logos/IconoMazaS.png"),
    ("Magia Interior",      "S", 0,  55, 0, 40, 0,  None, "TODO: efecto especial", "assets/logos/IconoBastonS.png"),
    ("Tirada del Destino",  "S", 25, 0,  0, 0,  50, None, "TODO: efecto especial", "assets/logos/IconoDagaS.png"),
    ("Sombra Runica",       "S", 0, 55, 0, 40, 0, None, "TODO: efecto especial", "assets/logos/IconoSombras.png"),
]

#(nombre, rareza, bonus_atk, bonus_magia, bonus_pv, bonus_def, bonus_destreza, efecto_especial)
#Runas según tablas 1.3 y 1.4 del GDD
RUNAS = [
    #Básicas
    ("RUNA_ATAQUE",    "basica", 25, 0,  0, 0,  0,  None),
    ("RUNA_MAGIA",     "basica", 0,  30, 0, 0,  0,  None),
    ("RUNA_DEFENSA",   "basica", 0,  0,  0, 20, 0,  None),
    ("RUNA_DESTREZA",  "basica", 0,  0,  0, 0,  25, None),
    #Mixtas — resultado del transmutador
    ("RUNA_ACERO",     "mixta",  30, 0,  0, 20, 0,  None),   # ATAQUE + DEFENSA
    ("RUNA_CAZA",      "mixta",  20, 0,  0, 0,  25, None),   # ATAQUE + DESTREZA
    ("RUNA_SOMBRA",    "mixta",  0,  0,  0, 15, 30, None),   # DESTREZA + DEFENSA
    ("RUNA_ARCANA",    "mixta",  0,  30, 0, 10, 0,  None),   # MAGIA + DEFENSA
    ("RUNA_GUARDIAN",  "mixta",  0,  0,  0, 40, 0,  None),   # DESTREZA + MAGIA — mayor DEF del juego
    #Penalización — resultado de combinación inválida en el transmutador
    ("RUNA_ROTA",      "rota",   0,  0,  0, -40, 0, "Penalización por combinación inválida"),
]

#FUNCIONES DE SEED

def _tabla_vacia(cursor: sqlite3.Cursor, tabla: str) -> bool:
    count = cursor.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]
    return count == 0


def seed_personajes(cursor: sqlite3.Cursor):
    if not _tabla_vacia(cursor, "personajes_catalogo"):
        print("personajes_catalogo ya tiene datos.")
        return
    cursor.executemany("""
        INSERT INTO personajes_catalogo
            (nombre, faccion, clase, rareza, atk_base, defensa_base, magia_base, pv_base, destreza_base, sprite_id, icono)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, PERSONAJES)
    print(f"{len(PERSONAJES)} personajes insertados.")


def seed_armas(cursor: sqlite3.Cursor):
    if not _tabla_vacia(cursor, "armas_catalogo"):
        print("armas_catalogo ya tiene datos.")
        return
    cursor.executemany("""
        INSERT INTO armas_catalogo
            (nombre, rareza, bonus_atk, bonus_magia, bonus_pv, bonus_def, bonus_destreza, personaje_s_id, efecto_especial, icono)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ARMAS)
    print(f"{len(ARMAS)} armas insertadas.")


def seed_runas(cursor: sqlite3.Cursor):
    if not _tabla_vacia(cursor, "runas_catalogo"):
        print("runas_catalogo ya tiene datos.")
        return
    cursor.executemany("""
        INSERT INTO runas_catalogo
            (nombre, rareza, bonus_atk, bonus_magia, bonus_pv, bonus_def, bonus_destreza, efecto_especial)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, RUNAS)
    print(f"{len(RUNAS)} runas insertadas.")


def seed_recursos(cursor: sqlite3.Cursor):
    if not _tabla_vacia(cursor, "recursos_jugador"):
        print("recursos_jugador ya tiene datos.")
        return
    cursor.execute("""
        INSERT INTO recursos_jugador
            (id, monedas, tickets_personaje, tickets_arma, pociones, pociones_max,
            ultima_regen, transmutadores, fragmentos_rojos, fragmentos_azules,
            vida_actual, vida_max)
        VALUES (1, 0, 20, 20, 5, 10, NULL, 0, 0, 0, 0, 0)
    """)
    print("Recursos iniciales insertados.")


def seed_pity(cursor: sqlite3.Cursor):
    if not _tabla_vacia(cursor, "contadores_pity"):
        print("contadores_pity ya tiene datos.")
        return
    cursor.executemany(
        "INSERT INTO contadores_pity (jugador_id, banner, contador) VALUES (?, ?, ?)",
        [(1, "personajes", 0), (1, "armas", 0)]
    )
    print("Contadores de pity insertados.")


def seed_mapa(cursor: sqlite3.Cursor):
    if not _tabla_vacia(cursor, "progreso_mapa"):
        print("progreso_mapa ya tiene datos.")
        return
    nodos = [
        (1,  "disponible", 0, 0),
        (2,  "bloqueado",  0, 0),
        (3,  "bloqueado",  0, 0),
        (4,  "bloqueado",  0, 0),
        (5,  "bloqueado",  0, 0),   # KRONOS — jefe
        (6,  "bloqueado",  0, 0),
        (7,  "bloqueado",  0, 0),
        (8,  "bloqueado",  0, 0),
        (9,  "bloqueado",  0, 0),
        (10, "bloqueado",  0, 0),   # KRONOS DEFINITIVO — jefe final
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