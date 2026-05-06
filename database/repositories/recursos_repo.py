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
        #Solo acepta columnas válidas.
        columnas_validas = {
            "monedas", "tickets_personaje", "tickets_arma",
            "pociones", "transmutadores",
            "fragmentos_rojos", "fragmentos_azules"
        }
        if tipo not in columnas_validas:
            raise ValueError(f"Columna no válida: {tipo}")
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

    def get_monedas(self) -> int:
        #Devuelve las monedas actuales del jugador.
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT monedas FROM recursos_jugador WHERE id = 1"
            ).fetchone()
            return row["monedas"] if row else 0
        finally:
            conn.close()

    def set_ultima_regen(self, timestamp: str):
        #Guarda el timestamp de la última regeneración de pociones.
        #timestamp formato: '2024-01-15 10:30:00'
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE recursos_jugador SET ultima_regen = ? WHERE id = 1",
                (timestamp,)
            )
            conn.commit()
        finally:
            conn.close()
            
    def set_faccion(self, faccion: str):
    # Guarda la facción elegida por el jugador en la fila única de recursos
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE recursos_jugador SET faccion = ? WHERE id = 1",
                (faccion,)
            )
            conn.commit()
        finally:
            conn.close()

    def get_tickets(self, jugador_id: int, banner: str) -> int:
        #Devuelve los tickets disponibles del jugador para el banner indicado.
        #banner = 'personajes' → tickets_personaje | 'armas' → tickets_arma
        columna = "tickets_personaje" if banner == "personajes" else "tickets_arma"
        conn = get_connection()
        try:
            row = conn.execute(
                f"SELECT {columna} FROM recursos_jugador WHERE id = 1"
            ).fetchone()
            return row[columna] if row else 0
        finally:
            conn.close()

    def consumir_ticket(self, jugador_id: int, banner: str, cantidad: int) -> bool:
        #Resta tickets del banner indicado si hay saldo suficiente.
        #Devuelve True si se pudo consumir, False si no hay tickets.
        #gacha.py llama esto DESPUÉS de verificar que hay item disponible.
        columna = "tickets_personaje" if banner == "personajes" else "tickets_arma"
        conn = get_connection()
        try:
            #Comprobamos saldo antes de restar
            row = conn.execute(
                f"SELECT {columna} FROM recursos_jugador WHERE id = 1"
            ).fetchone()
            if row is None or row[columna] < cantidad:
                return False
            conn.execute(
                f"UPDATE recursos_jugador SET {columna} = {columna} - ? WHERE id = 1",
                (cantidad,)
            )
            conn.commit()
            return True
        finally:
            conn.close()

    def agregar_fragmento(self, jugador_id: int, tipo: str, cantidad: int):
        #Suma fragmentos al jugador según el tipo de banner.
        #tipo = 'rojo' (personaje duplicado) | 'azul' (arma duplicada)
        columna = "fragmentos_rojos" if tipo == "rojo" else "fragmentos_azules"
        conn = get_connection()
        try:
            conn.execute(
                f"UPDATE recursos_jugador SET {columna} = {columna} + ? WHERE id = 1",
                (cantidad,)
            )
            conn.commit()
        finally:
            conn.close()

    def get_transmutadores(self) -> int:
        # Devuelve la cantidad de transmutadores del jugador
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT transmutadores FROM recursos_jugador WHERE id = 1"
            ).fetchone()
            return row["transmutadores"] if row else 0
        finally:
            conn.close()

    def consumir_transmutador(self) -> bool:
        # Consume 1 transmutador si hay. Devuelve True si se consumió, False si no había.
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT transmutadores FROM recursos_jugador WHERE id = 1"
            ).fetchone()
            if row is None or row["transmutadores"] <= 0:
                return False
            conn.execute(
                "UPDATE recursos_jugador SET transmutadores = transmutadores - 1 WHERE id = 1"
            )
            conn.commit()
            return True
        finally:
            conn.close()

    # ═══════════════════════════════════
    # VIDA DEL JUGADOR (persistente entre nodos)
    # ═══════════════════════════════════

    def get_vida(self) -> dict:
        # Devuelve la vida actual y máxima del jugador.
        # Si la fila no existe o las columnas son nulas, devuelve {0, 0}.
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT vida_actual, vida_max FROM recursos_jugador WHERE id = 1"
            ).fetchone()
            if row is None:
                return {"vida_actual": 0, "vida_max": 0}
            return {
                "vida_actual": row["vida_actual"] or 0,
                "vida_max":    row["vida_max"]    or 0,
            }
        finally:
            conn.close()

    def set_vida(self, vida_actual: int, vida_max: int):
        # Guarda la vida actual y máxima del jugador. La vida actual queda
        # acotada al rango [0, vida_max] para evitar valores incoherentes.
        if vida_max < 0:
            vida_max = 0
        if vida_actual < 0:
            vida_actual = 0
        if vida_actual > vida_max:
            vida_actual = vida_max
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE recursos_jugador SET vida_actual = ?, vida_max = ? WHERE id = 1",
                (vida_actual, vida_max)
            )
            conn.commit()
        finally:
            conn.close()

    def restaurar_vida(self):
        # Restaura la vida actual al máximo. Usado al consumir una poción.
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE recursos_jugador SET vida_actual = vida_max WHERE id = 1"
            )
            conn.commit()
        finally:
            conn.close()

    def get_personaje_activo_id(self) -> int:
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT personaje_activo_id FROM recursos_jugador WHERE id = 1"
            ).fetchone()
            return row["personaje_activo_id"] if row else 0
        finally:
            conn.close()

    def set_personaje_activo_id(self, inv_id: int):
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE recursos_jugador SET personaje_activo_id = ? WHERE id = 1",
                (inv_id,)
            )
            conn.commit()
        finally:
            conn.close()