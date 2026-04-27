"""
Tienda — Compra de objetos con monedas.
Productos:
  Poción:             30 monedas
  Ticket personaje:  200 monedas
  Ticket arma:       150 monedas
  Transmutador:      100 monedas

Las tiradas de gacha NO son responsabilidad de la Tienda.
Eso lo gestiona logic/gacha.py a través de GameManager.
"""

from logic.Clases.stat import PRECIO_POCION, PRECIO_TICKET_PERS, PRECIO_TICKET_ARMA

PRECIO_TRANSMUTADOR = 100


class Tienda:
    """
    Tienda del juego. Opera sobre una instancia de DatosJugador
    cargada desde BD. Llama a guardar_en_bd() tras cada compra.
    """

    def __init__(self, datos_jugador):
        self.datos = datos_jugador

    # ── Comprar poción ───────────────────────────────────────

    def comprar_pocion(self) -> dict:
        if self.datos.monedas < PRECIO_POCION:
            return {"ok": False, "mensaje": f"Monedas insuficientes ({self.datos.monedas}/{PRECIO_POCION})."}
        self.datos.gastar_monedas(PRECIO_POCION)
        self.datos.agregar_pociones(1)
        self.datos.guardar_en_bd()
        return {"ok": True, "mensaje": f"Poción comprada. Pociones: {self.datos.pociones}. Monedas: {self.datos.monedas}."}

    # ── Comprar ticket personaje ─────────────────────────────

    def comprar_ticket_personaje(self) -> dict:
        if self.datos.monedas < PRECIO_TICKET_PERS:
            return {"ok": False, "mensaje": f"Monedas insuficientes ({self.datos.monedas}/{PRECIO_TICKET_PERS})."}
        self.datos.gastar_monedas(PRECIO_TICKET_PERS)
        self.datos.agregar_ticket_personaje(1)
        self.datos.guardar_en_bd()
        return {"ok": True, "mensaje": f"Ticket de personaje comprado. Tickets: {self.datos.tickets_personaje}. Monedas: {self.datos.monedas}."}

    # ── Comprar ticket arma ──────────────────────────────────

    def comprar_ticket_arma(self) -> dict:
        if self.datos.monedas < PRECIO_TICKET_ARMA:
            return {"ok": False, "mensaje": f"Monedas insuficientes ({self.datos.monedas}/{PRECIO_TICKET_ARMA})."}
        self.datos.gastar_monedas(PRECIO_TICKET_ARMA)
        self.datos.agregar_ticket_arma(1)
        self.datos.guardar_en_bd()
        return {"ok": True, "mensaje": f"Ticket de arma comprado. Tickets: {self.datos.tickets_arma}. Monedas: {self.datos.monedas}."}

    # ── Comprar transmutador ─────────────────────────────────

    def comprar_transmutador(self) -> dict:
        if self.datos.monedas < PRECIO_TRANSMUTADOR:
            return {"ok": False, "mensaje": f"Monedas insuficientes ({self.datos.monedas}/{PRECIO_TRANSMUTADOR})."}
        self.datos.gastar_monedas(PRECIO_TRANSMUTADOR)
        self.datos.agregar_transmutadores(1)
        self.datos.guardar_en_bd()
        return {"ok": True, "mensaje": f"Transmutador comprado. Cargas: {self.datos.transmutadores}. Monedas: {self.datos.monedas}."}

    # ── Consultas ────────────────────────────────────────────

    def precios(self) -> dict:
        return {
            "pocion":            PRECIO_POCION,
            "ticket_personaje":  PRECIO_TICKET_PERS,
            "ticket_arma":       PRECIO_TICKET_ARMA,
            "transmutador":      PRECIO_TRANSMUTADOR,
        }

    def puede_comprar(self) -> dict:
        m = self.datos.monedas
        return {
            "pocion":           m >= PRECIO_POCION,
            "ticket_personaje": m >= PRECIO_TICKET_PERS,
            "ticket_arma":      m >= PRECIO_TICKET_ARMA,
            "transmutador":     m >= PRECIO_TRANSMUTADOR,
        }