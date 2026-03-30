"""
demo.py — Demo interactiva del juego desde consola.

Ejecutar desde la raíz del proyecto:
    python demo.py

Permite probar todos los sistemas: gacha, combate, inventario, mapa.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from firebase.game_manager import GameManager

# ── Colores ──
RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[92m"
RED    = "\033[91m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
GRAY   = "\033[90m"
WHITE  = "\033[97m"

def color_rareza(r):
    if r == "S": return YELLOW
    if r == "A": return PURPLE
    return WHITE

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def separador():
    print(f"{GRAY}{'─'*55}{RESET}")

def titulo(msg):
    print(f"\n{CYAN}{BOLD}  {msg}{RESET}")
    separador()


# ═══════════════════════════════════
# MENÚ PRINCIPAL
# ═══════════════════════════════════

def menu_principal(gm):
    while True:
        print(f"""
{CYAN}{BOLD}══════════════════════════════════════{RESET}
{CYAN}{BOLD}  ANOMALÍAS vs GUARDIANES — DEMO{RESET}
{CYAN}{BOLD}══════════════════════════════════════{RESET}
  Facción: {YELLOW}{gm.faccion.upper()}{RESET}
  Personaje: {GREEN}{gm.get_personaje_activo_info()['nombre']}{RESET}
{GRAY}──────────────────────────────────────{RESET}
  1. Tirar gacha (personajes)
  2. Tirar gacha (armas)
  3. Tirar x10 (personajes)
  4. Ver inventario
  5. Ver recursos
  6. Ver mapa
  7. Combatir en un nodo
  8. Cambiar personaje activo
  9. Usar poción
  0. Salir
{GRAY}──────────────────────────────────────{RESET}""")

        opcion = input(f"  {CYAN}Elige opción: {RESET}").strip()

        if opcion == "1":
            tirar_gacha(gm, "personajes")
        elif opcion == "2":
            tirar_gacha(gm, "armas")
        elif opcion == "3":
            tirar_x10(gm, "personajes")
        elif opcion == "4":
            ver_inventario(gm)
        elif opcion == "5":
            ver_recursos(gm)
        elif opcion == "6":
            ver_mapa(gm)
        elif opcion == "7":
            combatir(gm)
        elif opcion == "8":
            cambiar_personaje(gm)
        elif opcion == "9":
            usar_pocion(gm)
        elif opcion == "0":
            print(f"\n  {CYAN}¡Hasta luego!{RESET}\n")
            break


# ═══════════════════════════════════
# GACHA
# ═══════════════════════════════════

def tirar_gacha(gm, banner):
    titulo(f"GACHA — Banner de {banner}")
    r = gm.tirar_gacha(banner)

    if "error" in r:
        print(f"  {RED}Error: {r['error']}{RESET}")
        return

    rareza = r["rareza"]
    nombre = r["item"]["nombre"]
    col = color_rareza(rareza)
    nuevo = f"{GREEN}★ NUEVO{RESET}" if r["es_nuevo"] else f"{RED}↩ duplicado → fragmento {r['fragmento']}{RESET}"
    pity = r["pity_count"]

    print(f"  {col}{BOLD}[{rareza}] {nombre}{RESET}  {nuevo}")
    print(f"  {GRAY}Pity counter: {pity}{RESET}")


def tirar_x10(gm, banner):
    titulo(f"MULTI-PULL x10 — Banner de {banner}")
    resultados = gm.tirar_gacha_x10(banner)

    if len(resultados) == 1 and "error" in resultados[0]:
        print(f"  {RED}Error: {resultados[0]['error']}{RESET}")
        return

    conteo = {"S": 0, "A": 0, "B": 0}
    for i, r in enumerate(resultados, 1):
        if "error" in r:
            print(f"  {RED}Pull {i}: {r['error']}{RESET}")
            continue
        rareza = r["rareza"]
        nombre = r["item"]["nombre"]
        col = color_rareza(rareza)
        nuevo = "★" if r["es_nuevo"] else "↩"
        conteo[rareza] = conteo.get(rareza, 0) + 1
        print(f"  {col}  {i:>2}. [{rareza}] {nombre:<28}{RESET} {nuevo}")

    separador()
    print(f"  Resumen: {YELLOW}{conteo.get('S',0)}xS{RESET}  "
          f"{PURPLE}{conteo.get('A',0)}xA{RESET}  "
          f"{WHITE}{conteo.get('B',0)}xB{RESET}")


# ═══════════════════════════════════
# INVENTARIO
# ═══════════════════════════════════

def ver_inventario(gm):
    titulo("INVENTARIO")

    personajes = gm.get_personajes_jugador()
    print(f"  {BOLD}Personajes ({len(personajes)}):{RESET}")
    for p in personajes:
        col = color_rareza(p["rareza"])
        activo = " ◄ ACTIVO" if p.get("inv_id") == gm.personaje_activo_id else ""
        print(f"    {col}[{p['rareza']}]{RESET} {p['nombre']:<28} {p['clase']:<10}{GREEN}{activo}{RESET}")

    armas = gm.get_armas_jugador()
    print(f"\n  {BOLD}Armas ({len(armas)}):{RESET}")
    if armas:
        for a in armas:
            col = color_rareza(a["rareza"])
            print(f"    {col}[{a['rareza']}]{RESET} {a['nombre']}")
    else:
        print(f"    {GRAY}Ninguna{RESET}")

    runas = gm.get_runas_jugador()
    print(f"\n  {BOLD}Runas ({len(runas)}):{RESET}")
    if runas:
        for r in runas:
            print(f"    {r['nombre']}")
    else:
        print(f"    {GRAY}Ninguna{RESET}")


# ═══════════════════════════════════
# RECURSOS
# ═══════════════════════════════════

def ver_recursos(gm):
    titulo("RECURSOS")
    r = gm.get_recursos()
    if not r:
        print(f"  {RED}No se pudieron cargar.{RESET}")
        return

    print(f"  Tickets personaje : {YELLOW}{r.get('tickets_personaje', 0)}{RESET}")
    print(f"  Tickets arma      : {YELLOW}{r.get('tickets_arma', 0)}{RESET}")
    print(f"  Monedas           : {YELLOW}{r.get('moneda_premium', r.get('monedas', 0))}{RESET}")
    print(f"  Pociones          : {GREEN}{r.get('pociones', 0)}{RESET} / {r.get('pociones_max', 5)}")
    print(f"  Frag. personaje   : {RED}{r.get('fragmentos_rojos', 0)}{RESET}")
    print(f"  Frag. arma        : {CYAN}{r.get('fragmentos_azules', 0)}{RESET}")


# ═══════════════════════════════════
# MAPA
# ═══════════════════════════════════

def ver_mapa(gm):
    titulo("MAPA")
    mapa = gm.get_mapa()

    for nodo in mapa:
        nid = nodo["nodo_id"]
        estado = nodo["estado"]
        enemigo = nodo.get("enemigo", {})
        nombre = enemigo.get("nombre", "???")
        tipo = enemigo.get("tipo", "basico")

        if estado == "completado":
            icono = f"{GREEN}✅{RESET}"
        elif estado == "disponible":
            icono = f"{YELLOW}⚔️ {RESET}"
        else:
            icono = f"{GRAY}🔒{RESET}"

        tipo_icon = f"{RED}👑{RESET}" if tipo == "jefe" else "  "
        stats = f"ATK:{enemigo.get('atk',0)} DEF:{enemigo.get('defensa',0)} VID:{enemigo.get('vida',0)}"

        print(f"  {icono} Nodo {nid:>2}: {nombre:<22} {tipo_icon} {GRAY}{stats}{RESET}")


# ═══════════════════════════════════
# COMBATE
# ═══════════════════════════════════

def combatir(gm):
    titulo("COMBATE")

    # Mostrar nodos disponibles
    mapa = gm.get_mapa()
    disponibles = [n for n in mapa if n["estado"] in ("disponible", "completado")]

    if not disponibles:
        print(f"  {RED}No hay nodos disponibles.{RESET}")
        return

    print(f"  Nodos disponibles:")
    for n in disponibles:
        enemigo = n.get("enemigo", {})
        print(f"    {n['nodo_id']:>2}. {enemigo.get('nombre', '???')} "
              f"(ATK:{enemigo.get('atk',0)} DEF:{enemigo.get('defensa',0)} VID:{enemigo.get('vida',0)})")

    separador()
    try:
        nodo_id = int(input(f"  {CYAN}Nodo a combatir: {RESET}").strip())
    except ValueError:
        print(f"  {RED}Nodo inválido.{RESET}")
        return

    # Info del jugador
    activo = gm.get_personaje_activo_info()
    if activo:
        print(f"\n  {GREEN}Tu personaje: {activo['nombre']} ({activo['clase']}, {activo['rareza']}){RESET}")
        print(f"  {GRAY}ATK:{activo['atk_base']} DEF:{activo.get('defensa_base',0)} VID:{activo['pv_base']}{RESET}")

    print(f"\n  {YELLOW}Iniciando combate...{RESET}\n")

    resultado = gm.iniciar_combate(nodo_id)

    # Mostrar log completo
    for linea in resultado["log"]:
        print(f"  {linea}")

    print()
    if resultado["victoria"]:
        print(f"  {GREEN}{BOLD}🏆 ¡VICTORIA!{RESET}")
        if resultado["recompensas"]:
            print(f"  Recompensas: {resultado['recompensas']}")
    else:
        print(f"  {RED}{BOLD}💀 DERROTA{RESET}")
        print(f"  {GRAY}Usa una poción para volver a intentarlo.{RESET}")


# ═══════════════════════════════════
# CAMBIAR PERSONAJE
# ═══════════════════════════════════

def cambiar_personaje(gm):
    titulo("CAMBIAR PERSONAJE ACTIVO")

    personajes = gm.get_personajes_jugador()
    if len(personajes) <= 1:
        print(f"  {GRAY}Solo tienes un personaje.{RESET}")
        return

    for i, p in enumerate(personajes, 1):
        col = color_rareza(p["rareza"])
        activo = " ◄ ACTIVO" if p.get("inv_id") == gm.personaje_activo_id else ""
        print(f"  {i}. {col}[{p['rareza']}]{RESET} {p['nombre']} ({p['clase']}){GREEN}{activo}{RESET}")

    separador()
    try:
        idx = int(input(f"  {CYAN}Número del personaje: {RESET}").strip()) - 1
        if 0 <= idx < len(personajes):
            gm.cambiar_personaje_activo(personajes[idx]["inv_id"])
            print(f"  {GREEN}Personaje cambiado a: {personajes[idx]['nombre']}{RESET}")
        else:
            print(f"  {RED}Número inválido.{RESET}")
    except ValueError:
        print(f"  {RED}Entrada inválida.{RESET}")


# ═══════════════════════════════════
# POCIONES
# ═══════════════════════════════════

def usar_pocion(gm):
    if gm.usar_pocion():
        print(f"  {GREEN}Poción usada. Puedes volver a combatir.{RESET}")
    else:
        print(f"  {RED}No tienes pociones.{RESET}")


# ═══════════════════════════════════
# ARRANQUE
# ═══════════════════════════════════

def main():
    limpiar()
    print(f"""
{CYAN}{BOLD}══════════════════════════════════════════{RESET}
{CYAN}{BOLD}  ANOMALÍAS vs GUARDIANES DEL ESPACIO TIEMPO{RESET}
{CYAN}{BOLD}  Demo de consola — TFG{RESET}
{CYAN}{BOLD}══════════════════════════════════════════{RESET}
""")

    # Borrar BD vieja para demo limpia
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "game.db")
    if os.path.exists(db_path):
        os.remove(db_path)

    gm = GameManager()

    print(f"  {BOLD}Elige tu facción:{RESET}")
    print(f"    1. {CYAN}GUARDIANES{RESET} del Espacio Tiempo")
    print(f"    2. {PURPLE}ANOMALÍAS{RESET}")
    separador()

    while True:
        opcion = input(f"  {CYAN}Facción (1/2): {RESET}").strip()
        if opcion == "1":
            gm.iniciar_juego("guardian")
            break
        elif opcion == "2":
            gm.iniciar_juego("anomalia")
            break
        print(f"  {RED}Opción inválida.{RESET}")

    # Dar tickets extra para la demo
    from database.repositories import recursos_repo
    recursos_repo.add_recurso("tickets_personaje", 50)
    recursos_repo.add_recurso("tickets_arma", 30)
    print(f"\n  {GREEN}🎁 Bonus de demo: +50 tickets personaje, +30 tickets arma{RESET}")

    menu_principal(gm)


if __name__ == "__main__":
    main()