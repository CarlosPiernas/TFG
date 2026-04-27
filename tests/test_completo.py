"""
test_completo.py — Suite de tests completa para Anomalías vs Guardianes
Cubre todas las casuísticas del backend sin necesidad de levantar Kivy.
Ejecutar desde la raíz del proyecto:
    python tests/test_completo.py
"""

import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Setup: BD limpia antes de empezar ───────────────────────────────────────
db_path = os.path.join(os.path.dirname(__file__), "..", "data", "game.db")
if os.path.exists(db_path):
    os.remove(db_path)

from database.db_manager import initialize_db, get_connection
from database.seed import run_seed
initialize_db()
run_seed()

from database.repositories import (
    personaje_repo, arma_repo, runa_repo,
    inventario_repo, recursos_repo, pity_repo,
)
from database.repositories.mapa_repo import MapaRepo
from database.repositories.equipamiento_repo import EquipamientoRepo
from firebase.game_manager import GameManager

# ── Contadores globales ──────────────────────────────────────────────────────
_ok   = 0
_fail = 0


def ok(nombre):
    global _ok
    _ok += 1
    print(f"  ✅ {nombre}")


def falla(nombre, detalle=""):
    global _fail
    _fail += 1
    print(f"  ❌ {nombre}" + (f" — {detalle}" if detalle else ""))


def seccion(titulo):
    print(f"\n{'─'*55}")
    print(f"  {titulo}")
    print(f"{'─'*55}")


# ════════════════════════════════════════════════════════
# 1. BASE DE DATOS — SEED Y CATÁLOGOS
# ════════════════════════════════════════════════════════
seccion("1. SEED Y CATÁLOGOS")

personajes = personaje_repo.get_catalogo()
if len(personajes) == 12:
    ok("12 personajes en catálogo")
else:
    falla("12 personajes en catálogo", f"hay {len(personajes)}")

guardianes = personaje_repo.get_by_faccion("guardian")
anomalias  = personaje_repo.get_by_faccion("anomalia")
if len(guardianes) == 6:
    ok("6 guardianes")
else:
    falla("6 guardianes", f"hay {len(guardianes)}")

if len(anomalias) == 6:
    ok("6 anomalías")
else:
    falla("6 anomalías", f"hay {len(anomalias)}")

armas = arma_repo.get_catalogo()
if len(armas) == 6:
    ok("6 armas en catálogo (3 básicas + 3 S)")
else:
    falla("6 armas en catálogo", f"hay {len(armas)}")

runas = runa_repo.get_catalogo()
if len(runas) == 10:
    ok("10 runas en catálogo (4 básicas + 5 mixtas + 1 rota)")
else:
    falla("10 runas en catálogo", f"hay {len(runas)}")

recursos = recursos_repo.get_recursos()
if recursos and recursos.get("pociones") == 5:
    ok("Recursos iniciales correctos (5 pociones)")
else:
    falla("Recursos iniciales", str(recursos))

mapa_repo = MapaRepo()
nodos = mapa_repo.get_todos_nodos()
if len(nodos) == 10:
    ok("10 nodos en el mapa")
else:
    falla("10 nodos en el mapa", f"hay {len(nodos)}")

nodo1 = mapa_repo.get_nodo(1)
if nodo1 and nodo1["estado"] == "disponible":
    ok("Nodo 1 disponible al inicio")
else:
    falla("Nodo 1 disponible", str(nodo1))

nodo2 = mapa_repo.get_nodo(2)
if nodo2 and nodo2["estado"] == "bloqueado":
    ok("Nodo 2 bloqueado al inicio")
else:
    falla("Nodo 2 bloqueado", str(nodo2))


# ════════════════════════════════════════════════════════
# 2. GAME MANAGER — INICIO DE JUEGO
# ════════════════════════════════════════════════════════
seccion("2. GAME MANAGER — INICIO DE JUEGO")

gm = GameManager()

if gm.faccion is None:
    ok("GameManager arranca sin facción (primera vez)")
else:
    falla("GameManager sin facción inicial", f"tiene {gm.faccion}")

