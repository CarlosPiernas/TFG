import sqlite3
import os

#CONFIGURACIÓN
dir_base = os.path.dirname(os.path.abspath(__file__))
ruta_bd  = os.path.join(dir_base, "..", "data", "game.db")


#CONEXIÓN
def get_connection() -> sqlite3.Connection:
    #Abre y devuelve una conexión a la base de datos.
    os.makedirs(os.path.dirname(ruta_bd), exist_ok=True)
    conn = sqlite3.connect(ruta_bd)
    conn.row_factory = sqlite3.Row   #Permite acceder a columnas por nombre: row["nombre"]
    conn.execute("PRAGMA foreign_keys = ON")  #Activa las foreign keys
    return conn


#CREACIÓN DE TABLAS
def initialize_db():
    #Crea todas las tablas si no existen.
    conn = get_connection()
    try:
        cursor = conn.cursor()

        #Personajes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personajes_catalogo (
                id              INTEGER PRIMARY KEY,
                nombre          TEXT    NOT NULL,
                faccion         TEXT    NOT NULL,
                clase           TEXT    NOT NULL,
                rareza          TEXT    NOT NULL,
                atk_base        INTEGER NOT NULL DEFAULT 0,
                defensa_base    INTEGER NOT NULL DEFAULT 0,
                magia_base      INTEGER NOT NULL DEFAULT 0,
                pv_base         INTEGER NOT NULL DEFAULT 0,
                destreza_base   INTEGER NOT NULL DEFAULT 0,
                sprite_id       TEXT,                            -- splash grande del personaje
                icono           TEXT                             -- icono circular para tarjetas/gacha
            )
        """)

        #Armas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS armas_catalogo (
                id                INTEGER PRIMARY KEY,
                nombre            TEXT    NOT NULL,
                rareza            TEXT    NOT NULL,
                bonus_atk         INTEGER NOT NULL DEFAULT 0,
                bonus_magia       INTEGER NOT NULL DEFAULT 0,
                bonus_pv          INTEGER NOT NULL DEFAULT 0,
                bonus_def         INTEGER NOT NULL DEFAULT 0,   -- usado por armas S (ej: Hambre Voraz +55 DEF)
                bonus_destreza    INTEGER NOT NULL DEFAULT 0,
                personaje_s_id    INTEGER,
                efecto_especial   TEXT,
                icono             TEXT,                          -- ruta al PNG del icono del arma
                FOREIGN KEY (personaje_s_id) REFERENCES personajes_catalogo(id)
            )
        """)

        #Runas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS runas_catalogo (
                id                INTEGER PRIMARY KEY,
                nombre            TEXT    NOT NULL,
                rareza            TEXT    NOT NULL,
                bonus_atk         INTEGER NOT NULL DEFAULT 0,
                bonus_magia       INTEGER NOT NULL DEFAULT 0,
                bonus_pv          INTEGER NOT NULL DEFAULT 0,
                bonus_def         INTEGER NOT NULL DEFAULT 0,   -- usado por RUNA_DEFENSA, RUNA_GUARDIAN, etc.
                bonus_destreza    INTEGER NOT NULL DEFAULT 0,
                efecto_especial   TEXT
            )
        """)

        #Inventario del jugador
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventario_jugador (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo        TEXT    NOT NULL,
                catalogo_id INTEGER NOT NULL
            )
        """)

        #Objetos equipados
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipamiento_activo (
                personaje_inv_id  INTEGER NOT NULL,  -- id del personaje en inventario_jugador
                slot              TEXT    NOT NULL,  -- 'arma' | 'runa_1' | 'runa_2'
                item_inv_id       INTEGER NOT NULL,  -- id del arma/runa en inventario_jugador
                PRIMARY KEY (personaje_inv_id, slot),
                FOREIGN KEY (personaje_inv_id) REFERENCES inventario_jugador(id),
                FOREIGN KEY (item_inv_id)      REFERENCES inventario_jugador(id)
            )
        """)

        #Progreso del mapa
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progreso_mapa (
                nodo_id     INTEGER PRIMARY KEY,
                estado      TEXT    NOT NULL DEFAULT 'bloqueado',
                estrellas   INTEGER NOT NULL DEFAULT 0,
                intentos    INTEGER NOT NULL DEFAULT 0
            )
        """)

        #Contadores de pity
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contadores_pity (
                jugador_id  INTEGER NOT NULL,
                banner      TEXT    NOT NULL,
                contador    INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (jugador_id, banner)
            )
        """)

        #Recursos del jugador
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recursos_jugador (
                id                  INTEGER PRIMARY KEY CHECK (id = 1),
                faccion             TEXT,
                tickets_personaje   INTEGER NOT NULL DEFAULT 0,
                tickets_arma        INTEGER NOT NULL DEFAULT 0,
                monedas             INTEGER NOT NULL DEFAULT 0,
                pociones            INTEGER NOT NULL DEFAULT 5,
                pociones_max        INTEGER NOT NULL DEFAULT 5,
                ultima_regen        TEXT,
                transmutadores      INTEGER NOT NULL DEFAULT 0,
                fragmentos_rojos    INTEGER NOT NULL DEFAULT 0,
                fragmentos_azules   INTEGER NOT NULL DEFAULT 0,
                vida_actual         INTEGER NOT NULL DEFAULT 0,
                vida_max            INTEGER NOT NULL DEFAULT 0
            )
        """)

        # Historial de tiradas gacha
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historial_gacha (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                jugador_id  INTEGER NOT NULL,
                banner      TEXT    NOT NULL,
                tipo        TEXT    NOT NULL,
                catalogo_id INTEGER NOT NULL,
                rareza      TEXT    NOT NULL,
                es_nuevo    INTEGER NOT NULL,
                fecha       TEXT    NOT NULL
            )
        """)

        conn.commit()
        print("Base de datos inicializada correctamente.")
    except sqlite3.Error as e:
        print(f"[ERROR] Error al inicializar la base de datos: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    initialize_db()
    print(f"Archivo creado en: {os.path.abspath(ruta_bd)}")
    conn = get_connection()
    tablas = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    conn.close()
    print("Tablas creadas:")
    for t in tablas:
        print(f"       - {t['name']}")