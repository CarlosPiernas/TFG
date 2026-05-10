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
COLOR_STATS      = hex_to_kivy('#ffffff')   # verde menta brillante para stats de equipo

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
SLOT_RUNA_VACIO = 'assets/logos/SlotRunaVacio.png'
SLOT_ARMA_VACIO = 'assets/logos/SlotArmaVacio.png'

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
BOTON_TRANSMUTAR            = 'assets/logos/BotonTransmutar.png'
ICONO_TRANSMUTADOR        = 'assets/logos/CargaTransmutacion.png'
FLECHA_TRANSMUTAR_GUARDIAN = 'assets/logos/FlechaTransmutar.png'
FLECHA_TRANSMUTAR_ANOMALIA = 'assets/logos/FlechaTransmutarAnomalia.png'
CABECERA_FORJA            = 'assets/fondos/CabeceraForja.jpg'

# Inventario: cabecera y botones de pestañas
CABECERA_INVENTARIO       = 'assets/fondos/CabeceraInventario.jpg'
BOTON_PERSONAJES          = 'assets/logos/BotonPersonajes.png'
BOTON_ARMAS               = 'assets/logos/BotonArmas.png'
BOTON_RUNAS               = 'assets/logos/BotonRunas.png'
BOTON_OBJETOS             = 'assets/logos/BotonObjetos.png'


# Tienda
FONDO_TIENDA        = 'assets/fondos/Fondo_Tienda.png'
TITULO_TIENDA       = 'assets/fondos/Titulo_Tienda.png'
BOTON_COMPRAR       = 'assets/fondos/Boton_Comprar.png'
FRAGMENTO_ROJO      = 'assets/fondos/Fragmento_Rojo.png'
FRAGMENTO_AZUL      = 'assets/fondos/Fragmento_Azul.png'
ICONO_TRANSMUTADOR  = 'assets/logos/CargaTransmutacion.png'
LOGO_POCION           = 'assets/fondos/Logo_Pocion.png'

# Gacha
FONDO_GACHA_ARMAS      = 'assets/fondos/Fondo_Gacha_Armas.png'
FONDO_GACHA_ANOMALIA   = 'assets/fondos/Fondo_Gacha_Anomalia.png'
FONDO_GACHA_GUARDIANES = 'assets/fondos/Fondo_Gacha_Guardianes.png'
TITULO_GACHA           = 'assets/fondos/Titulo_Gacha.png'
TITULO_PERSONAJES      = 'assets/fondos/Titulo_Personajes.png'
TITULO_ARMAS           = 'assets/fondos/Titulo_Armas.png'
BOTON_INVOCAR          = 'assets/fondos/Boton_Invocar.png'
BOTON_FORJAR           = 'assets/fondos/Boton_Forjar.png'
BOTON_TIENDA           = 'assets/fondos/Boton_Tienda.png'
BOTON_VOLVER           = 'assets/logos/Boton.png'
TICKET_PERSONAJES      = 'assets/fondos/Ticket_Personajes.png'
TICKET_ARMAS           = 'assets/fondos/Ticket_Armas.png'

# Fondos
FONDO_SELECCION  = 'assets/fondos/Fondo_Seleccion.png'
FONDO_ANOMALIAS  = 'assets/fondos/Fondo_Anomalias.png'
FONDO_GUARDIANES = 'assets/fondos/Fondo_Guardianes.png'
FONDO_GACHA = 'assets/fondos/Fondo_Gacha_Anomalia.png'
FONDO_SPLASH = 'assets/fondos/Fondo_Splash.png'
# Nombres de facción
NOMBRE_ANOMALIA = 'ANOMALÍAS'
NOMBRE_GUARDIAN = 'GUARDIANES'

# ── Iconos de armas ────────────────────────────────────────────────────────
# Mapean el nombre interno del arma (tal y como aparece en seed.py de M1)
# a su icono visual. Si M1 añade un arma nueva sin entrada aquí, se cae al
# PLACEHOLDER en lugar de romper la UI.

