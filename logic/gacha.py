import random
from database.repositories import historial_repo, recursos_repo, pity_repo, inventario_repo
from database.config import GACHA_MODE

#Constantes
BASE_RATE_S         = 0.006
SOFT_PITY_START     = 60
HARD_PITY_GENSHIN   = 90
HARD_PITY_SIMPLE    = 20   #para modo simple (tasas altas)
BANNER_PERSONAJES = "personajes"
BANNER_ARMAS      = "armas"

#Pool S filtrado por facción — se carga desde BD
#Pool A y B son globales por banner

#Lógica de probabilidad
def _calcular_tasa_s(pity_count: int) -> float:
    #Sin soft pity todavía
    if pity_count < SOFT_PITY_START:
        return BASE_RATE_S
    #Incremento dinámico: subir de BASE a 1.0 en los pulls que quedan
    pulls_en_soft = pity_count - SOFT_PITY_START + 1
    rango = HARD_PITY_GENSHIN - SOFT_PITY_START          # = 30 pulls
    incremento = (1.0 - BASE_RATE_S) / rango     # ≈ 0.0331 por pull
    return min(BASE_RATE_S + incremento * pulls_en_soft, 1.0)

def _determinar_rareza(pity_count: int) -> str:
    if GACHA_MODE == "genshin":
        return _rareza_genshin(pity_count)   # tu curva con soft/hard pity
    else:
        return _rareza_simple(pity_count)    # probabilidades planas del GDD

def _rareza_simple(pity_count: int) -> str:
    if pity_count >= HARD_PITY_SIMPLE:
        return "S"
    roll = random.random()
    if roll < 0.03:   return "S"   # 3% en vez de 10%
    if roll < 0.33:   return "A"
    return "B"

def _rareza_genshin(pity_count: int) -> str:
    if pity_count >= HARD_PITY_GENSHIN:
        return "S"
    tasa_s = _calcular_tasa_s(pity_count)
    roll = random.random()
    if roll < tasa_s:          return "S"
    if roll < tasa_s + 0.30:   return "A"
    return "B"

def _seleccionar_item(rareza: str, banner: str, faccion: str) -> dict | None:
    #Obtiene el pool del banner correspondiente desde la BD
    from database.repositories import personaje_repo, arma_repo
    if banner == BANNER_PERSONAJES:
        pool = personaje_repo.get_by_rareza_y_faccion(rareza, faccion)
        tipo = "personaje"
    elif banner == BANNER_ARMAS:
        #En armas no hay rareza A — si sale A se trata como B
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

#Tirada individual
def realizar_pull(jugador_id: int, banner: str, faccion: str) -> dict:
    #Ejecuta un pull individual.
    #Devuelve un dict con: item, rareza, pity_count, es_nuevo, fragmento

    #Leer estado de pity actual desde BD
    estado_pity = pity_repo.get_pity(jugador_id, banner)
    if estado_pity is None:
        #Primera vez que tira en este banner
        pity_count = 0
    else:
        pity_count = estado_pity["pity_count"]

    #Primero calculamos rareza e item — son solo lectura, no tocan nada
    #Si algo falla aquí el jugador no pierde el ticket
    rareza = _determinar_rareza(pity_count)
    item   = _seleccionar_item(rareza, banner, faccion)
    if item is None:
        return {"error": "pool_vacio"}

    #Solo consumimos el ticket si hay item disponible
    exito = recursos_repo.consumir_ticket(jugador_id, banner, cantidad=1)
    if not exito:
        return {"error": "tickets_insuficientes"}

    #Actualizar contadores de pity
    if rareza == "S":
        nuevo_pity_count = 0  #reset al sacar S
    else:
        nuevo_pity_count = pity_count + 1
    pity_repo.actualizar_pity(jugador_id, banner, nuevo_pity_count)

    #Añadir al inventario o convertir en fragmento si es duplicado
    es_nuevo = inventario_repo.agregar_item(jugador_id, item["id"], item["tipo"])
    tipo_fragmento = "rojo" if banner == BANNER_PERSONAJES else "azul"
    if not es_nuevo:
        #Duplicado — convertir en fragmento según tipo de banner
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
        "item":       item,
        "rareza":     item["rareza"],
        "pity_count": nuevo_pity_count,
        "es_nuevo":   es_nuevo,
        "fragmento":  None if es_nuevo else tipo_fragmento,
    }
    

#Multi-pull x10
def realizar_multi_pull(jugador_id: int, banner: str, faccion: str) -> list[dict]:
    #Verificar tickets suficientes antes de empezar
    tickets = recursos_repo.get_tickets(jugador_id, banner)
    if tickets < 10:
        return [{"error": "tickets_insuficientes"}]

    #Verificar que el pool no está vacío antes de consumir nada
    #Hacemos una tirada de prueba sin tocar la BD para comprobar que hay items
    rareza_prueba = _determinar_rareza(0)
    item_prueba   = _seleccionar_item(rareza_prueba, banner, faccion)
    if item_prueba is None:
        return [{"error": "pool_vacio"}]

    #Todo en orden — ejecutar los 10 pulls
    resultados = []
    for i in range(10):
        resultado = realizar_pull(jugador_id, banner, faccion)
        #Si falla un pull intermedio, devolvemos lo que se pudo y paramos
        if "error" in resultado:
            resultados.append(resultado)
            break
        resultados.append(resultado)
    return resultados