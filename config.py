GACHA_MODE = "simple"
# Convierte un color hexadecimal (#RRGGBB) a tupla RGBA que entiende Kivy
def hex_to_kivy(hex_color):
    h = hex_color.lstrip('#')
    r, g, b = tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    return (r, g, b, 1)

# Paleta de colores
FONDO_PRINCIPAL  = hex_to_kivy('#0f0f1f')
PANEL_OSCURO     = hex_to_kivy('#1a2130')
PANEL_MEDIO      = hex_to_kivy('#212b3b')
COLOR_ANOMALIAS  = hex_to_kivy("#720998")
COLOR_GUARDIANES = hex_to_kivy('#ffbf00')
BLANCO           = hex_to_kivy('#ffffff')
GRIS             = hex_to_kivy('#808080')
COLOR_CAMPAÑA    = hex_to_kivy('#009aa6')
COLOR_VIDA       = hex_to_kivy('#00cc33')
COLOR_VIDA_MEDIA = hex_to_kivy('#ff9900')
COLOR_VIDA_BAJA  = hex_to_kivy('#cc2222')
COLOR_STATS      = hex_to_kivy('#5fffa8')   # verde menta brillante para stats de equipo

# Moneda e iconos de navegación
ICONO_MONEDA     = 'assets/logos/Moneda.png'
ICONO_GACHA      = 'assets/logos/IconoGacha.png'
ICONO_INVENTARIO = 'assets/logos/IconoInventario.png'
ICONO_ATK      = 'assets/logos/Ataque.png'
ICONO_DEF      = 'assets/logos/Defensa.png'
ICONO_DES      = 'assets/logos/Destreza.png'
ICONO_MAG      = 'assets/logos/Magia.png'
ICONO_POCION   = 'assets/logos/potions.png'
PAPIRO_ANOMALIA  = 'assets/fondos/papiroAnomalo.png'
PAPIRO_GUARDIAN  = 'assets/fondos/papiroGuardian.png'
ICONO_CAMPAÑA    = 'assets/logos/IconoCampaña.png'
FONDO_HOME       = 'assets/fondos/FondoPantallaHome.jpg'

# Fondos bloque runas
FONDO_RUNA_ANOMALIA  = 'assets/fondos/fondoRunaAnoma.jpg'
FONDO_RUNA_GUARDIAN  = 'assets/fondos/fondoRunaGuard.jpg'

# Placeholder para assets que faltan
PLACEHOLDER = 'assets/test.png'

# Logos
LOGO_ANOMALIA = 'assets/logos/Logo_Anomalias.png'
LOGO_GUARDIAN = 'assets/logos/Logo_Guardianes.png'

# Marco decorativo de la barra de vida (común para ambas facciones)
MARCO_VIDA    = 'assets/logos/MarcoVida.png'

# ── Forja: fondos por facción y slots de runas ──────────────────────────────
FONDO_FORJA_GUARDIAN = 'assets/fondos/Forja_Guar_Pulida.jpg'
FONDO_FORJA_ANOMALIA = 'assets/fondos/ForjaVacioPulida.jpg'

SLOT_RUNA_GUARDIAN   = 'assets/logos/SlotRunaGuardian-sinFondo.png'
SLOT_RUNA_ANOMALIA   = 'assets/logos/SoltRunaVacio-sinFondo.png'
SLOT_RUNA_RESULTADO  = 'assets/logos/SlotResultadoRuna.png'

# Forja: iconos de botones y cargas
ICONO_FORJAR              = 'assets/logos/IconoForjar.png'
MARCO_BOTON               = 'assets/logos/Boton.png'
BOTON_FORJAR              = 'assets/logos/BotonForjar.png'
ICONO_TRANSMUTADOR        = 'assets/logos/CargaTransmutacion.png'
FLECHA_TRANSMUTAR_GUARDIAN = 'assets/logos/FlechaTransmutar.png'
FLECHA_TRANSMUTAR_ANOMALIA = 'assets/logos/FlechaTransmutarAnomalia.png'
CABECERA_FORJA            = 'assets/fondos/CabeceraForja.jpg'

# Sprites personajes
SPRITE_ANOMALIA = 'assets/personajes/PersonajesS/Jugable/NEXPAS/NEXPASsplash.png'
SPRITE_GUARDIAN = 'assets/personajes/PersonajesS/Jugable/SARA/sarasplash.png'

# Fondos
FONDO_SELECCION  = 'assets/fondos/Fondo_Seleccion.png'
FONDO_ANOMALIAS  = 'assets/fondos/Fondo_Anomalias.png'
FONDO_GUARDIANES = 'assets/fondos/Fondo_Guardianes.png'
FONDO_GACHA = 'assets/fondos/Fondo_Gacha.png'
# Nombres de facción
NOMBRE_ANOMALIA = 'ANOMALÍAS'
NOMBRE_GUARDIAN = 'GUARDIANES'