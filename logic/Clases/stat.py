# stats.py — Clases/
# Todos los valores numéricos del juego en un solo sitio
# Cambiar aquí afecta a todo el juego sin tocar la lógica

# ══════════════════════════════════════════════════
# STATS BASE DE PERSONAJES — RAREZA B (sin equipo)
# ══════════════════════════════════════════════════

STATS_GUERRERO_B = {
    "atk":     130,
    "defensa": 100,
    "vida":    600,
}

STATS_MAGO_B = {
    "atk":     50,
    "magia":  100,   # ATK efectivo = atk + magia = 150
    "defensa": 80,
    "vida":   400,
}

STATS_ASESINO_B = {
    "atk":      110,
    "defensa":   90,
    "vida":     500,
    "destreza":  50,
}

# ══════════════════════════════════════════════════
# STATS BASE DE PERSONAJES — RAREZA A (+20% sobre B)
# ══════════════════════════════════════════════════

STATS_GUERRERO_A = {
    "atk":     156,
    "defensa": 120,
    "vida":    720,
}

STATS_MAGO_A = {
    "atk":     60,
    "magia":  120,   # ATK efectivo = 180
    "defensa": 96,
    "vida":   480,
}

STATS_ASESINO_A = {
    "atk":      132,
    "defensa":  108,
    "vida":     600,
    "destreza":  60,
}

# ══════════════════════════════════════════════════
# STATS BASE DE PERSONAJES — RAREZA S (+50% sobre A)      # ← CAMBIO: era +30%
# ══════════════════════════════════════════════════

STATS_GUERRERO_S = {
    "atk":     240,       # era 203
    "defensa": 195,       # era 156
    "vida":    1100,      # era 936
}

STATS_MAGO_S = {
    "atk":     90,        # era 78
    "magia":  185,        # era 156 — ATK efectivo = 275
    "defensa": 200,       # era 125 — CAMBIO MAYOR: necesario para sobrevivir jefes
    "vida":   750,        # era 624
}

STATS_ASESINO_S = {
    "atk":      198,      # era 172
    "defensa":  165,      # era 140
    "vida":     920,      # era 780
    "destreza":  90,      # era 78
}

# Alias rareza B para compatibilidad con código existente
STATS_GUERRERO = STATS_GUERRERO_B
STATS_MAGO     = STATS_MAGO_B
STATS_ASESINO  = STATS_ASESINO_B


# ════════════════
# RUNAS SIMPLES
# ═══════════════

RUNA_ATAQUE    = {"atk": 25}
RUNA_MAGIA     = {"magia": 30}
RUNA_DEFENSA   = {"defensa": 20}
RUNA_DESTREZA  = {"destreza": 25}


# ══════════════
# RUNAS MIXTAS
# ═══════════════

RUNA_ACERO          = {"atk": 30, "defensa": 20}
RUNA_SOMBRA         = {"destreza": 30, "defensa": 15}
RUNA_ARCANA         = {"magia": 30, "defensa": 10}
RUNA_CAZA           = {"atk": 20, "destreza": 25}
RUNA_GUARDIAN        = {"defensa": 40}
RUNA_ROTA            = {"defensa": -40}


# ═══════════════
# ARMAS BÁSICAS
# ════════════════

ARMA_MANDOBLE = {"atk": 20}           # Guerrero
ARMA_BASTON   = {"magia": 20}         # Mago
ARMA_DAGA     = {"atk": 20}           # Asesino


# ══════════════════════════════════
# ARMAS S (únicas por personaje S)
# ═══════════════════════════════════

ARMA_S_GUERRERO = {"atk": 55, "defensa": 55}               # era {"atk": 30, "defensa": 20} — Mandoble de Cronos
ARMA_S_MAGO     = {"magia": 55, "defensa": 40}             # era {"magia": 40, "defensa": -10} — Cetro del Vacío (ya no penaliza)
ARMA_S_ASESINO  = {"atk": 25, "destreza": 50}              # era {"atk": 10, "destreza": 30} — Hoja Espectral


