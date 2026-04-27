"""
Tienda — Compra de objetos y uso de tickets.
Productos:
  Poción:              30 monedas  — restaura vida + contadores al máximo
  Ticket personaje:   200 monedas  — tirada gacha del pool de personajes
  Ticket arma:        150 monedas  — tirada gacha del pool de armas
  Transmutador:       100 monedas  — carga para la Forja

Uso de tickets:
  Al usar un ticket, se hace una tirada aleatoria:
    Ticket personaje: B(60%), A(30%), S(10%)
    Ticket arma: básica(70%), S(30%)
  Si sale un duplicado → 1 fragmento del color correspondiente.
"""

import random
from logic.Clases.stat import (
    PRECIO_POCION, PRECIO_TICKET_PERS, PRECIO_TICKET_ARMA,
    PERSONAJES, PROB_PERSONAJE, PROB_ARMA,
)

PRECIO_TRANSMUTADOR = 100
# ══════════════════════════════════
# POOLS DE GACHA
# ═══════════════════════════════════
# Personajes agrupados por rareza
_POOL_PERS = {"B": [], "A": [], "S": []}
for _nombre, _datos in PERSONAJES.items():
    _POOL_PERS[_datos["rareza"]].append(_nombre)

# Armas agrupadas por tipo
_POOL_ARMAS = {
    "basica": ["Mandoble", "Bastón", "Daga"],
    "S":      ["Mandoble_Cronos", "Cetro_Vacío", "Hoja_Espectral"],
}


def _tirar_personaje():
    """
    Tirada aleatoria según probabilidades: B:60%, A:30%, S:10%.
    Devuelve (nombre, rareza).
    """
    r = random.random()
    if r < PROB_PERSONAJE["B"]:
        rareza = "B"
    elif r < PROB_PERSONAJE["B"] + PROB_PERSONAJE["A"]:
        rareza = "A"
    else:
        rareza = "S"
    nombre = random.choice(_POOL_PERS[rareza])
    return nombre, rareza


def _tirar_arma():
    """
    Tirada aleatoria según probabilidades: básica:70%, S:30%.
    Devuelve (nombre, tipo).
    """
    r = random.random()
    if r < PROB_ARMA["basica"]:
        tipo = "basica"
    else:
        tipo = "S"
    nombre = random.choice(_POOL_ARMAS[tipo])
    return nombre, tipo