# Guardianes
gm.iniciar_juego("GUARDIANES")
if gm.faccion == "guardian":
    ok("Facción normalizada correctamente: GUARDIANES → guardian")
else:
    falla("Normalización facción", f"resultado: {gm.faccion}")

if gm.personaje_activo_id is not None:
    ok("Personaje activo asignado tras iniciar_juego")
else:
    falla("Personaje activo asignado")

# Intentar cambiar facción (debe ignorarse)
gm.iniciar_juego("ANOMALÍAS")
if gm.faccion == "guardian":
    ok("No se puede cambiar facción una vez elegida")
else:
    falla("Facción no cambia", f"cambió a {gm.faccion}")

info = gm.get_personaje_activo_info()
if info and info.get("faccion") == "guardian":
    ok(f"Personaje activo es de facción guardian: {info['nombre']}")
else:
    falla("Personaje activo facción correcta", str(info))

# Persistencia de facción en BD
faccion_bd = recursos_repo.get_recursos().get("faccion")
if faccion_bd == "guardian":
    ok("Facción persiste en BD")
else:
    falla("Facción persiste en BD", f"valor: {faccion_bd}")


# ════════════════════════════════════════════════════════
# 3. INVENTARIO
# ════════════════════════════════════════════════════════
seccion("3. INVENTARIO")

personajes_jugador = gm.get_personajes_jugador()
if len(personajes_jugador) == 1:
    ok("Jugador empieza con 1 personaje")
else:
    falla("1 personaje inicial", f"hay {len(personajes_jugador)}")

armas_jugador = gm.get_armas_jugador()
if len(armas_jugador) == 0:
    ok("Jugador empieza sin armas")
else:
    falla("Sin armas iniciales", f"hay {len(armas_jugador)}")

# Añadir ítem y verificar duplicado
arma_b = arma_repo.get_by_rareza("B")[0]
es_nuevo = inventario_repo.agregar_item(1, arma_b["id"], "arma")
if es_nuevo:
    ok("Añadir arma nueva al inventario")
else:
    falla("Añadir arma nueva")

es_duplicado = inventario_repo.agregar_item(1, arma_b["id"], "arma")
if not es_duplicado:
    ok("Detecta duplicado correctamente")
else:
    falla("Detección de duplicado")

armas_jugador = gm.get_armas_jugador()
if len(armas_jugador) == 1:
    ok("Inventario de armas actualizado")
else:
    falla("Inventario armas", f"hay {len(armas_jugador)}")


# ════════════════════════════════════════════════════════
# 4. EQUIPAMIENTO
# ════════════════════════════════════════════════════════
seccion("4. EQUIPAMIENTO")

equip_repo = EquipamientoRepo()
arma_inv = gm.get_armas_jugador()[0]

resultado = gm.equipar_arma(arma_inv["inv_id"])
if resultado.get("ok"):
    ok("Equipar arma al personaje activo")
else:
    falla("Equipar arma", str(resultado))

equipo = equip_repo.get_equipo_de_personaje(gm.personaje_activo_id)
armas_equipadas = [e for e in equipo if e.get("slot") == "arma"]
if len(armas_equipadas) == 1:
    ok("Arma aparece en el equipo")
else:
    falla("Arma en equipo", str(equipo))

# Añadir una runa y equiparla
runa_cat = runa_repo.get_by_rareza("basica")[0]
inventario_repo.agregar_item(1, runa_cat["id"], "runa")
runas_jugador = gm.get_runas_jugador()
if runas_jugador:
    resultado_runa = gm.equipar_runa(runas_jugador[0]["inv_id"], 1)
    if resultado_runa.get("ok"):
        ok("Equipar runa en slot 1")
    else:
        falla("Equipar runa", str(resultado_runa))
else:
    falla("No hay runas para equipar")

# Cambiar personaje activo
personaje2_id = gm.get_personajes_jugador()[0]["inv_id"]
gm.cambiar_personaje_activo(personaje2_id)
if gm.personaje_activo_id == personaje2_id:
    ok("Cambio de personaje activo")
else:
    falla("Cambio personaje activo")


# ════════════════════════════════════════════════════════
# 5. PITY Y GACHA
# ════════════════════════════════════════════════════════
seccion("5. PITY Y GACHA")

