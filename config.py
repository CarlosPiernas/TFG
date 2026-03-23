# Convierte un color hexadecimal (#RRGGBB) a tupla RGBA que entiende Kivy
def hex_to_kivy(hex_color):
    h = hex_color.lstrip('#')
    r, g, b = tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    return (r, g, b, 1)
 
 
# Paleta de colores 
FONDO_PRINCIPAL  = hex_to_kivy('#0f0f1f')   # Fondo oscuro principal
PANEL_OSCURO     = hex_to_kivy('#1a2130')   # Panel oscuro
PANEL_MEDIO      = hex_to_kivy('#212b3b')   # Panel medio
COLOR_ANOMALIAS  = hex_to_kivy('#00e5f0')   # Acento Anomalías
COLOR_GUARDIANES = hex_to_kivy('#ffbf00')   # Acento Guardianes / monedas
BLANCO           = hex_to_kivy('#ffffff')
GRIS             = hex_to_kivy('#808080')
COLOR_CAMPAÑA    = hex_to_kivy('#009aa6')   # Botón campaña
COLOR_VIDA       = hex_to_kivy('#00cc33')   # Barra de vida
 
 
# Rutas de imágenes 
 
# Pantalla de selección — logos de cada facción
LOGO_ANOMALIA = 'TFG/Logos/Logo_Anomalias.png'
LOGO_GUARDIAN = 'TFG/Logos/Logo_Guardianes.png'
 
# Pantalla principal — sprites de los personajes 
SPRITE_ANOMALIA = 'TFG/Personajes/Clase S/kuXow.png'
SPRITE_GUARDIAN = 'TFG/Personajes/Clase S/GoldShip.png'
 
# Nombres de facción
NOMBRE_ANOMALIA = 'ANOMALÍAS'
NOMBRE_GUARDIAN = 'GUARDIANES'