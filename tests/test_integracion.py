"""
test_integracion.py — Test end-to-end del flujo completo.

Ejecutar desde la raíz del proyecto:
    python tests/test_integracion.py
"""

import sys, os
_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# ── Colores ──
RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[92m"
RED    = "\033[91m"
CYAN   = "\033[96m"
GRAY   = "\033[90m"

def ok(msg):   print(f"  {GREEN}✅ {msg}{RESET}")
def fail(msg): print(f"  {RED}❌ {msg}{RESET}")
def info(msg): print(f"  {CYAN}ℹ  {msg}{RESET}")
def titulo(msg):
    print(f"\n{CYAN}{'─'*55}{RESET}")
    print(f"{CYAN}{BOLD}  {msg}{RESET}")
    print(f"{CYAN}{'─'*55}{RESET}")

errores = 0


def test_firebase():
    global errores
    titulo("TEST 1 — Firebase / Enemy Loader")

    from firebase.firebase_client import FirebaseClient
    from firebase.enemy_loader import EnemyLoader

    fb = FirebaseClient()
    info(f"Modo: {fb.modo}")

    todos = fb.get_todos_enemigos()
    if len(todos) >= 10:
        ok(f"Cargados {len(todos)} enemigos.")
    else:
        fail(f"Solo {len(todos)} enemigos (esperados ≥10).")
        errores += 1

    e1 = fb.get_enemigo(1)
    if e1 and e1["nombre"] == "Anomalía Alfa":
        ok(f"Nodo 1: {e1['nombre']} (ATK:{e1['atk']} DEF:{e1['defensa']} VID:{e1['vida']})")
    else:
        fail(f"Nodo 1 incorrecto: {e1}")
        errores += 1

    e5 = fb.get_enemigo(5)
    if e5 and e5["tipo"] == "jefe":
        ok(f"Nodo 5 (jefe): {e5['nombre']}")
    else:
        fail(f"Nodo 5 no es jefe: {e5}")
        errores += 1

    loader = EnemyLoader(fb)
    enemigo = loader.crear_enemigo(3)
    if enemigo is not None:
        ok(f"Enemigo creado: {enemigo.nombre} ({enemigo.__class__.__name__})")
    else:
        fail("No se pudo crear enemigo del nodo 3.")
        errores += 1

    jefe = loader.crear_enemigo(5)
    if jefe is not None and jefe.__class__.__name__ == "EnemigoJefe":
        ok(f"Jefe creado: {jefe.nombre} ({jefe.__class__.__name__})")
    else:
        fail("No se pudo crear jefe del nodo 5.")
        errores += 1


def test_game_manager():
    global errores
    titulo("TEST 2 — GameManager (integración)")

    db_path = os.path.join(_ROOT, "data", "game.db")
    if os.path.exists(db_path):
        os.remove(db_path)
        info("BD anterior eliminada para test limpio.")

    from firebase.game_manager import GameManager
    gm = GameManager()

    gm.iniciar_juego("guardian")
    if gm.faccion == "guardian":
        ok(f"Facción: {gm.faccion}")
    else:
        fail(f"Facción incorrecta: {gm.faccion}")
        errores += 1

    activo = gm.get_personaje_activo_info()
    if activo:
        ok(f"Personaje activo: {activo['nombre']} ({activo['clase']}, {activo['rareza']})")
    else:
        fail("No hay personaje activo.")
        errores += 1

    recursos = gm.get_recursos()
    if recursos:
        ok(f"Recursos: {recursos.get('tickets_personaje', 0)} tickets pers., "
           f"{recursos.get('tickets_arma', 0)} tickets arma")
    else:
        fail("No se pudieron obtener recursos.")
        errores += 1

    return gm


def test_gacha(gm):
    global errores
    titulo("TEST 3 — Gacha")

    from database.repositories import recursos_repo
    recursos_repo.add_recurso("tickets_personaje", 20)
    info("Añadidos 20 tickets de personaje para test.")

    for i in range(5):
        r = gm.tirar_gacha("personajes")
        if "error" in r:
            fail(f"Pull {i+1}: {r['error']}")
            errores += 1
        else:
            rareza = r.get("rareza", "?")
            nombre = r.get("item", {}).get("nombre", "???")
            nuevo = "★ nuevo" if r.get("es_nuevo") else "↩ duplicado"
            pity = r.get("pity_count", 0)
            print(f"    Pull {i+1}: [{rareza}] {nombre:<28} {nuevo} (pity: {pity})")

    personajes = gm.get_personajes_jugador()
    ok(f"Personajes en inventario: {len(personajes)}")
    for p in personajes:
        print(f"      - {p['nombre']} ({p['clase']}, {p['rareza']})")


def test_combate(gm):
    global errores
    titulo("TEST 4 — Combate (nodo 1)")

    resultado = gm.iniciar_combate(1)

    if resultado["log"]:
        ok(f"Combate ejecutado. Log: {len(resultado['log'])} líneas.")
        for linea in resultado["log"][-5:]:
            print(f"    {GRAY}{linea}{RESET}")
    else:
        fail("Combate sin log.")
        errores += 1

    if resultado["victoria"]:
        ok(f"Victoria. Recompensas: {resultado['recompensas']}")
    else:
        info("Derrota (puede ser normal con personaje B vs nodo 1).")

    ok("Combate terminó sin bucle infinito.")


def test_mapa(gm):
    global errores
    titulo("TEST 5 — Mapa")

    mapa = gm.get_mapa()
    if len(mapa) >= 10:
        ok(f"Mapa con {len(mapa)} nodos.")
    else:
        fail(f"Solo {len(mapa)} nodos (esperados ≥10).")
        errores += 1

    for nodo in mapa[:5]:
        enemigo_nombre = nodo.get("enemigo", {}).get("nombre", "Sin enemigo")
        print(f"    Nodo {nodo['nodo_id']:>2}: {nodo['estado']:<12} → {enemigo_nombre}")


def main():
    global errores
    print(f"\n{'='*55}")
    print(f"{BOLD}  TEST DE INTEGRACIÓN — Anomalías vs Guardianes{RESET}")
    print(f"{'='*55}")

    test_firebase()
    gm = test_game_manager()
    test_gacha(gm)
    test_combate(gm)
    test_mapa(gm)

    titulo("RESUMEN")
    if errores == 0:
        print(f"  {GREEN}{BOLD}TODOS LOS TESTS PASARON ✅{RESET}")
    else:
        print(f"  {RED}{BOLD}{errores} ERROR(ES) DETECTADO(S) ❌{RESET}")
    print()

if __name__ == "__main__":
    main()