# Verificar pity inicial
pity = pity_repo.get_pity(1, "personajes")
if pity and pity.get("pity_count") == 0:
    ok("Pity inicial en 0")
else:
    falla("Pity inicial", str(pity))

# Tirar gacha (tenemos 10 tickets de personaje del seed)
resultado_gacha = gm.tirar_gacha("personajes")
if "error" not in resultado_gacha:
    ok(f"Tirada gacha exitosa — rareza: {resultado_gacha.get('rareza')}")
else:
    falla("Tirada gacha", str(resultado_gacha))

pity_tras_tirada = pity_repo.get_pity(1, "personajes")
if pity_tras_tirada:
    rareza = resultado_gacha.get("rareza")
    contador_esperado = 0 if rareza == "S" else 1
    if pity_tras_tirada["pity_count"] == contador_esperado:
        ok("Contador pity actualizado correctamente")
    else:
        falla("Contador pity", f"esperado {contador_esperado}, hay {pity_tras_tirada['pity_count']}")

# Forzar pity duro (simular 5 tiradas sin S)
from database.config import GACHA_MODE
from logic.gacha import HARD_PITY_SIMPLE, HARD_PITY_GENSHIN
limite = HARD_PITY_SIMPLE if GACHA_MODE == "simple" else HARD_PITY_GENSHIN

# Forzar exactamente en el límite — la siguiente tirada DEBE ser S
pity_repo.actualizar_pity(1, "personajes", limite)
resultado_pity = gm.tirar_gacha("personajes")
if resultado_pity.get("rareza") == "S":
    ok(f"Pity duro funciona — S garantizado en tirada {limite}")
else:
    falla("Pity duro", f"salió {resultado_pity.get('rareza')}")

# Tirada sin tickets
recursos_repo.add_recurso("tickets_personaje", -999)  # vaciar
resultado_sin_ticket = gm.tirar_gacha("personajes")
if resultado_sin_ticket.get("error") == "tickets_insuficientes":
    ok("Error correcto con tickets insuficientes")
else:
    falla("Error tickets insuficientes", str(resultado_sin_ticket))

# Restaurar tickets
recursos_repo.add_recurso("tickets_personaje", 10)

# Gacha banner armas
resultado_arma = gm.tirar_gacha("armas")
if "error" not in resultado_arma:
    ok(f"Gacha banner armas funciona — rareza: {resultado_arma.get('rareza')}")
else:
    falla("Gacha banner armas", str(resultado_arma))

# Facción Anomalía — nuevo GameManager
db_path2 = os.path.join(os.path.dirname(__file__), "..", "data", "game_anomalia.db")
# Usamos mismo gm pero verificamos pool anomalía directamente
pool = personaje_repo.get_by_rareza_y_faccion("B", "anomalia")
if pool:
    ok("Pool anomalías no vacío para rareza B")
else:
    falla("Pool anomalías rareza B vacío")

pool_s = personaje_repo.get_by_rareza_y_faccion("S", "guardian")
if pool_s:
    ok("Pool guardianes no vacío para rareza S")
else:
    falla("Pool guardianes rareza S vacío")


# ════════════════════════════════════════════════════════
# 6. COMBATE
# ════════════════════════════════════════════════════════
seccion("6. COMBATE")

gm.nodo_seleccionado = 1
resultado_combate = gm.iniciar_combate(1)

if "victoria" in resultado_combate:
    ok("Combate retorna resultado")
else:
    falla("Combate retorna resultado", str(resultado_combate))

if isinstance(resultado_combate.get("log"), list) and len(resultado_combate["log"]) > 0:
    ok("Log de combate generado")
else:
    falla("Log de combate", str(resultado_combate.get("log")))

# Combate con personaje activo sin equipo (debe funcionar igual)
resultado_combate2 = gm.iniciar_combate(1)
if "victoria" in resultado_combate2:
    ok("Combate funciona sin equipo equipado")
else:
    falla("Combate sin equipo", str(resultado_combate2))

