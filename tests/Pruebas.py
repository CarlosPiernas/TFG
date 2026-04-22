import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.Clases.Guerrero import Guerrero
from logic.Clases.Mago import Mago
from logic.Clases.Asesino import Asesino
from logic.Clases.EnemigoBasico import EnemigoBasico
from logic.Clases.EnemigoJefe import EnemigoJefe
from logic.Clases.stat import (
    STATS_GUERRERO, STATS_MAGO, STATS_ASESINO,
    STATS_GUERRERO_A, STATS_GUERRERO_S,
    STATS_MAGO_A,     STATS_MAGO_S,
    STATS_ASESINO_A,  STATS_ASESINO_S,
    ENEMIGOS,
    RUNA_ATAQUE, RUNA_DEFENSA, RUNA_MAGIA, RUNA_DESTREZA,
    RUNA_ACERO, RUNA_CAZA, RUNA_ARCANA, RUNA_SOMBRA, RUNA_GUARDIAN,
    ARMA_MANDOBLE, ARMA_BASTON, ARMA_DAGA,
    ARMA_S_GUERRERO, ARMA_S_MAGO, ARMA_S_ASESINO,
)
from logic.Combate.Encuentro import Encuentro, imprimir_log


def crear_enemigo(nodo):
    """Construye el enemigo del nodo indicado leyendo desde stat.py."""
    datos = ENEMIGOS[nodo]
    if datos["tipo"] == "jefe":
        return EnemigoJefe(datos["nombre"], datos["atk"], datos["vida"], datos["defensa"])
    return EnemigoBasico(datos["nombre"], datos["atk"], datos["vida"], datos["defensa"])


def equipar_para_nodo(jugador, nodo, clase):
    """
    Equipa al jugador con el equipamiento requerido para el nodo indicado.
    Nodos 1-4: sin equipo.
    Nodo 5 (jefe): 1 runa defensiva.
    Nodos 6-9 (básicos): 2 runas ofensivas.
    Nodo 10 (jefe): 2 runas defensivas + arma S.
    """
    armas   = {"Guerrero": ARMA_MANDOBLE, "Mago": ARMA_BASTON, "Asesino": ARMA_DAGA}
    armas_s = {"Guerrero": ARMA_S_GUERRERO, "Mago": ARMA_S_MAGO, "Asesino": ARMA_S_ASESINO}

    # ── Nodo 5 (jefe): 1 runa defensiva ──
    if nodo == 5:
        runa_n5 = {"Guerrero": RUNA_ACERO, "Mago": RUNA_GUARDIAN, "Asesino": RUNA_SOMBRA}
        jugador.equip_runa(runa_n5[clase], slot=1)

    # ── Nodos 6-9 (básicos): 2 runas ofensivas ──
    elif 6 <= nodo <= 9:
        runa1_of = {"Guerrero": RUNA_ATAQUE,  "Mago": RUNA_MAGIA,    "Asesino": RUNA_DESTREZA}
        runa2_of = {"Guerrero": RUNA_ACERO,   "Mago": RUNA_ARCANA,   "Asesino": RUNA_CAZA}
        jugador.equip_runa(runa1_of[clase], slot=1)
        jugador.equip_runa(runa2_of[clase], slot=2)

    # ── Nodo 10 (jefe final): 2 runas defensivas ──
    elif nodo == 10:
        runa1_def = {"Guerrero": RUNA_DEFENSA,  "Mago": RUNA_DEFENSA,  "Asesino": RUNA_DESTREZA}
        runa2_def = {"Guerrero": RUNA_ACERO,    "Mago": RUNA_GUARDIAN, "Asesino": RUNA_SOMBRA}
        jugador.equip_runa(runa1_def[clase], slot=1)
        jugador.equip_runa(runa2_def[clase], slot=2)

    # ── Armas ──
    if nodo >= 7 and nodo < 10:
        jugador.equip_arma(armas[clase])
    if nodo == 10:
        jugador.equip_arma(armas_s[clase])


def stats_para_nodo(clase, nodo):
    """Devuelve los stats base según rareza requerida por el nodo."""
    if nodo <= 7:   rareza = "B"
    elif nodo == 8: rareza = "A"
    else:           rareza = "S"  # nodos 9 y 10

    tabla = {
        "Guerrero": {"B": STATS_GUERRERO, "A": STATS_GUERRERO_A, "S": STATS_GUERRERO_S},
        "Mago":     {"B": STATS_MAGO,     "A": STATS_MAGO_A,     "S": STATS_MAGO_S},
        "Asesino":  {"B": STATS_ASESINO,  "A": STATS_ASESINO_A,  "S": STATS_ASESINO_S},
    }
    return tabla[clase][rareza]


def crear_jugador(clase, nodo):
    """Crea el jugador con la rareza adecuada para el nodo."""
    stats = stats_para_nodo(clase, nodo)
    if clase == "Guerrero": return Guerrero("ALEX",   **stats)
    if clase == "Mago":     return Mago("LYRA",       **stats)
    if clase == "Asesino":  return Asesino("CIPHER",  **stats)


def probar_clase_completa(clase):
    enc = Encuentro()

    print("\n" + "=" * 55)
    print(f"  {clase.upper()} — NODOS 1 AL 10")
    print("=" * 55)

    for nodo in range(1, 11):
        datos = ENEMIGOS[nodo]
        requisito = datos.get("requisito", "sin equipo")
        tipo = "JEFE" if datos["tipo"] == "jefe" else f"Nodo {nodo}"

        print(f"\n{'─' * 55}")
        print(f"  {tipo}: {datos['nombre']}  [{requisito}]")
        print(f"{'─' * 55}")

        jugador = crear_jugador(clase, nodo)
        equipar_para_nodo(jugador, nodo, clase)
        enemigo = crear_enemigo(nodo)
        imprimir_log(enc.iniciar(jugador, enemigo))


# ── Recorrido completo de las 3 clases ───────────────────
probar_clase_completa("Guerrero")
probar_clase_completa("Mago")
probar_clase_completa("Asesino")