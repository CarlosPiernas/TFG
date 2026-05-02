
from database.db_manager import get_connection

PRECIO_POCION           = 30
PRECIO_TICKET_PERSONAJE = 200
PRECIO_TICKET_ARMA      = 150
PRECIO_TRANSMUTADOR     = 100
FRAGMENTOS_TICKET_PERS  = 50
FRAGMENTOS_TICKET_ARMA  = 50


def _get_recursos():
    conn = get_connection()
    try:
        return dict(conn.execute("SELECT * FROM recursos_jugador WHERE id = 1").fetchone())
    finally:
        conn.close()


def _add_recurso(campo: str, cantidad: int):
    conn = get_connection()
    try:
        conn.execute(
            f"UPDATE recursos_jugador SET {campo} = {campo} + ? WHERE id = 1",
            (cantidad,)
        )
        conn.commit()
    finally:
        conn.close()


def comprar_pocion() -> dict:
    r = _get_recursos()
    if r['monedas'] < PRECIO_POCION:
        return {"ok": False, "mensaje": f"Monedas insuficientes ({r['monedas']}/{PRECIO_POCION})."}
    _add_recurso('monedas', -PRECIO_POCION)
    _add_recurso('pociones', 1)
    return {"ok": True, "mensaje": "Poción comprada."}


def comprar_ticket_personaje(con_fragmentos=False) -> dict:
    r = _get_recursos()
    if con_fragmentos:
        if r['fragmentos_rojos'] < FRAGMENTOS_TICKET_PERS:
            return {"ok": False, "mensaje": f"Fragmentos insuficientes ({r['fragmentos_rojos']}/{FRAGMENTOS_TICKET_PERS})."}
        _add_recurso('fragmentos_rojos', -FRAGMENTOS_TICKET_PERS)
    else:
        if r['monedas'] < PRECIO_TICKET_PERSONAJE:
            return {"ok": False, "mensaje": f"Monedas insuficientes ({r['monedas']}/{PRECIO_TICKET_PERSONAJE})."}
        _add_recurso('monedas', -PRECIO_TICKET_PERSONAJE)
    _add_recurso('tickets_personaje', 1)
    return {"ok": True, "mensaje": "Ticket de personaje comprado."}


def comprar_ticket_arma(con_fragmentos=False) -> dict:
    r = _get_recursos()
    if con_fragmentos:
        if r['fragmentos_azules'] < FRAGMENTOS_TICKET_ARMA:
            return {"ok": False, "mensaje": f"Fragmentos insuficientes ({r['fragmentos_azules']}/{FRAGMENTOS_TICKET_ARMA})."}
        _add_recurso('fragmentos_azules', -FRAGMENTOS_TICKET_ARMA)
    else:
        if r['monedas'] < PRECIO_TICKET_ARMA:
            return {"ok": False, "mensaje": f"Monedas insuficientes ({r['monedas']}/{PRECIO_TICKET_ARMA})."}
        _add_recurso('monedas', -PRECIO_TICKET_ARMA)
    _add_recurso('tickets_arma', 1)
    return {"ok": True, "mensaje": "Ticket de arma comprado."}


def comprar_transmutador() -> dict:
    r = _get_recursos()
    if r['monedas'] < PRECIO_TRANSMUTADOR:
        return {"ok": False, "mensaje": f"Monedas insuficientes ({r['monedas']}/{PRECIO_TRANSMUTADOR})."}
    _add_recurso('monedas', -PRECIO_TRANSMUTADOR)
    _add_recurso('transmutadores', 1)
    return {"ok": True, "mensaje": "Transmutador comprado."}


def get_recursos_tienda() -> dict:
    r = _get_recursos()
    return {
        "monedas":           r.get('monedas', 0),
        "fragmentos_rojos":  r.get('fragmentos_rojos', 0),
        "fragmentos_azules": r.get('fragmentos_azules', 0),
    }


def puede_comprar() -> dict:
    r = _get_recursos()
    m = r.get('monedas', 0)
    fr = r.get('fragmentos_rojos', 0)
    fa = r.get('fragmentos_azules', 0)
    return {
        "pocion":                    m  >= PRECIO_POCION,
        "ticket_personaje_monedas":  m  >= PRECIO_TICKET_PERSONAJE,
        "ticket_personaje_frags":    fr >= FRAGMENTOS_TICKET_PERS,
        "ticket_arma_monedas":       m  >= PRECIO_TICKET_ARMA,
        "ticket_arma_frags":         fa >= FRAGMENTOS_TICKET_ARMA,
        "transmutador":              m  >= PRECIO_TRANSMUTADOR,
    }