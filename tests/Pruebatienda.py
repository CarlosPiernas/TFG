"""
Prueba de Tienda y RecompensaNodo.
Simula una run completa: completar nodos, cobrar recompensas, comprar en tienda, usar tickets.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.Almacenamiento.DatosJugador import DatosJugador
from logic.Almacenamiento.Tienda import Tienda
from logic.Almacenamiento.RecompensaNodo import RecompensaNodo
from logic.Almacenamiento.Mochila import Mochila


def separador(titulo):
    print(f"\n{'═' * 60}")
    print(f"  {titulo}")
    print(f"{'═' * 60}")


def test_run_completa():
    separador("SIMULACIÓN DE RUN COMPLETA")

    datos = DatosJugador("TestPlayer")
    tienda = Tienda(datos)
    mochila = Mochila(datos)

    print(f"\n  Estado inicial:")
    print(f"    Monedas: {datos.monedas}")
    print(f"    Pociones: {datos.pociones}")
    print(f"    Tickets pers: {datos.tickets_personaje}")
    print(f"    Tickets arma: {datos.tickets_arma}")

    # ── Completar los 10 nodos y cobrar recompensas ──
    print(f"\n  {'─' * 50}")
    print(f"  COMPLETANDO 10 NODOS")
    print(f"  {'─' * 50}")

    for nodo in range(1, 11):
        print(f"\n  Nodo {nodo} ({RecompensaNodo.resumen_recompensas(nodo)}):")
        log = RecompensaNodo.aplicar(datos, nodo)
        for linea in log:
            print(f"    {linea}")

    # ── Estado tras 10 nodos ──
    print(f"\n  {'─' * 50}")
    print(f"  ESTADO TRAS COMPLETAR RUN")
    print(f"  {'─' * 50}")
    print(f"    Monedas: {datos.monedas}")
    print(f"    Pociones: {datos.pociones}")
    print(f"    Transmutadores: {datos.transmutadores}")
    print(f"    Tickets personaje: {datos.tickets_personaje}")
    print(f"    Tickets arma: {datos.tickets_arma}")
    print(f"    Runas: {datos.runas}")

    # ── Comprar pociones en tienda ──
    print(f"\n  {'─' * 50}")
    print(f"  COMPRANDO 8 POCIONES EN TIENDA")
    print(f"  {'─' * 50}")
    for i in range(8):
        r = tienda.comprar_pocion()
        if i == 0 or i == 7:
            print(f"    {r['mensaje']}")
        elif i == 1:
            print(f"    ... (comprando 6 más) ...")

    # ── Comprar tickets ──
    print(f"\n  {'─' * 50}")
    print(f"  COMPRANDO TICKETS")
    print(f"  {'─' * 50}")
    print(f"    Monedas disponibles: {datos.monedas}")
    print(f"    Precios: {tienda.precios()}")
    print(f"    Puede comprar: {tienda.puede_comprar()}")

    # Comprar tickets de personaje mientras pueda
    while datos.monedas >= 200:
        r = tienda.comprar_ticket_personaje()
        print(f"    {r['mensaje']}")

    # Comprar tickets de arma mientras pueda
    while datos.monedas >= 150:
        r = tienda.comprar_ticket_arma()
        print(f"    {r['mensaje']}")

    # Comprar transmutador si puede
    while datos.monedas >= 100:
        r = tienda.comprar_transmutador()
        print(f"    {r['mensaje']}")

    print(f"    Monedas restantes: {datos.monedas}")

    # ── Usar tickets de personaje ──
    print(f"\n  {'─' * 50}")
    print(f"  USANDO TICKETS DE PERSONAJE ({datos.tickets_personaje})")
    print(f"  {'─' * 50}")

    while datos.tickets_personaje > 0:
        r = tienda.usar_ticket_personaje()
        print(f"    {r['mensaje']}")

    # ── Usar tickets de arma ──
    print(f"\n  {'─' * 50}")
    print(f"  USANDO TICKETS DE ARMA ({datos.tickets_arma})")
    print(f"  {'─' * 50}")

    while datos.tickets_arma > 0:
        r = tienda.usar_ticket_arma()
        print(f"    {r['mensaje']}")

    # ── Estado final ──
    print(f"\n  {'─' * 50}")
    print(f"  INVENTARIO FINAL")
    print(f"  {'─' * 50}")
    consumibles = mochila.ver_consumibles()
    for clave, valor in consumibles.items():
        print(f"    {clave}: {valor}")

    print(f"\n  Personajes desbloqueados:")
    for p in mochila.listar_personajes():
        print(f"    {p['nombre']} — {p['clase']} ({p['rareza']}) [{p['faccion']}]")

    print(f"\n  Armas desbloqueadas:")
    for a in mochila.listar_armas():
        print(f"    {a['nombre']} — {a['tipo']} ({a['clase']})")

    print(f"\n  Runas:")
    for r in mochila.listar_runas():
        stats_str = ", ".join(f"{k}: {v:+d}" for k, v in r['stats'].items())
        print(f"    {r['nombre']} ×{r['cantidad']} — {stats_str}")

    print(f"\n  Fragmentos: rojos={datos.fragmentos_personaje}, azules={datos.fragmentos_arma}")
    print(f"  Resumen: {mochila.resumen()}")


def test_tienda_sin_monedas():
    separador("TEST: TIENDA SIN MONEDAS")
    datos = DatosJugador("Pobre")
    tienda = Tienda(datos)

    r = tienda.comprar_pocion()
    print(f"  Poción: {r['mensaje']}")
    r = tienda.comprar_ticket_personaje()
    print(f"  Ticket pers: {r['mensaje']}")
    r = tienda.comprar_ticket_arma()
    print(f"  Ticket arma: {r['mensaje']}")
    r = tienda.comprar_transmutador()
    print(f"  Transmutador: {r['mensaje']}")


def test_tickets_sin_stock():
    separador("TEST: USAR TICKET SIN TENERLO")
    datos = DatosJugador("SinTickets")
    tienda = Tienda(datos)

    r = tienda.usar_ticket_personaje()
    print(f"  Ticket pers: {r['mensaje']}")
    r = tienda.usar_ticket_arma()
    print(f"  Ticket arma: {r['mensaje']}")


def test_fragmentos_por_duplicados():
    separador("TEST: ACUMULACIÓN DE FRAGMENTOS POR DUPLICADOS")
    datos = DatosJugador("Gacha")
    tienda = Tienda(datos)

    # Dar muchas monedas y comprar muchos tickets
    datos.monedas = 5000
    for _ in range(20):
        tienda.comprar_ticket_personaje()

    print(f"  Tras comprar 20 tickets de personaje:")
    print(f"    Tickets: {datos.tickets_personaje}")

    # Usar todos
    nuevos = 0
    duplicados = 0
    while datos.tickets_personaje > 0:
        r = tienda.usar_ticket_personaje()
        if r["es_nuevo"]:
            nuevos += 1
        else:
            duplicados += 1

    print(f"    Nuevos: {nuevos}, Duplicados: {duplicados}")
    print(f"    Fragmentos rojos: {datos.fragmentos_personaje}")
    print(f"    Personajes: {len(datos.personajes_desbloqueados)}/12")

    # Si puede canjear fragmentos
    if datos.puede_canjear_personaje():
        from logic.Clases.stat import PERSONAJES
        for nombre in PERSONAJES:
            if not datos.tiene_personaje(nombre):
                datos.canjear_fragmentos_personaje(nombre)
                print(f"    Canjeado con fragmentos: {nombre}")
                break


if __name__ == "__main__":
    test_run_completa()
    test_tienda_sin_monedas()
    test_tickets_sin_stock()
    test_fragmentos_por_duplicados()