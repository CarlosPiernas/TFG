"""
Mochila — Interfaz del inventario del jugador.
Pestañas:
  - Personajes: ver desbloqueados, seleccionar uno → ver lore y stats
  - Armas: ver desbloqueadas, seleccionar una → ver lore y stats
  - Runas: ver desbloqueadas con stats de cada una
  - Consumibles: fragmentos, tickets, pociones, transmutadores

La Mochila NO guarda datos — solo lee y consulta de DatosJugador y stat.py.
"""

from logic.Clases.stat import (
    PERSONAJES, RUNA_ATAQUE, RUNA_MAGIA, RUNA_DEFENSA, RUNA_DESTREZA,
    RUNA_ACERO, RUNA_SOMBRA, RUNA_ARCANA, RUNA_CAZA, RUNA_GUARDIAN, RUNA_ROTA,
    ARMA_MANDOBLE, ARMA_BASTON, ARMA_DAGA,
    ARMA_S_GUERRERO, ARMA_S_MAGO, ARMA_S_ASESINO,
)

# ═══════════════════════════════════
# CATÁLOGO DE RUNAS (nombre → dict de stats)
# ═══════════════════════════════════

CATALOGO_RUNAS = {
    # Básicas
    "ATAQUE":   {"stats": RUNA_ATAQUE,   "tipo": "basica",  "descripcion": "Aumenta el ataque del portador."},
    "MAGIA":    {"stats": RUNA_MAGIA,    "tipo": "basica",  "descripcion": "Aumenta la magia del portador."},
    "DEFENSA":  {"stats": RUNA_DEFENSA,  "tipo": "basica",  "descripcion": "Aumenta la defensa del portador."},
    "DESTREZA": {"stats": RUNA_DESTREZA, "tipo": "basica",  "descripcion": "Aumenta la destreza del portador."},
    # Mixtas
    "ACERO":    {"stats": RUNA_ACERO,    "tipo": "mixta",   "descripcion": "Runa forjada en acero. Otorga ataque y defensa."},
    "SOMBRA":   {"stats": RUNA_SOMBRA,   "tipo": "mixta",   "descripcion": "Runa de las sombras. Otorga destreza y defensa."},
    "ARCANA":   {"stats": RUNA_ARCANA,   "tipo": "mixta",   "descripcion": "Runa arcana. Otorga magia y algo de defensa."},
    "CAZA":     {"stats": RUNA_CAZA,     "tipo": "mixta",   "descripcion": "Runa del cazador. Otorga ataque y destreza."},
    "GUARDIAN": {"stats": RUNA_GUARDIAN,  "tipo": "mixta",   "descripcion": "Runa del guardian. La mayor defensa del juego."},
    # Rota
    "ROTA":     {"stats": RUNA_ROTA,     "tipo": "rota",    "descripcion": "Runa corrupta. Penaliza la defensa del portador."},
}

# ═══════════════════════════════════
# CATÁLOGO DE ARMAS (nombre → info)
# ═══════════════════════════════════

CATALOGO_ARMAS = {
    "Mandoble":        {"stats": ARMA_MANDOBLE,    "tipo": "basica", "clase": "Guerrero",
                        "lore": "[Lore pendiente] Un mandoble pesado forjado para resistir el combate prolongado."},
    "Bastón":          {"stats": ARMA_BASTON,      "tipo": "basica", "clase": "Mago",
                        "lore": "[Lore pendiente] Un bastón canalizado con energía arcana."},
    "Daga":            {"stats": ARMA_DAGA,        "tipo": "basica", "clase": "Asesino",
                        "lore": "[Lore pendiente] Una daga ligera diseñada para golpes rápidos y precisos."},
    "Mandoble_Cronos": {"stats": ARMA_S_GUERRERO,  "tipo": "S",      "clase": "Guerrero",
                        "lore": "[Lore pendiente] El Mandoble de Cronos, forjado con fragmentos del tiempo. Solo un Guerrero S puede empuñarlo."},
    "Cetro_Vacío":     {"stats": ARMA_S_MAGO,      "tipo": "S",      "clase": "Mago",
                        "lore": "[Lore pendiente] El Cetro del Vacío, un arma que canaliza la nada misma. Solo un Mago S puede controlarlo."},
    "Hoja_Espectral":  {"stats": ARMA_S_ASESINO,   "tipo": "S",      "clase": "Asesino",
                        "lore": "[Lore pendiente] La Hoja Espectral, invisible al ojo humano. Solo un Asesino S puede sentir su filo."},
}