class Tienda:
    """
    Tienda del juego. Opera sobre una instancia de DatosJugador.
    Todos los métodos devuelven un diccionario con el resultado
    para que la UI pueda mostrarlo.
    """

    def __init__(self, datos_jugador):
        self.datos = datos_jugador
    # ═══════════════════════════════════
    # COMPRAR POCIÓN
    # ═══════════════════════════════════
    def comprar_pocion(self):
        """
        Compra 1 poción por 30 monedas.
        Devuelve {"ok": bool, "mensaje": str}.
        """
        if self.datos.monedas < PRECIO_POCION:
            return {
                "ok": False,
                "mensaje": f"Monedas insuficientes ({self.datos.monedas}/{PRECIO_POCION}).",
            }
        self.datos.gastar_monedas(PRECIO_POCION)
        self.datos.agregar_pociones(1)
        return {
            "ok": True,
            "mensaje": f"Poción comprada. Pociones: {self.datos.pociones}. "
                       f"Monedas restantes: {self.datos.monedas}.",
        }
    # ═══════════════════════════════════
    # COMPRAR TICKET PERSONAJE
    # ═══════════════════════════════════
    def comprar_ticket_personaje(self):
        """
        Compra 1 ticket rojo por 200 monedas.
        Se guarda en el inventario para usarlo cuando el jugador quiera.
        """
        if self.datos.monedas < PRECIO_TICKET_PERS:
            return {
                "ok": False,
                "mensaje": f"Monedas insuficientes ({self.datos.monedas}/{PRECIO_TICKET_PERS}).",
            }
        self.datos.gastar_monedas(PRECIO_TICKET_PERS)
        self.datos.agregar_ticket_personaje(1)
        return {
            "ok": True,
            "mensaje": f"Ticket de personaje comprado. Tickets: {self.datos.tickets_personaje}. "
                       f"Monedas restantes: {self.datos.monedas}.",
        }

    # ═══════════════════════════════════
    # COMPRAR TICKET ARMA
    # ═══════════════════════════════════

    def comprar_ticket_arma(self):
        """
        Compra 1 ticket azul por 150 monedas.
        Se guarda en el inventario para usarlo cuando el jugador quiera.
        """
        if self.datos.monedas < PRECIO_TICKET_ARMA:
            return {
                "ok": False,
                "mensaje": f"Monedas insuficientes ({self.datos.monedas}/{PRECIO_TICKET_ARMA}).",
            }
        self.datos.gastar_monedas(PRECIO_TICKET_ARMA)
        self.datos.agregar_ticket_arma(1)
        return {
            "ok": True,
            "mensaje": f"Ticket de arma comprado. Tickets: {self.datos.tickets_arma}. "
                       f"Monedas restantes: {self.datos.monedas}.",
        }

    # ═══════════════════════════════════
    # COMPRAR TRANSMUTADOR
    # ═══════════════════════════════════

    def comprar_transmutador(self):
        """
        Compra 1 carga de transmutador por 100 monedas.
        """
        if self.datos.monedas < PRECIO_TRANSMUTADOR:
            return {
                "ok": False,
                "mensaje": f"Monedas insuficientes ({self.datos.monedas}/{PRECIO_TRANSMUTADOR}).",
            }
        self.datos.gastar_monedas(PRECIO_TRANSMUTADOR)
        self.datos.agregar_transmutadores(1)
        return {
            "ok": True,
            "mensaje": f"Transmutador comprado. Cargas: {self.datos.transmutadores}. "
                       f"Monedas restantes: {self.datos.monedas}.",
        }

    # ═══════════════════════════════════
    # USAR TICKET DE PERSONAJE (GACHA)
    # ═══════════════════════════════════

    def usar_ticket_personaje(self):
        """
        Consume 1 ticket de personaje y hace la tirada gacha.
        B: 60%, A: 30%, S: 10%.
        Si el personaje ya está desbloqueado → +1 fragmento rojo.
        Devuelve {"ok", "mensaje", "personaje", "rareza", "es_nuevo"}.
        """
        if not self.datos.usar_ticket_personaje():
            return {
                "ok": False,
                "mensaje": "No tienes tickets de personaje.",
            }

        nombre, rareza = _tirar_personaje()
        es_nuevo, _ = self.datos.desbloquear_personaje(nombre)

        if es_nuevo:
            msg = f"¡Nuevo personaje desbloqueado! {nombre} (rareza {rareza})"
        else:
            msg = (f"Personaje repetido: {nombre} (rareza {rareza}) "
                   f"→ +1 fragmento rojo ({self.datos.fragmentos_personaje})")

        return {
            "ok": True,
            "mensaje": msg,
            "personaje": nombre,
            "rareza": rareza,
            "es_nuevo": es_nuevo,
        }

    # ═══════════════════════════════════
    # USAR TICKET DE ARMA (GACHA)
    # ═══════════════════════════════════

    def usar_ticket_arma(self):
        """
        Consume 1 ticket de arma y hace la tirada gacha.
        Básica: 70%, S: 30%.
        Si el arma ya está desbloqueada → +1 fragmento azul.
        Devuelve {"ok", "mensaje", "arma", "tipo", "es_nuevo"}.
        """
        if not self.datos.usar_ticket_arma():
            return {
                "ok": False,
                "mensaje": "No tienes tickets de arma.",
            }

        nombre, tipo = _tirar_arma()
        es_nuevo, _ = self.datos.desbloquear_arma(nombre)

        if es_nuevo:
            msg = f"¡Nueva arma desbloqueada! {nombre} (tipo {tipo})"
        else:
            msg = (f"Arma repetida: {nombre} (tipo {tipo}) "
                   f"→ +1 fragmento azul ({self.datos.fragmentos_arma})")

        return {
            "ok": True,
            "mensaje": msg,
            "arma": nombre,
            "tipo": tipo,
            "es_nuevo": es_nuevo,
        }

    # ═══════════════════════════════════
    # CONSULTAR PRECIOS
    # ═══════════════════════════════════

    def precios(self):
        """Devuelve los precios de todos los productos de la tienda."""
        return {
            "pocion": PRECIO_POCION,
            "ticket_personaje": PRECIO_TICKET_PERS,
            "ticket_arma": PRECIO_TICKET_ARMA,
            "transmutador": PRECIO_TRANSMUTADOR,
        }

    def puede_comprar(self):
        """Devuelve qué items puede comprar el jugador con sus monedas actuales."""
        m = self.datos.monedas
        return {
            "pocion": m >= PRECIO_POCION,
            "ticket_personaje": m >= PRECIO_TICKET_PERS,
            "ticket_arma": m >= PRECIO_TICKET_ARMA,
            "transmutador": m >= PRECIO_TRANSMUTADOR,
        }