ICONO_ARMA_DAGA_B     = 'assets/logos/IconoDagaB.png'
ICONO_ARMA_MANDOBLE_B = 'assets/logos/IconoMandobleB.png'
ICONO_ARMA_BASTON_B   = 'assets/logos/IconoBastonB.png'
ICONO_ARMA_DAGA_S     = 'assets/logos/IconoDagaS.png'
ICONO_ARMA_MAZA_S     = 'assets/logos/IconoMazaS.png'
ICONO_ARMA_BASTON_S   = 'assets/logos/IconoBastonS.png'

# Las claves coinciden EXACTAMENTE con los nombres en seed.py de M1.
ARMA_ICONOS = {
    # Básicas (B)
    'Daga':                ICONO_ARMA_DAGA_B,
    'Mandoble':            ICONO_ARMA_MANDOBLE_B,
    'Baston':              ICONO_ARMA_BASTON_B,
    # Únicas (S)
    'Tirada del Destino':  ICONO_ARMA_DAGA_S,
    'Hambre Voraz':        ICONO_ARMA_MAZA_S,
    'Magia Interior':      ICONO_ARMA_BASTON_S,
}

# Nombres bonitos a mostrar al usuario. El nombre interno (clave) sigue siendo
# el que persiste M1 en BD; este diccionario es solo presentación.
ARMA_NOMBRES_DISPLAY = {
    'Daga':                'Daga',
    'Mandoble':            'Mandoble',
    'Baston':              'Bastón',
    'Tirada del Destino':  'Tirada del Destino',
    'Hambre Voraz':        'Hambre Voraz',
    'Magia Interior':      'Magia Interior',
}


def icono_arma(nombre_db: str) -> str:
    """Devuelve la ruta del icono de un arma a partir de su nombre interno."""
    return ARMA_ICONOS.get(nombre_db, PLACEHOLDER)


def nombre_arma(nombre_db: str) -> str:
    """Devuelve el nombre bonito de un arma a partir de su nombre interno."""
    return ARMA_NOMBRES_DISPLAY.get(nombre_db, nombre_db)

# Mapa
FONDO_MAPA1_ANOMALIAS  = 'assets/fondos/Fondo_mapa1_Anomalias.png'
FONDO_MAPA2_ANOMALIAS  = 'assets/fondos/Fondo_mapa2_Anomalias.png'
FONDO_MAPA1_GUARDIANES = 'assets/fondos/Fondo_mapa1_Guardianes.png'
FONDO_MAPA2_GUARDIANES = 'assets/fondos/Fondo_mapa2_Guardianes.png'
PORTAL_ANOMALIAS       = 'assets/logos/Portal_anomalias.png'
PORTAL_GUARDIANES      = 'assets/logos/Portal_guardianes.png'
FLECHA_ARRIBA          = 'assets/logos/flecha_arriba.png'
FLECHA_ABAJO           = 'assets/logos/flecha_abajo.png'

# ── Iconos de personajes ───────────────────────────────────────────────────
# Mapean el nombre interno (tal y como lo devuelve tirar_gacha) a su icono.

ICONO_ANOMALIA_GUERRERO_B = 'assets/logos/IconoGuerreroBAnomalia.png'
ICONO_ANOMALIA_ASESINO_B  = 'assets/logos/IconoAsesinoBAnomalia.png'
ICONO_ANOMALIA_ASESINO_A  = 'assets/logos/IconoAsesinoAAnomaliaA.png'
ICONO_ANOMALIA_MAGO_A     = 'assets/logos/IconoMagoAAnomaliaA.png'
ICONO_ANOMALIA_GUERRERO_S = 'assets/logos/IconoGuerreroAnomaliaS.png'
ICONO_ANOMALIA_MAGO_S     = 'assets/logos/IconoMagoAnomalia.png'

ICONO_GUARDIAN_GUERRERO_B = 'assets/logos/IconoGerreroBGuardian.png'   # typo en filename intencional
ICONO_GUARDIAN_MAGO_B     = 'assets/logos/IconoMagoBGuardian.png'
ICONO_GUARDIAN_GUERRERO_A = 'assets/logos/GuerreroAGuardian.png'        # sin prefijo "Icono"
ICONO_GUARDIAN_MAGO_A     = 'assets/logos/IconoMagoAGuardian.png'
ICONO_GUARDIAN_ASESINO_S  = 'assets/logos/IconoAsesinoSGuardian.png'
ICONO_GUARDIAN_MAGO_S     = 'assets/logos/IconoMagoGuardianS.png'

