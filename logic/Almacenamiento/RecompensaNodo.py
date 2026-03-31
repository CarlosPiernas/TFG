"""
RecompensaNodo — Recompensas al completar cada nodo.
Al completar un nodo, el jugador recibe automáticamente:
  Nodos 1-3:  50 monedas
  Nodo 4:     75 monedas + 1 runa básica
  Nodo 5:     100 monedas + 1 runa + 1 transmutador + 1 ticket personaje gratis
  Nodos 6-7:  100 monedas + 1 runa básica
  Nodos 8-9:  150 monedas + 1 runa básica
  Nodo 10:    200 monedas + 1 runa + 1 transmutador + 1 ticket aleatorio (50% pers / 50% arma)

Total por run: 1025 monedas + 7 runas + 2 transmutadores + 2 tickets gratis.
Nodos repetibles una vez vencidos.
"""
import random
from logic.Clases.stat import (
    MONEDAS_POR_NODO,
    NODOS_DROP_RUNA,
    NODOS_TRANSMUTADOR,
    NODOS_TICKET_GRATIS,
)

# Runas básicas que pueden dropear en nodos
_RUNAS_DROP = ["ATAQUE", "MAGIA", "DEFENSA", "DESTREZA"]


class RecompensaNodo:
    """
    Calcula y aplica las recompensas de un nodo al DatosJugador.
    Devuelve un log de lo que se obtuvo para que la UI lo muestre.
    """

    @staticmethod
    def aplicar(datos_jugador, nodo):
        """
        Aplica todas las recompensas del nodo al DatosJugador.
        Devuelve una lista de strings describiendo cada recompensa.
        """
        if nodo not in MONEDAS_POR_NODO:
            raise ValueError(f"Nodo inválido: {nodo}")

        log = []

        # ── Monedas ──
        monedas = MONEDAS_POR_NODO[nodo]
        datos_jugador.ganar_monedas(monedas)
        log.append(f"+{monedas} monedas (total: {datos_jugador.monedas})")

        # ── Runa básica (nodos 4-10) ──
        if nodo in NODOS_DROP_RUNA:
            runa = random.choice(_RUNAS_DROP)
            datos_jugador.agregar_runa(runa)
            log.append(f"Runa obtenida: RUNA_{runa} (total: {datos_jugador.cantidad_runa(runa)})")

        # ── Transmutador (jefes nodo 5 y 10) ──
        if nodo in NODOS_TRANSMUTADOR:
            datos_jugador.agregar_transmutadores(1)
            log.append(f"Transmutador obtenido (total: {datos_jugador.transmutadores})")

        # ── Ticket gratis (jefes) ──
        if nodo in NODOS_TICKET_GRATIS:
            tipo_ticket = NODOS_TICKET_GRATIS[nodo]

            if tipo_ticket == "personaje":
                datos_jugador.agregar_ticket_personaje(1)
                log.append(f"Ticket de personaje gratis obtenido (total: {datos_jugador.tickets_personaje})")
            elif tipo_ticket == "aleatorio":
                if random.random() < 0.5:
                    datos_jugador.agregar_ticket_personaje(1)
                    log.append(f"Ticket aleatorio: personaje (total: {datos_jugador.tickets_personaje})")
                else:
                    datos_jugador.agregar_ticket_arma(1)
                    log.append(f"Ticket aleatorio: arma (total: {datos_jugador.tickets_arma})")

        # ── Registrar nodo completado ──
        datos_jugador.registrar_nodo_vencido(nodo)

        return log

    @staticmethod
    def resumen_recompensas(nodo):
        """
        Devuelve un texto con las recompensas posibles del nodo (sin aplicar).
        Para que la UI muestre al jugador qué puede ganar.
        """
        if nodo not in MONEDAS_POR_NODO:
            return "Nodo inválido"

        partes = [f"{MONEDAS_POR_NODO[nodo]} monedas"]

        if nodo in NODOS_DROP_RUNA:
            partes.append("1 runa básica")
        if nodo in NODOS_TRANSMUTADOR:
            partes.append("1 transmutador")
        if nodo in NODOS_TICKET_GRATIS:
            tipo = NODOS_TICKET_GRATIS[nodo]
            if tipo == "personaje":
                partes.append("1 ticket personaje gratis")
            elif tipo == "aleatorio":
                partes.append("1 ticket aleatorio (personaje o arma)")

        return " + ".join(partes)