class Mochila:
    """
    Interfaz del inventario. Lee datos de DatosJugador.
    Cada método devuelve la información que la UI necesita mostrar.
    """

    def __init__(self, datos_jugador):
        """Recibe una instancia de DatosJugador."""
        self.datos = datos_jugador

    # ═══════════════════════════════════
    # PESTAÑA: PERSONAJES
    # ═══════════════════════════════════

    def listar_personajes(self):
        """
        Devuelve lista de personajes desbloqueados con su info básica.
        Cada elemento: {"nombre", "clase", "rareza", "faccion"}.
        """
        resultado = []
        for nombre in sorted(self.datos.personajes_desbloqueados):
            if nombre in PERSONAJES:
                datos_pers = PERSONAJES[nombre]
                resultado.append({
                    "nombre":  nombre,
                    "clase":   datos_pers["clase"],
                    "rareza":  datos_pers["rareza"],
                    "faccion": datos_pers["faccion"],
                })
        return resultado

    def ver_personaje(self, nombre):
        """
        Devuelve el detalle completo de un personaje desbloqueado.
        Incluye stats, lore, clase, rareza, facción.
        Devuelve None si no está desbloqueado o no existe.
        """
        if not self.datos.tiene_personaje(nombre):
            return None
        if nombre not in PERSONAJES:
            return None

        datos_pers = PERSONAJES[nombre]
        return {
            "nombre":  nombre,
            "clase":   datos_pers["clase"],
            "rareza":  datos_pers["rareza"],
            "faccion": datos_pers["faccion"],
            "stats":   datos_pers["stats"],
            "lore":    datos_pers.get("lore", "[Lore pendiente]"),
        }

    # ═══════════════════════════════════
    # PESTAÑA: ARMAS
    # ═══════════════════════════════════

    def listar_armas(self):
        """
        Devuelve lista de armas desbloqueadas con info básica.
        Cada elemento: {"nombre", "tipo", "clase"}.
        """
        resultado = []
        for nombre in sorted(self.datos.armas_desbloqueadas):
            if nombre in CATALOGO_ARMAS:
                info = CATALOGO_ARMAS[nombre]
                resultado.append({
                    "nombre": nombre,
                    "tipo":   info["tipo"],
                    "clase":  info["clase"],
                })
        return resultado

    def ver_arma(self, nombre):
        """
        Devuelve el detalle completo de un arma desbloqueada.
        Incluye stats, lore, tipo, clase.
        Devuelve None si no está desbloqueada o no existe.
        """
        if not self.datos.tiene_arma(nombre):
            return None
        if nombre not in CATALOGO_ARMAS:
            return None

        info = CATALOGO_ARMAS[nombre]
        return {
            "nombre": nombre,
            "tipo":   info["tipo"],
            "clase":  info["clase"],
            "stats":  info["stats"],
            "lore":   info["lore"],
        }

    # ═══════════════════════════════════
    # PESTAÑA: RUNAS
    # ═══════════════════════════════════

    def listar_runas(self):
        """
        Devuelve lista de runas que el jugador posee (cantidad > 0).
        Cada elemento: {"nombre", "cantidad", "tipo", "stats", "descripcion"}.
        """
        resultado = []
        for nombre, cantidad in self.datos.listar_runas():
            if nombre in CATALOGO_RUNAS:
                info = CATALOGO_RUNAS[nombre]
                resultado.append({
                    "nombre":      nombre,
                    "cantidad":    cantidad,
                    "tipo":        info["tipo"],
                    "stats":       info["stats"],
                    "descripcion": info["descripcion"],
                })
            else:
                # Runa desconocida (no debería pasar, pero por seguridad)
                resultado.append({
                    "nombre":      nombre,
                    "cantidad":    cantidad,
                    "tipo":        "desconocida",
                    "stats":       {},
                    "descripcion": "Runa desconocida.",
                })
        return resultado

    def ver_runa(self, nombre):
        """
        Devuelve el detalle de una runa específica.
        Devuelve None si el jugador no la posee.
        """
        if self.datos.cantidad_runa(nombre) <= 0:
            return None
        if nombre not in CATALOGO_RUNAS:
            return None

        info = CATALOGO_RUNAS[nombre]
        return {
            "nombre":      nombre,
            "cantidad":    self.datos.cantidad_runa(nombre),
            "tipo":        info["tipo"],
            "stats":       info["stats"],
            "descripcion": info["descripcion"],
        }

    # ═══════════════════════════════════
    # PESTAÑA: CONSUMIBLES
    # ═══════════════════════════════════

    def ver_consumibles(self):
        """
        Devuelve un diccionario con todos los consumibles del jugador.
        La UI muestra esto directamente.
        """
        return {
            "pociones":            self.datos.pociones,
            "transmutadores":      self.datos.transmutadores,
            "tickets_personaje":   self.datos.tickets_personaje,
            "tickets_arma":        self.datos.tickets_arma,
            "fragmentos_personaje": self.datos.fragmentos_personaje,
            "fragmentos_arma":     self.datos.fragmentos_arma,
            "monedas":             self.datos.monedas,
        }

    # ═══════════════════════════════════
    # RESUMEN GENERAL
    # ═══════════════════════════════════

    def resumen(self):
        """Devuelve un resumen de todo el inventario para debug/UI."""
        total_pers = len(PERSONAJES)
        total_armas = len(CATALOGO_ARMAS)

        return {
            "personajes": f"{len(self.datos.personajes_desbloqueados)}/{total_pers}",
            "armas":      f"{len(self.datos.armas_desbloqueadas)}/{total_armas}",
            "runas":      len(self.datos.runas),
            "consumibles": self.ver_consumibles(),
        }