# Nodo bloqueado
# Usar nodo 3 que nunca se ha tocado
resultado_bloqueado = gm.iniciar_combate(3)
if not resultado_bloqueado.get("victoria") and "bloqueado" in str(resultado_bloqueado.get("log", [])).lower():
    ok("Nodo bloqueado devuelve error correcto")
else:
    falla("Nodo bloqueado", str(resultado_bloqueado))

# Nodo inexistente
resultado_inexistente = gm.iniciar_combate(99)
if not resultado_inexistente.get("victoria"):
    ok("Nodo inexistente devuelve error")
else:
    falla("Nodo inexistente", str(resultado_inexistente))

# Victoria desbloquea nodo siguiente
if resultado_combate.get("victoria"):
    nodo2_tras_victoria = mapa_repo.get_nodo(2)
    if nodo2_tras_victoria and nodo2_tras_victoria["estado"] in ("disponible", "completado"):
        ok("Victoria desbloquea nodo siguiente")
    else:
        falla("Victoria desbloquea nodo 2", str(nodo2_tras_victoria))

# Recompensas
recompensas = resultado_combate.get("recompensas")
if recompensas and "monedas" in recompensas:
    ok(f"Recompensas incluyen monedas: {recompensas['monedas']}")
else:
    falla("Recompensas con monedas", str(recompensas))


# ════════════════════════════════════════════════════════
# 7. MAPA
# ════════════════════════════════════════════════════════
seccion("7. MAPA")

mapa = gm.get_mapa()
if len(mapa) == 10:
    ok("get_mapa devuelve 10 nodos")
else:
    falla("get_mapa 10 nodos", f"hay {len(mapa)}")

nodo_info = gm.get_nodo(1)
if nodo_info and "nodo_id" in nodo_info:
    ok("get_nodo devuelve info correcta")
else:
    falla("get_nodo", str(nodo_info))

# Completar nodo y verificar estrellas
mapa_repo.completar_nodo(1, estrellas=1)
nodo_completado = mapa_repo.get_nodo(1)
if nodo_completado and nodo_completado["estado"] == "completado":
    ok("Nodo marcado como completado")
else:
    falla("Nodo completado", str(nodo_completado))


# ════════════════════════════════════════════════════════
# 8. RECURSOS Y POCIONES
# ════════════════════════════════════════════════════════
seccion("8. RECURSOS Y POCIONES")

recursos_actuales = gm.get_recursos()
if recursos_actuales:
    ok("get_recursos devuelve datos")
else:
    falla("get_recursos")

# Consumir poción
pociones_antes = recursos_actuales.get("pociones", 0)
resultado_pocion = gm.usar_pocion()
pociones_despues = recursos_repo.get_recursos().get("pociones", 0)

if resultado_pocion and pociones_despues == pociones_antes - 1:
    ok("Consumir poción reduce en 1")
else:
    falla("Consumir poción", f"antes={pociones_antes}, después={pociones_despues}")

# Sin pociones
recursos_repo.add_recurso("pociones", -999)
resultado_sin_pocion = gm.usar_pocion()
if not resultado_sin_pocion:
    ok("Usar poción sin stock devuelve False")
else:
    falla("Sin pociones devuelve False")
recursos_repo.add_recurso("pociones", 5)

# add_recurso — monedas
monedas_antes = gm.get_recursos().get("monedas", 0)
recursos_repo.add_recurso("monedas", 100)
monedas_despues = gm.get_recursos().get("monedas", 0)
if monedas_despues == monedas_antes + 100:
    ok("add_recurso monedas funciona")
else:
    falla("add_recurso monedas", f"{monedas_antes} → {monedas_despues}")

# Transmutadores
recursos_repo.add_recurso("transmutadores", 3)
transmutadores = gm.get_transmutadores()
if transmutadores >= 3:
    ok("get_transmutadores funciona")
else:
    falla("get_transmutadores", f"valor: {transmutadores}")

consumido = recursos_repo.consumir_transmutador()
if consumido:
    ok("consumir_transmutador funciona")
else:
    falla("consumir_transmutador")


# ════════════════════════════════════════════════════════
# 9. FORJA / TRANSMUTACIÓN
# ════════════════════════════════════════════════════════
seccion("9. FORJA / TRANSMUTACIÓN")

