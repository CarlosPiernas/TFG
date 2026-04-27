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

# Logos
LOGO_ANOMALIA = 'assets/logos/Logo_Anomalias.png'
LOGO_GUARDIAN = 'assets/logos/Logo_Guardianes.png'

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