# ═══════════════════
# ENEMIGOS POR NODO
# ═══════════════════

ENEMIGOS = {
    1: {
        "nombre":  "Anomalía Alfa",
        "tipo":    "basico",
        "atk":      80,
        "defensa":  90,
        "vida":    300,
    },
    2: {
        "nombre":  "Sombra Errante",
        "tipo":    "basico",
        "atk":     105,
        "defensa": 115,
        "vida":    400,
    },
    3: {
        "nombre":  "Distorsión Menor",
        "tipo":    "basico",
        "atk":     115,
        "defensa": 130,
        "vida":    500,
    },
    4: {
        "nombre":  "Eco del Vacío",
        "tipo":    "basico",
        "atk":     125,
        "defensa": 132,
        "vida":    600,
    },
    5: {
        "nombre":  "KRONOS",
        "tipo":    "jefe",
        "atk":     100,
        "defensa": 120,
        "vida":    900,
    },

    # ══════════════════════════════════════════════════
    # NODOS 6-10 — Requieren equipamiento progresivo
    # ══════════════════════════════════════════════════

    6: {
        "nombre":  "Anomalía Beta",
        "tipo":    "basico",
        "atk":     160,
        "defensa": 175,
        "vida":    950,
        "requisito": "2 runas",
    },
    7: {
        "nombre":  "Sombra Profunda",
        "tipo":    "basico",
        "atk":     179,
        "defensa": 195,
        "vida":    1100,
        "requisito": "2 runas + arma básica",
    },
    8: {
        "nombre":  "Distorsión Mayor",
        "tipo":    "basico",
        "atk":     198,
        "defensa": 221,
        "vida":    1300,
        "requisito": "2 runas + arma básica + personaje A",
    },
    9: {
        "nombre":  "Vacío Absoluto",
        "tipo":    "basico",
        "atk":     218,
        "defensa": 268,
        "vida":    1500,
        "requisito": "2 runas + arma básica + personaje S",
    },
    10: {
        "nombre":  "KRONOS DEFINITIVO",
        "tipo":    "jefe",
        "atk":     280,
        "defensa": 265,
        "vida":    1800,
        "requisito": "2 runas + arma S + personaje S",
    },
}
PERSONAJES = {
    # ── Anomalías ──────────────────────────────────
    "Nombre1":  {"faccion": "Anomalias", "clase": "Guerrero", "rareza": "B", "stats": STATS_GUERRERO_B,
                 "lore": "[Lore pendiente] Guerrero de las Anomalías, rango B."},
    "Nombre2":  {"faccion": "Anomalias", "clase": "Asesino",  "rareza": "B", "stats": STATS_ASESINO_B,
                 "lore": "[Lore pendiente] Asesino de las Anomalías, rango B."},
    "Nombre3":  {"faccion": "Anomalias", "clase": "Asesino",  "rareza": "A", "stats": STATS_ASESINO_A,
                 "lore": "[Lore pendiente] Asesino de élite de las Anomalías, rango A."},
    "Nombre4":  {"faccion": "Anomalias", "clase": "Mago",     "rareza": "A", "stats": STATS_MAGO_A,
                 "lore": "[Lore pendiente] Mago avanzado de las Anomalías, rango A."},
    "Nombre5":  {"faccion": "Anomalias", "clase": "Guerrero", "rareza": "S", "stats": STATS_GUERRERO_S,
                 "lore": "[Lore pendiente] El guerrero supremo de las Anomalías, rango S."},
    "Nombre6":  {"faccion": "Anomalias", "clase": "Mago",     "rareza": "S", "stats": STATS_MAGO_S,
                 "lore": "[Lore pendiente] El mago más poderoso de las Anomalías, rango S."},
    # ── Guardianes ─────────────────────────────────
    "Nombre7":  {"faccion": "Guardianes", "clase": "Guerrero", "rareza": "B", "stats": STATS_GUERRERO_B,
                 "lore": "[Lore pendiente] Guerrero de los Guardianes, rango B."},
    "Nombre8":  {"faccion": "Guardianes", "clase": "Mago",     "rareza": "B", "stats": STATS_MAGO_B,
                 "lore": "[Lore pendiente] Mago de los Guardianes, rango B."},
    "Nombre9":  {"faccion": "Guardianes", "clase": "Guerrero", "rareza": "A", "stats": STATS_GUERRERO_A,
                 "lore": "[Lore pendiente] Guerrero veterano de los Guardianes, rango A."},
    "Nombre10": {"faccion": "Guardianes", "clase": "Mago",     "rareza": "A", "stats": STATS_MAGO_A,
                 "lore": "[Lore pendiente] Mago avanzado de los Guardianes, rango A."},
    "Nombre11": {"faccion": "Guardianes", "clase": "Asesino",  "rareza": "S", "stats": STATS_ASESINO_S,
                 "lore": "[Lore pendiente] El asesino legendario de los Guardianes, rango S."},
    "Nombre12": {"faccion": "Guardianes", "clase": "Mago",     "rareza": "S", "stats": STATS_MAGO_S,
                 "lore": "[Lore pendiente] El mago supremo de los Guardianes, rango S."},
}
# ═══════════════════════════════════════════
# ECONOMÍA — Monedas y precios
# ═══════════════════════════════════════════