PERSONAJE_ICONOS = {
    'Anomalia_Guerrero_B': ICONO_ANOMALIA_GUERRERO_B,
    'Anomalia_Asesino_B':  ICONO_ANOMALIA_ASESINO_B,
    'Anomalia_Asesino_A':  ICONO_ANOMALIA_ASESINO_A,
    'Anomalia_Mago_A':     ICONO_ANOMALIA_MAGO_A,
    'Anomalia_Guerrero_S': ICONO_ANOMALIA_GUERRERO_S,
    'Anomalia_Mago_S':     ICONO_ANOMALIA_MAGO_S,
    'Guardian_Guerrero_B': ICONO_GUARDIAN_GUERRERO_B,
    'Guardian_Mago_B':     ICONO_GUARDIAN_MAGO_B,
    'Guardian_Guerrero_A': ICONO_GUARDIAN_GUERRERO_A,
    'Guardian_Mago_A':     ICONO_GUARDIAN_MAGO_A,
    'Guardian_Asesino_S':  ICONO_GUARDIAN_ASESINO_S,
    'Guardian_Mago_S':     ICONO_GUARDIAN_MAGO_S,
}


def icono_personaje(nombre_db: str) -> str:
    """Devuelve la ruta del icono de un personaje a partir de su nombre interno."""
    return PERSONAJE_ICONOS.get(nombre_db, PLACEHOLDER)


def nombre_personaje(nombre_db: str) -> str:
    """Devuelve el nombre legible: 'Anomalia_Mago_S' -> 'Mago S'."""
    partes = nombre_db.split('_')
    if len(partes) >= 3:
        return f'{partes[1]} {partes[2]}'
    return nombre_db


# ── Iconos de runas ────────────────────────────────────────────────────────
# Mapean el nombre interno de la runa (tal y como aparece en seed.py de M1)
# a su icono visual. Las claves coinciden EXACTAMENTE con los nombres en BD.

ICONO_RUNA_ATAQUE   = 'assets/logos/runas/Ataque.png'
ICONO_RUNA_MAGIA    = 'assets/logos/runas/Magia.png'
ICONO_RUNA_DEFENSA  = 'assets/logos/runas/Defensa.png'
ICONO_RUNA_DESTREZA = 'assets/logos/runas/Destreza.png'
ICONO_RUNA_ACERO    = 'assets/logos/runas/Acero.png'
ICONO_RUNA_CAZA     = 'assets/logos/runas/Caza.png'
ICONO_RUNA_SOMBRA   = 'assets/logos/runas/Sombras.png'   # filename en plural
ICONO_RUNA_ARCANA   = 'assets/logos/runas/Arcana.png'
ICONO_RUNA_GUARDIAN = 'assets/logos/runas/Guardian.png'
ICONO_RUNA_ROTA     = 'assets/logos/runas/Rota.png'

RUNA_ICONOS = {
    # Básicas
    'RUNA_ATAQUE':   ICONO_RUNA_ATAQUE,
    'RUNA_MAGIA':    ICONO_RUNA_MAGIA,
    'RUNA_DEFENSA':  ICONO_RUNA_DEFENSA,
    'RUNA_DESTREZA': ICONO_RUNA_DESTREZA,
    # Mixtas
    'RUNA_ACERO':    ICONO_RUNA_ACERO,
    'RUNA_CAZA':     ICONO_RUNA_CAZA,
    'RUNA_SOMBRA':   ICONO_RUNA_SOMBRA,
    'RUNA_ARCANA':   ICONO_RUNA_ARCANA,
    'RUNA_GUARDIAN': ICONO_RUNA_GUARDIAN,
    # Penalización
    'RUNA_ROTA':     ICONO_RUNA_ROTA,
}


def icono_runa(nombre_db: str) -> str:
    """Devuelve la ruta del icono de una runa a partir de su nombre interno."""
    return RUNA_ICONOS.get(nombre_db, PLACEHOLDER)