# Añadir runas básicas al inventario para poder transmutar
runa_ataque  = runa_repo.get_by_nombre("RUNA_ATAQUE")
runa_defensa = runa_repo.get_by_nombre("RUNA_DEFENSA")

if runa_ataque:
    inventario_repo.agregar_item(1, runa_ataque["id"], "runa")
    ok("RUNA_ATAQUE encontrada en catálogo")
else:
    falla("RUNA_ATAQUE en catálogo")

if runa_defensa:
    inventario_repo.agregar_item(1, runa_defensa["id"], "runa")
    ok("RUNA_DEFENSA encontrada en catálogo")
else:
    falla("RUNA_DEFENSA en catálogo")

# get_runas_basicas_jugador
runas_basicas = gm.get_runas_basicas_jugador()
nombres_basicas = [r["nombre"] for r in runas_basicas]
if "RUNA_ATAQUE" in nombres_basicas or "RUNA_DEFENSA" in nombres_basicas:
    ok(f"get_runas_basicas_jugador devuelve runas: {nombres_basicas}")
else:
    falla("get_runas_basicas_jugador", str(nombres_basicas))

# Transmutar sin transmutadores
recursos_repo.consumir_transmutador()
recursos_repo.consumir_transmutador()
recursos_repo.consumir_transmutador()
# Aseguramos 0 transmutadores
conn = get_connection()
conn.execute("UPDATE recursos_jugador SET transmutadores = 0 WHERE id = 1")
conn.commit()
conn.close()

resultado_sin_trans = gm.transmutar("RUNA_ATAQUE", "RUNA_DEFENSA")
if not resultado_sin_trans.get("ok"):
    ok("Transmutar sin transmutadores devuelve error")
else:
    falla("Error sin transmutadores", str(resultado_sin_trans))

# Transmutar con transmutadores
recursos_repo.add_recurso("transmutadores", 2)

resultado_transmutacion = gm.transmutar("RUNA_ATAQUE", "RUNA_DEFENSA")
if resultado_transmutacion.get("ok"):
    ok(f"Transmutación exitosa — resultado: {resultado_transmutacion.get('resultado', {}).get('nombre', '?')}")
else:
    falla("Transmutación", str(resultado_transmutacion))

# Verificar que la runa resultado está en el inventario
runas_inv = gm.get_runas_jugador()
nombres_inv = [r["nombre"] for r in runas_inv]
if "RUNA_ACERO" in nombres_inv:
    ok("RUNA_ACERO en inventario tras transmutación")
else:
    falla("RUNA_ACERO en inventario", str(nombres_inv))

# Transmutar combinación inválida (ATAQUE + MAGIA = ROTA)
runa_magia = runa_repo.get_by_nombre("RUNA_MAGIA")
runa_ataque2 = runa_repo.get_by_nombre("RUNA_ATAQUE")
if runa_magia and runa_ataque2:
    inventario_repo.agregar_item(1, runa_magia["id"], "runa")
    inventario_repo.agregar_item(1, runa_ataque2["id"], "runa")
    recursos_repo.add_recurso("transmutadores", 1)
    resultado_rota = gm.transmutar("RUNA_ATAQUE", "RUNA_MAGIA")
    if resultado_rota.get("ok") and not resultado_rota.get("es_valida"):
        ok("Combinación inválida genera RUNA_ROTA")
    else:
        falla("Combinación inválida", str(resultado_rota))

# Transmutar sin runas en inventario
resultado_sin_runa = gm.transmutar("RUNA_ATAQUE", "RUNA_DEFENSA")
if not resultado_sin_runa.get("ok"):
    ok("Error al transmutar sin runas disponibles")
else:
    falla("Error sin runas", str(resultado_sin_runa))


# ════════════════════════════════════════════════════════
# 10. PERSISTENCIA ENTRE SESIONES
# ════════════════════════════════════════════════════════
seccion("10. PERSISTENCIA ENTRE SESIONES")

# Simular nuevo arranque — nuevo GameManager con la misma BD
gm2 = GameManager()

if gm2.faccion == "guardian":
    ok("Facción persiste entre sesiones")