MONEDAS_POR_NODO = {
    1: 50, 2: 50, 3: 50,
    4: 75,
    5: 100,       # jefe — también da 1 ticket gratis + 1 transmutador
    6: 100, 7: 100,
    8: 150, 9: 150,
    10: 200,      # jefe final — también da 1 transmutador + 1 ticket aleatorio
}

PRECIO_POCION        = 30     # restaura vida + contadores al máximo
PRECIO_TICKET_PERS   = 200    # ticket rojo (personaje)
PRECIO_TICKET_ARMA   = 150    # ticket azul (arma)

NODOS_DROP_RUNA      = [4, 5, 6, 7, 8, 9, 10]  # 7 runas básicas por run
NODOS_TRANSMUTADOR   = [5, 10]                   # 2 transmutadores por run
NODOS_TICKET_GRATIS  = {
    5:  "personaje",      # nodo 5: siempre ticket de personaje
    10: "aleatorio",      # nodo 10: 50% personaje / 50% arma (RNG)
}


# ═══════════════════════════════════════════
# TRANSMUTADOR — Recetas de combinación
# ═══════════════════════════════════════════

RECETAS_TRANSMUTADOR = {
    frozenset(["ATAQUE", "DEFENSA"]):   "ACERO",     # +30 ATK, +20 DEF
    frozenset(["ATAQUE", "DESTREZA"]):  "CAZA",      # +20 ATK, +25 DES
    frozenset(["DESTREZA", "DEFENSA"]): "SOMBRA",    # +30 DES, +15 DEF
    frozenset(["MAGIA", "DEFENSA"]):    "ARCANA",    # +30 MAG, +10 DEF
    frozenset(["DESTREZA", "MAGIA"]):   "GUARDIAN",  # +40 DEF pura — mayor DEF del juego
}
# Cualquier combinación NO listada arriba (ej: ATAQUE + MAGIA) = RUNA_ROTA (-40 DEF)
RESULTADO_MEZCLA_INVALIDA = "ROTA"

RUNAS_MIXTAS_MAP = {
    "ACERO":    RUNA_ACERO,
    "CAZA":     RUNA_CAZA,
    "SOMBRA":   RUNA_SOMBRA,
    "ARCANA":   RUNA_ARCANA,
    "GUARDIAN": RUNA_GUARDIAN,
    "ROTA":     RUNA_ROTA,
}


# ═══════════════════════════════════════════
# GACHA — Probabilidades de tickets
# ═══════════════════════════════════════════

PROB_PERSONAJE = {"B": 0.60, "A": 0.30, "S": 0.10}
PROB_ARMA      = {"basica": 0.70, "S": 0.30}

FRAGMENTOS_PARA_ELEGIR = 10  # fragmentos necesarios para elegir un personaje/arma