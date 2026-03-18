import random
from database.repositories import recursos_repo, pity_repo, inventario_repo

#Constantes
BASE_RATE_S         = 0.006
BASE_RATE_A         = 0.051
SOFT_PITY_START     = 60
HARD_PITY           = 90

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
    rango = HARD_PITY - SOFT_PITY_START          # = 30 pulls
    incremento = (1.0 - BASE_RATE_S) / rango     # ≈ 0.0331 por pull
    return min(BASE_RATE_S + incremento * pulls_en_soft, 1.0)

def _determinar_rareza(pity_count: int) -> str:
    #Hard pity: si llegamos a 90 sin S, es S garantizado
    if pity_count >= HARD_PITY:
        return "S"
    tasa_s = _calcular_tasa_s(pity_count)
    roll = random.random()
    if roll < tasa_s:
        return "S"
    #Si no es S, comprobamos A sobre el espacio restante
    elif roll < tasa_s + BASE_RATE_A:
        return "A"
    else:
        return "B"

def _seleccionar_item(rareza: str, banner: str, faccion: str) -> dict | None:
    #Obtiene el pool del banner correspondiente desde la BD
    from database.repositories import personaje_repo, arma_repo
    if banner == BANNER_PERSONAJES:
        pool = personaje_repo.get_by_rareza_y_faccion(rareza, faccion)
    elif banner == BANNER_ARMAS:
        pool = arma_repo.get_by_rareza(rareza)
    else:
        return None
    if not pool:
        return None
    return random.choice(pool)

#Tirada individual
def realizar_pull(jugador_id: int, banner: str, faccion: str) -> dict:
    #Ejecuta un pull individual.
    #Devuelve un dict con: item, rareza, pity_count, es_nuevo
    #Leer estado de pity actual desde BD
    estado_pity = pity_repo.get_pity(jugador_id, banner)
    if estado_pity is None:
        #Primera vez que tira en este banner
        pity_count    = 0
        garantia_a    = 0
    else:
        pity_count = estado_pity["pity_count"]
        garantia_a = estado_pity["garantia_a"] 
    #Consumir ticket del banner correspondiente
    exito = recursos_repo.consumir_ticket(jugador_id, banner, cantidad=1)
    if not exito:
        return {"error": "tickets_insuficientes"}
    #Determinar rareza con soft/hard pity
    rareza = _determinar_rareza(pity_count)
    #Seleccionar item aleatorio del pool correcto
    item = _seleccionar_item(rareza, banner, faccion)
    if item is None:
        return {"error": "pool_vacio"}
    #Actualizar contadores de pity
    if rareza == "S":
        nuevo_pity_count = 0  #reset al sacar S
    else:
        nuevo_pity_count = pity_count + 1
    pity_repo.actualizar_pity(jugador_id, banner, nuevo_pity_count)
    #Añadir al inventario (si ya existe, pendiente decisión de duplicados)
    es_nuevo = inventario_repo.agregar_item(jugador_id, item["id"], item["tipo"])
    return {
        "item":       item,
        "rareza":     rareza,
        "pity_count": nuevo_pity_count,
        "es_nuevo":   es_nuevo,
    }

#Multi-pull x10
def realizar_multi_pull(jugador_id: int, banner: str, faccion: str) -> list[dict]:
    #Ejecuta 10 pulls con garantía de al menos 1 resultado A o superior.
    #Verificar tickets suficientes antes de empezar
    tickets = recursos_repo.get_tickets(jugador_id, banner)
    if tickets < 10:
        return [{"error": "tickets_insuficientes"}]
    resultados = []
    hay_a_o_superior = False
    for i in range(10):
        resultado = realizar_pull(jugador_id, banner, faccion)
        if resultado.get("rareza") in ("S", "A"):
            hay_a_o_superior = True
        resultados.append(resultado)
    #Garantía: si los 10 pulls fueron B, el último se convierte en A
    if not hay_a_o_superior:
        ultimo = resultados[-1]
        item_a = _seleccionar_item("A", banner, faccion)
        if item_a:
            #Revertir el item B y sustituir por A garantizado
            inventario_repo.revertir_ultimo_item(jugador_id)
            es_nuevo = inventario_repo.agregar_item(jugador_id, item_a["id"], item_a["tipo"])
            resultados[-1] = {
                "item":       item_a,
                "rareza":     "A",
                "pity_count": ultimo["pity_count"],
                "es_nuevo":   es_nuevo,
                "garantia":   True,  #flag para animación especial en UI
            }
    return resultados