else:
    falla("Facción persiste", f"valor: {gm2.faccion}")

if gm2.personaje_activo_id is not None:
    ok("Personaje activo se recupera entre sesiones")
else:
    falla("Personaje activo persiste")

inv2 = gm2.get_personajes_jugador()
if len(inv2) > 0:
    ok("Inventario persiste entre sesiones")
else:
    falla("Inventario persiste")

# No debe iniciar juego de nuevo si ya hay facción
gm2.iniciar_juego("ANOMALÍAS")
if gm2.faccion == "guardian":
    ok("iniciar_juego ignorado si ya hay facción")
else:
    falla("iniciar_juego ignorado", f"facción cambió a {gm2.faccion}")


# ════════════════════════════════════════════════════════
# 11. REPOS ADICIONALES
# ════════════════════════════════════════════════════════
seccion("11. REPOS ADICIONALES")

# personaje_repo
p_por_id = personaje_repo.get_by_id(1)
if p_por_id and "nombre" in p_por_id:
    ok("personaje_repo.get_by_id funciona")
else:
    falla("personaje_repo.get_by_id")

p_por_rareza = personaje_repo.get_by_rareza("S")
if len(p_por_rareza) == 4:
    ok("4 personajes de rareza S")
else:
    falla("4 personajes S", f"hay {len(p_por_rareza)}")

# arma_repo
arma_por_id = arma_repo.get_by_id(1)
if arma_por_id and "nombre" in arma_por_id:
    ok("arma_repo.get_by_id funciona")
else:
    falla("arma_repo.get_by_id")

armas_s = arma_repo.get_by_rareza("S")
if len(armas_s) == 3:
    ok("3 armas de rareza S")
else:
    falla("3 armas S", f"hay {len(armas_s)}")

# runa_repo
runa_por_nombre = runa_repo.get_by_nombre("RUNA_ACERO")
if runa_por_nombre and runa_por_nombre["nombre"] == "RUNA_ACERO":
    ok("runa_repo.get_by_nombre funciona")
else:
    falla("runa_repo.get_by_nombre", str(runa_por_nombre))

# inventario — eliminar item
runa_tmp = runa_repo.get_by_nombre("RUNA_SOMBRA")
if runa_tmp:
    inventario_repo.agregar_item(1, runa_tmp["id"], "runa")
    inv_antes = inventario_repo.get_inventario_by_tipo("runa")
    # obtener su inv_id
    for it in inv_antes:
        if it["catalogo_id"] == runa_tmp["id"]:
            eliminado = inventario_repo.eliminar_item(it["id"])
            if eliminado:
                ok("inventario_repo.eliminar_item funciona")
            else:
                falla("eliminar_item")
            break

# pity_repo
pity_repo.actualizar_pity(1, "armas", 15)
p = pity_repo.get_pity(1, "armas")
if p and p["pity_count"] == 15:
    ok("pity_repo.actualizar_pity y get_pity")
else:
    falla("pity_repo", str(p))

pity_repo.reset_pity(1, "armas")
p_reset = pity_repo.get_pity(1, "armas")
if p_reset and p_reset["pity_count"] == 0:
    ok("pity_repo.reset_pity funciona")
else:
    falla("reset_pity", str(p_reset))

# mapa_repo
mapa_repo.completar_nodo(1, estrellas=3)
n = mapa_repo.get_nodo(1)
if n and n["estrellas"] == 3:
    ok("mapa_repo.completar_nodo con estrellas")
else:
    falla("completar_nodo estrellas", str(n))


# ════════════════════════════════════════════════════════
# RESUMEN FINAL
# ════════════════════════════════════════════════════════
print(f"\n{'═'*55}")
print(f"  RESULTADO: {_ok} ✅  |  {_fail} ❌  |  Total: {_ok + _fail}")
print(f"{'═'*55}")

if _fail == 0:
    print("\n  🎉 TODOS LOS TESTS PASAN — el backend está listo para la demo")
else:
    print(f"\n  ⚠️  {_fail} test(s) fallaron — revisar antes de la demo")

sys.exit(0 if _fail == 0 else 1)
