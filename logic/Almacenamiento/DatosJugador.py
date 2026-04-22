"""
DatosJugador — Estado completo del jugador.
Esta clase es todo lo que el jugador posee.
Tanto la Mochila como la Forja leen y modifican estos datos.
Cuando se integre la base de datos, solo hay que añadir métodos
cargar_desde_bd() y guardar_en_bd() sin tocar Mochila ni Forja.
"""

from logic.Clases.stat import PERSONAJES, FRAGMENTOS_PARA_ELEGIR


class DatosJugador:

    def __init__(self, nombre_jugador="Jugador"):
        self.nombre = nombre_jugador

        # ── Desbloqueos (sets de nombres/IDs) ──
        self.personajes_desbloqueados = set()
        self.armas_desbloqueadas = set()

        # ── Runas: nombre → cantidad ──
        self.runas = {}

        # ── Moneda ──
        self.monedas = 0

        # ── Consumibles ──
        self.pociones = 0
        self.transmutadores = 0
        self.tickets_personaje = 0
        self.tickets_arma = 0

        # ── Fragmentos ──
        self.fragmentos_personaje = 0   # rojos
        self.fragmentos_arma = 0        # azules

        # ── Progreso ──
        self.nodos_vencidos = set()
        self.nodo_actual = 0

    # ═══════════════════════════════════
    # MONEDAS
    # ═══════════════════════════════════

    def ganar_monedas(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva.")
        self.monedas += cantidad

    def gastar_monedas(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva.")
        if self.monedas < cantidad:
            raise ValueError(
                f"Monedas insuficientes: tienes {self.monedas}, necesitas {cantidad}."
            )
        self.monedas -= cantidad

    # ═══════════════════════════════════
    # PERSONAJES
    # ═══════════════════════════════════

    def desbloquear_personaje(self, nombre):
        """
        Intenta desbloquear un personaje.
        Si ya lo tiene → genera 1 fragmento de personaje.
        Devuelve (es_nuevo, nombre).
        """
        if nombre in self.personajes_desbloqueados:
            self.fragmentos_personaje += 1
            return False, nombre
        else:
            self.personajes_desbloqueados.add(nombre)
            return True, nombre

    def tiene_personaje(self, nombre):
        return nombre in self.personajes_desbloqueados

    # ═══════════════════════════════════
    # ARMAS
    # ═══════════════════════════════════

    def desbloquear_arma(self, nombre):
        """
        Intenta desbloquear un arma.
        Si ya la tiene → genera 1 fragmento de arma.
        Devuelve (es_nuevo, nombre).
        """
        if nombre in self.armas_desbloqueadas:
            self.fragmentos_arma += 1
            return False, nombre
        else:
            self.armas_desbloqueadas.add(nombre)
            return True, nombre

    def tiene_arma(self, nombre):
        return nombre in self.armas_desbloqueadas

    # ═══════════════════════════════════
    # RUNAS
    # ═══════════════════════════════════

    def agregar_runa(self, nombre, cantidad=1):
        self.runas[nombre] = self.runas.get(nombre, 0) + cantidad

    def quitar_runa(self, nombre, cantidad=1):
        actual = self.runas.get(nombre, 0)
        if actual < cantidad:
            raise ValueError(
                f"No tienes suficientes runas '{nombre}': "
                f"tienes {actual}, necesitas {cantidad}."
            )
        self.runas[nombre] -= cantidad
        if self.runas[nombre] == 0:
            del self.runas[nombre]

    def cantidad_runa(self, nombre):
        return self.runas.get(nombre, 0)

    def listar_runas(self):
        """Devuelve lista de (nombre, cantidad) ordenada."""
        return sorted(self.runas.items())

    # ═══════════════════════════════════
    # CONSUMIBLES
    # ═══════════════════════════════════

    def agregar_pociones(self, cantidad=1):
        self.pociones += cantidad

    def usar_pocion(self):
        if self.pociones <= 0:
            return False
        self.pociones -= 1
        return True

    def agregar_transmutadores(self, cantidad=1):
        self.transmutadores += cantidad

    def usar_transmutador(self):
        if self.transmutadores <= 0:
            return False
        self.transmutadores -= 1
        return True

    def agregar_ticket_personaje(self, cantidad=1):
        self.tickets_personaje += cantidad

    def agregar_ticket_arma(self, cantidad=1):
        self.tickets_arma += cantidad

    def usar_ticket_personaje(self):
        if self.tickets_personaje <= 0:
            return False
        self.tickets_personaje -= 1
        return True

    def usar_ticket_arma(self):
        if self.tickets_arma <= 0:
            return False
        self.tickets_arma -= 1
        return True

    # ═══════════════════════════════════
    # FRAGMENTOS
    # ═══════════════════════════════════

    def puede_canjear_personaje(self):
        return self.fragmentos_personaje >= FRAGMENTOS_PARA_ELEGIR

    def puede_canjear_arma(self):
        return self.fragmentos_arma >= FRAGMENTOS_PARA_ELEGIR

    def canjear_fragmentos_personaje(self, nombre):
        if not self.puede_canjear_personaje():
            raise ValueError(
                f"Fragmentos insuficientes: tienes {self.fragmentos_personaje}, "
                f"necesitas {FRAGMENTOS_PARA_ELEGIR}."
            )
        if nombre in self.personajes_desbloqueados:
            raise ValueError(f"Ya tienes desbloqueado '{nombre}'.")
        self.fragmentos_personaje -= FRAGMENTOS_PARA_ELEGIR
        self.personajes_desbloqueados.add(nombre)
        return nombre

    def canjear_fragmentos_arma(self, nombre):
        if not self.puede_canjear_arma():
            raise ValueError(
                f"Fragmentos insuficientes: tienes {self.fragmentos_arma}, "
                f"necesitas {FRAGMENTOS_PARA_ELEGIR}."
            )
        if nombre in self.armas_desbloqueadas:
            raise ValueError(f"Ya tienes desbloqueada '{nombre}'.")
        self.fragmentos_arma -= FRAGMENTOS_PARA_ELEGIR
        self.armas_desbloqueadas.add(nombre)
        return nombre

    # ═══════════════════════════════════
    # PROGRESO
    # ═══════════════════════════════════

    def registrar_nodo_vencido(self, nodo):
        self.nodos_vencidos.add(nodo)
        if nodo > self.nodo_actual:
            self.nodo_actual = nodo

    # ═══════════════════════════════════
    # RESUMEN (para debug)
    # ═══════════════════════════════════

    def __str__(self):
        runas_str = ", ".join(f"{k}×{v}" for k, v in sorted(self.runas.items())) or "ninguna"
        pers_str = ", ".join(sorted(self.personajes_desbloqueados)) or "ninguno"
        armas_str = ", ".join(sorted(self.armas_desbloqueadas)) or "ninguna"

        return (
            f"══════ DATOS DE {self.nombre.upper()} ══════\n"
            f"  Monedas:           {self.monedas}\n"
            f"  Personajes:        {pers_str}\n"
            f"  Armas:             {armas_str}\n"
            f"  Runas:             {runas_str}\n"
            f"  Pociones:          {self.pociones}\n"
            f"  Transmutadores:    {self.transmutadores}\n"
            f"  Tickets personaje: {self.tickets_personaje}\n"
            f"  Tickets arma:      {self.tickets_arma}\n"
            f"  Frag. personaje:   {self.fragmentos_personaje}\n"
            f"  Frag. arma:        {self.fragmentos_arma}\n"
            f"  Nodo actual:       {self.nodo_actual}\n"
            f"{'═' * 40}"
        )