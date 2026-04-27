import random
from database.repositories import historial_repo, recursos_repo, pity_repo, inventario_repo
from database.config import GACHA_MODE

# Constantes
BASE_RATE_S         = 0.006
SOFT_PITY_START     = 60
HARD_PITY_GENSHIN   = 90
HARD_PITY_SIMPLE    = 5    # 5 para demo del tribunal
BANNER_PERSONAJES   = "personajes"
BANNER_ARMAS        = "armas"


def _calcular_tasa_s(pity_count: int) -> float:
    if pity_count < SOFT_PITY_START:
        return BASE_RATE_S
    pulls_en_soft = pity_count - SOFT_PITY_START + 1
    rango = HARD_PITY_GENSHIN - SOFT_PITY_START
    incremento = (1.0 - BASE_RATE_S) / rango
    return min(BASE_RATE_S + incremento * pulls_en_soft, 1.0)


def _determinar_rareza(pity_count: int) -> str:
    if GACHA_MODE == "genshin":
        return _rareza_genshin(pity_count)
    else:
        return _rareza_simple(pity_count)


def _rareza_simple(pity_count: int) -> str:
    if pity_count >= HARD_PITY_SIMPLE:
        return "S"
    roll = random.random()
    if roll < 0.10:   return "S"   # 10% según GDD
    if roll < 0.40:   return "A"   # 30%
    return "B"                      # 60%


def _rareza_genshin(pity_count: int) -> str:
    if pity_count >= HARD_PITY_GENSHIN:
        return "S"
    tasa_s = _calcular_tasa_s(pity_count)
    roll = random.random()
    if roll < tasa_s:          return "S"
    if roll < tasa_s + 0.30:   return "A"
    return "B"


def _seleccionar_item(rareza: str, banner: str, faccion: str) -> dict | None:
    from database.repositories import personaje_repo, arma_repo
    if banner == BANNER_PERSONAJES:
        pool = personaje_repo.get_by_rareza_y_faccion(rareza, faccion)
        tipo = "personaje"
    elif banner == BANNER_ARMAS:
        rareza_arma = "B" if rareza == "A" else rareza
        pool = arma_repo.get_by_rareza(rareza_arma)
        tipo = "arma"
    else:
        return None
    if not pool:
        return None
    item = dict(random.choice(pool))
    item["tipo"] = tipo
    return item


def realizar_pull(jugador_id: int, banner: str, faccion: str) -> dict:
    estado_pity = pity_repo.get_pity(jugador_id, banner)
    if estado_pity is None:
        pity_count = 0
    else:
        pity_count = estado_pity["pity_count"]

    rareza = _determinar_rareza(pity_count)
    item   = _seleccionar_item(rareza, banner, faccion)
    if item is None:
        return {"error": "pool_vacio"}

    exito = recursos_repo.consumir_ticket(jugador_id, banner, cantidad=1)
    if not exito:
        return {"error": "tickets_insuficientes"}

    if rareza == "S":
        nuevo_pity_count = 0
    else:
        nuevo_pity_count = pity_count + 1
    pity_repo.actualizar_pity(jugador_id, banner, nuevo_pity_count)

    es_nuevo = inventario_repo.agregar_item(jugador_id, item["id"], item["tipo"])
    tipo_fragmento = "rojo" if banner == BANNER_PERSONAJES else "azul"
    if not es_nuevo:
        recursos_repo.agregar_fragmento(jugador_id, tipo_fragmento, cantidad=1)

    historial_repo.registrar_tirada(
        jugador_id  = jugador_id,
        banner      = banner,
        tipo        = item["tipo"],
        catalogo_id = item["id"],
        rareza      = rareza,
        es_nuevo    = es_nuevo,
    )

    return {
        "item":      item,
        "rareza":    item["rareza"],
        "pity_count": nuevo_pity_count,
        "es_nuevo":  es_nuevo,
        "fragmento": None if es_nuevo else tipo_fragmento,
    }


def realizar_multi_pull(jugador_id: int, banner: str, faccion: str) -> list[dict]:
    tickets = recursos_repo.get_tickets(jugador_id, banner)
    if tickets < 10:
        return [{"error": "tickets_insuficientes"}]

    rareza_prueba = _determinar_rareza(0)
    item_prueba   = _seleccionar_item(rareza_prueba, banner, faccion)
    if item_prueba is None:
        return [{"error": "pool_vacio"}]

    resultados = []
    for i in range(10):
        resultado = realizar_pull(jugador_id, banner, faccion)
        if "error" in resultado:
            resultados.append(resultado)
            break
        resultados.append(resultado)
    return resultados