"""
Prueba del sistema Almacenamiento: DatosJugador + Mochila + Forja.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.Almacenamiento.DatosJugador import DatosJugador
from logic.Almacenamiento.Mochila import Mochila
from logic.Almacenamiento.Forja import Forja


def separador(titulo):
    print(f"\n{'═' * 60}")
    print(f"  {titulo}")
    print(f"{'═' * 60}")


def test_mochila_vacia():
    separador("TEST: MOCHILA VACÍA")
    datos = DatosJugador("TestPlayer")
    mochila = Mochila(datos)

    print(f"  Personajes: {mochila.listar_personajes()}")
    print(f"  Armas:      {mochila.listar_armas()}")
    print(f"  Runas:      {mochila.listar_runas()}")
    print(f"  Consumibles: {mochila.ver_consumibles()}")
    print(f"  Resumen:    {mochila.resumen()}")


def test_mochila_con_datos():
    separador("TEST: MOCHILA CON DATOS")
    datos = DatosJugador("HeroTest")

    # Desbloquear cosas
    datos.desbloquear_personaje("Nombre1")
    datos.desbloquear_personaje("Nombre5")
    datos.desbloquear_personaje("Nombre6")
    datos.desbloquear_arma("Mandoble")
    datos.desbloquear_arma("Mandoble_Cronos")
    datos.agregar_runa("ATAQUE", 3)
    datos.agregar_runa("DEFENSA", 2)
    datos.agregar_runa("ACERO", 1)
    datos.monedas = 500
    datos.pociones = 5
    datos.transmutadores = 2
    datos.tickets_personaje = 1
    datos.fragmentos_personaje = 7

    mochila = Mochila(datos)

    # ── Pestaña Personajes ──
    print("\n  📋 PESTAÑA PERSONAJES:")
    for p in mochila.listar_personajes():
        print(f"    {p['nombre']} — {p['clase']} ({p['rareza']}) [{p['faccion']}]")

    # Seleccionar uno para ver detalle
    detalle = mochila.ver_personaje("Nombre5")
    if detalle:
        print(f"\n  🔍 Detalle de {detalle['nombre']}:")
        print(f"    Clase: {detalle['clase']}, Rareza: {detalle['rareza']}")
        print(f"    Stats: {detalle['stats']}")
        print(f"    Lore: {detalle['lore']}")

    # ── Pestaña Armas ──
    print("\n  ⚔️  PESTAÑA ARMAS:")
    for a in mochila.listar_armas():
        print(f"    {a['nombre']} — {a['tipo']} ({a['clase']})")

    detalle_arma = mochila.ver_arma("Mandoble_Cronos")
    if detalle_arma:
        print(f"\n  🔍 Detalle de {detalle_arma['nombre']}:")
        print(f"    Stats: {detalle_arma['stats']}")
        print(f"    Lore: {detalle_arma['lore']}")

    # ── Pestaña Runas ──
    print("\n  🔮 PESTAÑA RUNAS:")
    for r in mochila.listar_runas():
        stats_str = ", ".join(f"{k}: {v:+d}" for k, v in r['stats'].items())
        print(f"    {r['nombre']} ×{r['cantidad']} ({r['tipo']}) — {stats_str}")

    # ── Pestaña Consumibles ──
    print("\n  🎒 PESTAÑA CONSUMIBLES:")
    cons = mochila.ver_consumibles()
    for clave, valor in cons.items():
        print(f"    {clave}: {valor}")


def test_forja_valida():
    separador("TEST: FORJA — COMBINACIÓN VÁLIDA")
    datos = DatosJugador("Herrero")
    datos.agregar_runa("ATAQUE", 2)
    datos.agregar_runa("DEFENSA", 1)
    datos.agregar_transmutadores(1)

    forja = Forja(datos)

    # Ver runas disponibles
    print(f"  Runas disponibles: {forja.runas_disponibles()}")
    print(f"  Transmutadores: {datos.transmutadores}")

    # Colocar runas
    r1 = forja.colocar_runa(1, "ATAQUE")
    print(f"  Slot 1: {r1['mensaje']}")
    r2 = forja.colocar_runa(2, "DEFENSA")
    print(f"  Slot 2: {r2['mensaje']}")

    # Previsualizar
    prev = forja.previsualizar()
    print(f"  Previsualización: {prev['nombre']} — válida: {prev['es_valida']}")

    # Estado de la forja
    estado = forja.estado()
    print(f"  Puede transmutar: {estado['puede_transmutar']}")

    # Transmutar
    resultado = forja.transmutar()
    print(f"  {resultado['mensaje']}")
    print(f"  Inventario runas: {datos.runas}")


def test_forja_invalida():
    separador("TEST: FORJA — COMBINACIÓN INVÁLIDA → RUNA ROTA")
    datos = DatosJugador("Imprudente")
    datos.agregar_runa("ATAQUE", 1)
    datos.agregar_runa("MAGIA", 1)
    datos.agregar_transmutadores(1)

    forja = Forja(datos)

    forja.colocar_runa(1, "ATAQUE")
    forja.colocar_runa(2, "MAGIA")

    # Previsualizar
    prev = forja.previsualizar()
    print(f"  Previsualización: {prev['nombre']} — válida: {prev['es_valida']}")
    print(f"  ⚠️  {prev['descripcion']}")

    # Transmutar igual (jugador decide arriesgarse)
    resultado = forja.transmutar()
    print(f"  {resultado['mensaje']}")
    print(f"  Inventario runas: {datos.runas}")


def test_forja_sin_recursos():
    separador("TEST: FORJA — SIN RECURSOS")
    datos = DatosJugador("SinNada")

    forja = Forja(datos)

    # Sin runas
    r = forja.colocar_runa(1, "ATAQUE")
    print(f"  Sin runas: {r['mensaje']}")

    # Con runas pero sin transmutador
    datos.agregar_runa("ATAQUE", 1)
    datos.agregar_runa("DEFENSA", 1)
    forja.colocar_runa(1, "ATAQUE")
    forja.colocar_runa(2, "DEFENSA")
    r = forja.transmutar()
    print(f"  Sin transmutador: {r['mensaje']}")


def test_forja_todas_combinaciones():
    separador("TEST: TODAS LAS COMBINACIONES DE LA FORJA")
    basicas = ["ATAQUE", "DEFENSA", "DESTREZA", "MAGIA"]

    for i, r1 in enumerate(basicas):
        for r2 in basicas[i+1:]:
            datos = DatosJugador("Test")
            datos.agregar_runa(r1, 1)
            datos.agregar_runa(r2, 1)
            datos.agregar_transmutadores(1)

            forja = Forja(datos)
            forja.colocar_runa(1, r1)
            forja.colocar_runa(2, r2)
            resultado = forja.transmutar()

            res = resultado["resultado"]
            marca = "✅" if res["es_valida"] else "❌"
            stats_str = ", ".join(f"{k}:{v:+d}" for k, v in res["stats"].items())
            print(f"  {marca} {r1:>10} + {r2:<10} = {res['nombre']:<10} ({stats_str})")


if __name__ == "__main__":
    test_mochila_vacia()
    test_mochila_con_datos()
    test_forja_valida()
    test_forja_invalida()
    test_forja_sin_recursos()
    test_forja_todas_combinaciones()