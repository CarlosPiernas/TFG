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
COLOR_ANOMALIAS  = hex_to_kivy("#B37DC6")
COLOR_GUARDIANES = hex_to_kivy('#ffbf00')
BLANCO           = hex_to_kivy('#ffffff')
GRIS             = hex_to_kivy('#808080')
COLOR_CAMPAÑA    = hex_to_kivy('#009aa6')
COLOR_VIDA       = hex_to_kivy('#00cc33')
COLOR_VIDA_MEDIA = hex_to_kivy('#ff9900')
COLOR_VIDA_BAJA  = hex_to_kivy('#cc2222')
COLOR_STATS      = hex_to_kivy('#ffffff')

#Fondos Combate Nodo
FONDO_NODO_1_4 = 'assets/fondos/FondosNodos/Nodo1-4Guardianes.JPg'

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
LOGO_ANOMALIA = 'assets/logos/Logo_Anomalia.png'
LOGO_GUARDIAN = 'assets/logos/Logo_Guardianes.png'

# Marco decorativo de la barra de vida (común para ambas facciones)
MARCO_VIDA    = 'assets/logos/MarcoVida.png'

# ── Forja: fondos por facción y slots de runas ──────────────────────────────
FONDO_FORJA_GUARDIAN = 'assets/fondos/Forja_Guardianes.png'
FONDO_FORJA_ANOMALIA = 'assets/fondos/Forja_Anomalias.png'

SLOT_RUNA_GUARDIAN   = 'assets/logos/SlotRunaGuardian-sinFondo.png'
SLOT_RUNA_ANOMALIA   = 'assets/logos/SoltRunaVacio-sinFondo.png'
SLOT_RUNA_RESULTADO  = 'assets/logos/SlotResultadoRuna.png'

# Forja: iconos de botones y cargas
ICONO_FORJAR               = 'assets/logos/IconoForjar.png'
MARCO_BOTON                = 'assets/logos/Boton.png'
BOTON_TRANSMUTAR           = 'assets/logos/BotonTransmutar.png'
ICONO_TRANSMUTADOR         = 'assets/logos/CargaTransmutacion.png'
FLECHA_TRANSMUTAR_GUARDIAN = 'assets/logos/FlechaTransmutar.png'
FLECHA_TRANSMUTAR_ANOMALIA = 'assets/logos/FlechaTransmutarAnomalia.png'
CABECERA_FORJA             = 'assets/fondos/CabeceraForja.jpg'

# Inventario: cabecera y botones de pestañas
CABECERA_INVENTARIO       = 'assets/fondos/CabeceraInventario.jpg'
BOTON_PERSONAJES          = 'assets/logos/BotonPersonajes.png'
BOTON_ARMAS               = 'assets/logos/BotonArmas.png'
BOTON_RUNAS               = 'assets/logos/BotonRunas.png'
BOTON_OBJETOS             = 'assets/logos/BotonObjetos.png'

# Tienda
FONDO_TIENDA       = 'assets/fondos/Fondo_Tienda.png'
TITULO_TIENDA      = 'assets/fondos/Titulo_Tienda.png'
BOTON_COMPRAR      = 'assets/fondos/Boton_Comprar.png'
FRAGMENTO_ROJO     = 'assets/fondos/Fragmento_Rojo.png'
FRAGMENTO_AZUL     = 'assets/fondos/Fragmento_Azul.png'
LOGO_POCION        = 'assets/fondos/Logo_Pocion.png'

# Sprites personajes
SPRITE_ANOMALIA = 'assets/personajes/PersonajesS/Jugable/NEXPAS/NEXPASsplash.png'
SPRITE_GUARDIAN = 'assets/personajes/PersonajesS/Jugable/SARA/sarasplash.png'

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
FONDO_GACHA      = 'assets/fondos/Fondo_Gacha_Anomalia.png'

# Nombres de facción
NOMBRE_ANOMALIA = 'ANOMALÍAS'
NOMBRE_GUARDIAN = 'GUARDIANES'


# ══════════════════════════════════════════════════════════════════════════════
# ── ICONOS DE ARMAS ───────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

ICONO_ARMA_DAGA_B     = 'assets/logos/IconoDagaB.png'
ICONO_ARMA_MANDOBLE_B = 'assets/logos/IconoMandobleB.png'
ICONO_ARMA_BASTON_B   = 'assets/logos/IconoBastonB.png'
ICONO_ARMA_DAGA_S     = 'assets/logos/IconoDagaS.png'
ICONO_ARMA_MAZA_S     = 'assets/logos/IconoMazaS.png'
ICONO_ARMA_BASTON_S   = 'assets/logos/IconoBastonS.png'

ARMA_ICONOS = {
    'Daga':               ICONO_ARMA_DAGA_B,
    'Mandoble':           ICONO_ARMA_MANDOBLE_B,
    'Baston':             ICONO_ARMA_BASTON_B,
    'Tirada del Destino': ICONO_ARMA_DAGA_S,
    'Hambre Voraz':       ICONO_ARMA_MAZA_S,
    'Magia Interior':     ICONO_ARMA_BASTON_S,
}

# Nombre bonito que ve el jugador (clave = nombre interno en BD).
# "Tirada del Destino" se renombra a "Apuesta Amañada" en la UI.
ARMA_NOMBRES_DISPLAY = {
    'Daga':               'Daga',
    'Mandoble':           'Mandoble',
    'Baston':             'Bastón',
    'Tirada del Destino': 'Apuesta Amañada',
    'Hambre Voraz':       'Hambre Voraz',
    'Magia Interior':     'Magia Interior',
}

# Lore / descripción de cada arma mostrada en el inventario.
ARMA_LORE = {
    'Daga': (
        'Pareja de cuchillos desgastados por el uso. '
        'Más historia que filo, más cicatrices que brillo.'
    ),
    'Mandoble': (
        'Espadón de doble filo heredado de la primera línea. '
        'Su peso aplasta tanto el escudo del enemigo como su voluntad de resistir.'
    ),
    'Baston': (
        'Vara de madera endurecida por ciclos de energía arcana. '
        'Canaliza y amplifica la magia de su portador hasta el límite de lo controlable.'
    ),
    'Tirada del Destino': (
        'Cuchilla de pura energía que al empuñar te da la sensación '
        'de que puedes forzar tu propia suerte.'
    ),
    'Hambre Voraz': (
        'Maza pesada que al golpear devora la piel y consume la vida '
        'de sus oponentes.'
    ),
    'Magia Interior': (
        'Abrumador poder antiguo que impregna a su portador de la sensación '
        'de que poseerlo conlleva un riesgo elevado pero obligatorio.'
    ),
}


def icono_arma(nombre_db: str) -> str:
    return ARMA_ICONOS.get(nombre_db, PLACEHOLDER)

def nombre_arma(nombre_db: str) -> str:
    return ARMA_NOMBRES_DISPLAY.get(nombre_db, nombre_db)

def lore_arma(nombre_db: str) -> str:
    return ARMA_LORE.get(nombre_db, '')
# Mapa
FONDO_MAPA1_ANOMALIAS  = 'assets/fondos/Fondo_mapa1_Anomalias.png'
FONDO_MAPA2_ANOMALIAS  = 'assets/fondos/Fondo_mapa2_Anomalias.png'
FONDO_MAPA1_GUARDIANES = 'assets/fondos/Fondo_mapa1_Guardianes.png'
FONDO_MAPA2_GUARDIANES = 'assets/fondos/Fondo_mapa2_Guardianes.png'
PORTAL_ANOMALIAS       = 'assets/logos/Portal_anomalias.png'
PORTAL_GUARDIANES      = 'assets/logos/Portal_guardianes.png'
FLECHA_ARRIBA          = 'assets/logos/flecha_arriba.png'
FLECHA_ABAJO           = 'assets/logos/flecha_abajo.png'


# ══════════════════════════════════════════════════════════════════════════════
# ── ICONOS Y TEXTOS DE PERSONAJES ─────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

ICONO_ANOMALIA_GUERRERO_B = 'assets/logos/IconoGuerreroBAnomalia.png'
ICONO_ANOMALIA_ASESINO_B  = 'assets/logos/IconoAsesinoBAnomalia.png'
ICONO_ANOMALIA_ASESINO_A  = 'assets/logos/IconoAsesinoAAnomaliaA.png'
ICONO_ANOMALIA_MAGO_A     = 'assets/logos/IconoMagoAAnomaliaA.png'
ICONO_ANOMALIA_GUERRERO_S = 'assets/logos/IconoGuerreroAnomaliaS.png'
ICONO_ANOMALIA_MAGO_S     = 'assets/logos/IconoMagoAnomalia.png'

ICONO_GUARDIAN_GUERRERO_B = 'assets/logos/IconoGerreroBGuardian.png'
ICONO_GUARDIAN_MAGO_B     = 'assets/logos/IconoMagoBGuardian.png'
ICONO_GUARDIAN_GUERRERO_A = 'assets/logos/GuerreroAGuardian.png'
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

# Nombres bonitos que ve el jugador en inventario y en el popup de gacha.
PERSONAJE_NOMBRES_DISPLAY = {
    'Anomalia_Guerrero_B': 'Cascarón Errante',
    'Anomalia_Asesino_B':  'Acechador de Fisuras',
    'Anomalia_Asesino_A':  'Segador Vacío',
    'Anomalia_Mago_A':     'Ojo del Caos',
    'Anomalia_Guerrero_S': 'Voracidad Latente',
    'Anomalia_Mago_S':     'Erudito Sombrío',
    'Guardian_Guerrero_B': 'Kaedrel, el Reforjado',
    'Guardian_Mago_B':     'Alaric, el Archivista',
    'Guardian_Guerrero_A': 'Storm, el Nexo Dorado',
    'Guardian_Mago_A':     'Velen, el Profeta Rúnico',
    'Guardian_Asesino_S':  'Varek, el Trunca Suertes',
    'Guardian_Mago_S':     'Nara, la Última Arma',
}

# Lore / historia de cada personaje mostrada en el inventario.
PERSONAJE_LORE = {
    'Anomalia_Guerrero_B': (
        'Lo que antes fue un soldado con nombre y patria, ahora es un recipiente hueco. '
        'Se mueve por inercia, blandiendo su acero oxidado contra todo lo que '
        'aún conserve un latido.'
    ),
    'Anomalia_Asesino_B': (
        'Una criatura que vive en los entre-espacios. No camina sobre el suelo, '
        'sino que se desliza a través de las grietas de la realidad '
        'en busca de sus víctimas.'
    ),
    'Anomalia_Asesino_A': (
        'Depredador forjado en las entrañas del vacío. Sus hojas no cortan el cuerpo, '
        'sino que borran la conexión de la víctima con este mundo. '
        'Aquellos que caen bajo su guadaña no dejan cadáver.'
    ),
    'Anomalia_Mago_A': (
        'Su sola presencia deforma la gravedad y el tiempo, haciendo que los hechizos '
        'de los héroes se retuerzan y que sus huesos se vuelvan tan frágiles como el cristal. '
        'Antaño tenía cuerpo y nombre; ahora es puro vacío.'
    ),
    'Anomalia_Guerrero_S': (
        'Antaño la vanguardia de la orden de los Guardianes, su nombre y gloria se '
        'ahogaron en el abismo tras su sacrificio. En el último suspiro, la entidad '
        'de hambre pura se enraizó en su cuerpo inerte, convirtiendo su cadáver '
        'de hierro en un recipiente para una voracidad insaciable.'
    ),
    'Anomalia_Mago_S': (
        'Antiguo protector de un mundo perdido, sucumbió a la obsesión y fue reclamado '
        'por el Vacío. No lanza magia común: materializa el vacío para invocar Sombra. '
        'En su interior ya no habita un hombre, sino un conocimiento oscuro que ha '
        'borrado cualquier rastro de piedad.'
    ),
    'Guardian_Guerrero_B': (
        'Soldado de infantería que sobrevivió al primer desgarro de la realidad. '
        'Kaedrel es un puente entre la pólvora moderna y la energía de ciclos ancestrales, '
        'poseyendo una fuerza que su cuerpo de carne apenas puede contener.'
    ),
    'Guardian_Mago_B': (
        'El miembro más longevo de la orden. Su cuerpo es un vestigio frágil y desgastado, '
        'pero su mente es una biblioteca viviente que almacena los fracasos de '
        'civilizaciones pasadas. Castiga a las anomalías con el peso de la historia.'
    ),
    'Guardian_Guerrero_A': (
        'Representa la nueva generación de la facción. Storm viste equipo táctico '
        'contemporáneo potenciado por tecnología de los antiguos, que le permite manejar '
        'su colosal arma de piedra. Es la prueba viviente de que el presente puede '
        'reclamarse si se abraza el poder del pasado.'
    ),
    'Guardian_Mago_A': (
        'Su conocimiento rúnico permitió a los Guardianes aumentar su poder hasta hacer '
        'frente a las anomalías. Guiado por un odio desmedido hacia el enemigo, '
        'no piensa en otra cosa que no sea perfeccionar su dominio de las runas.'
    ),
    'Guardian_Asesino_S': (
        'El operativo más pragmático de la orden. Desprecia los rezos y la pulcritud; '
        'su brazo es un Catalizador de Caos rescatado de una línea temporal colapsada. '
        'Cada golpe es una apuesta peligrosa entre la victoria absoluta o su propia destrucción. '
        'La destreza es su única religión y su daga de energía su mejor compañera.'
    ),
    'Guardian_Mago_S': (
        'No nació con poderes, pero su voluntad la convirtió en el arma más peligrosa '
        'de los Guardianes. Absorbe la esencia de las anomalías derrotadas, que quedan '
        'presas en su piel como tatuajes de tinta rosa incandescente. Juzgada por los '
        'veteranos de la orden, dispuesta a pagar cualquier precio por acabar con el enemigo, '
        'aunque implique su propia destrucción.'
    ),
}


def icono_personaje(nombre_db: str) -> str:
    return PERSONAJE_ICONOS.get(nombre_db, PLACEHOLDER)

def nombre_personaje(nombre_db: str) -> str:
    """Nombre bonito completo: 'Anomalia_Guerrero_B' -> 'Cascarón Errante'."""
    return PERSONAJE_NOMBRES_DISPLAY.get(nombre_db, nombre_db)

def nombre_personaje_corto(nombre_db: str) -> str:
    """Nombre corto para el popup del gacha: 'Anomalia_Guerrero_B' -> 'Guerrero B'."""
    partes = nombre_db.split('_')
    if len(partes) >= 3:
        return f'{partes[1]} {partes[2]}'
    return nombre_db

def lore_personaje(nombre_db: str) -> str:
    return PERSONAJE_LORE.get(nombre_db, '')


# ══════════════════════════════════════════════════════════════════════════════
# ── ICONOS Y TEXTOS DE RUNAS ──────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

ICONO_RUNA_ATAQUE   = 'assets/logos/runas/Ataque.png'
ICONO_RUNA_MAGIA    = 'assets/logos/runas/Magia.png'
ICONO_RUNA_DEFENSA  = 'assets/logos/runas/Defensa.png'
ICONO_RUNA_DESTREZA = 'assets/logos/runas/Destreza.png'
ICONO_RUNA_ACERO    = 'assets/logos/runas/Acero.png'
ICONO_RUNA_CAZA     = 'assets/logos/runas/Caza.png'
ICONO_RUNA_SOMBRA   = 'assets/logos/runas/Sombras.png'
ICONO_RUNA_ARCANA   = 'assets/logos/runas/Arcana.png'
ICONO_RUNA_GUARDIAN = 'assets/logos/runas/Guardian.png'
ICONO_RUNA_ROTA     = 'assets/logos/runas/Rota.png'

RUNA_ICONOS = {
    'RUNA_ATAQUE':   ICONO_RUNA_ATAQUE,
    'RUNA_MAGIA':    ICONO_RUNA_MAGIA,
    'RUNA_DEFENSA':  ICONO_RUNA_DEFENSA,
    'RUNA_DESTREZA': ICONO_RUNA_DESTREZA,
    'RUNA_ACERO':    ICONO_RUNA_ACERO,
    'RUNA_CAZA':     ICONO_RUNA_CAZA,
    'RUNA_SOMBRA':   ICONO_RUNA_SOMBRA,
    'RUNA_ARCANA':   ICONO_RUNA_ARCANA,
    'RUNA_GUARDIAN': ICONO_RUNA_GUARDIAN,
    'RUNA_ROTA':     ICONO_RUNA_ROTA,
}

# Nombres bonitos de runas.
RUNA_NOMBRES_DISPLAY = {
    'RUNA_ATAQUE':   'Runa de Ataque',
    'RUNA_MAGIA':    'Runa de Magia',
    'RUNA_DEFENSA':  'Runa de Defensa',
    'RUNA_DESTREZA': 'Runa de Destreza',
    'RUNA_ACERO':    'Runa de Acero',
    'RUNA_CAZA':     'Runa de Caza',
    'RUNA_SOMBRA':   'Runa de Sombra',
    'RUNA_ARCANA':   'Runa Arcana',
    'RUNA_GUARDIAN': 'Runa de Guardián',
    'RUNA_ROTA':     'Runa Rota',
}

# Lore / descripción de cada runa.
RUNA_LORE = {
    'RUNA_ATAQUE': (
        'Símbolo grabado en piedra de guerra. '
        'Potencia la fuerza bruta de quien la porta, convirtiendo cada golpe '
        'en una sentencia inapelable.'
    ),
    'RUNA_MAGIA': (
        'Glifo arcano que amplifica el flujo de energía mágica de su portador. '
        'Los hechizos dejan de ser gestos para convertirse en voluntad pura.'
    ),
    'RUNA_DEFENSA': (
        'Escudo rúnico que endurece la piel y ralentiza los impactos más letales. '
        'Aquellos que la portan saben que resistir también es una forma de ganar.'
    ),
    'RUNA_DESTREZA': (
        'Inscripción que agudiza los reflejos y acelera cada movimiento de combate. '
        'Con ella, el portador parece moverse un instante antes de que el peligro llegue.'
    ),
    'RUNA_ACERO': (
        'Fusión de guerra y resistencia, forjada para quienes atacan '
        'sin dejar de cubrirse. Una sola runa que no entiende de medias tintas.'
    ),
    'RUNA_CAZA': (
        'Combina velocidad y fuerza bruta. '
        'Ideal para cazadores que no dan tregua y cierran la distancia '
        'antes de que el enemigo pueda reaccionar.'
    ),
    'RUNA_SOMBRA': (
        'Otorga la agilidad de las sombras y la resistencia de la oscuridad más profunda. '
        'Quienes la portan se mueven como si el mundo fuera apenas un obstáculo menor.'
    ),
    'RUNA_ARCANA': (
        'Convergencia de magia pura y escudo arcano. '
        'Protege tanto el cuerpo como el canal mágico, '
        'permitiendo lanzar hechizos incluso bajo el fuego más intenso.'
    ),
    'RUNA_GUARDIAN': (
        'El sello más antiguo de la orden. Sacrifica toda capacidad ofensiva '
        'a cambio de una defensa casi inexpugnable. '
        'Portarla es una declaración: yo no caigo.'
    ),
    'RUNA_ROTA': (
        'El resultado de una transmutación fallida. '
        'En lugar de potenciar, drena la resistencia de quien la porta. '
        'Solo los desesperados o los descuidados acaban con ella equipada.'
    ),
}


def icono_runa(nombre_db: str) -> str:
    return RUNA_ICONOS.get(nombre_db, PLACEHOLDER)

def nombre_runa(nombre_db: str) -> str:
    return RUNA_NOMBRES_DISPLAY.get(nombre_db, nombre_db)

def lore_runa(nombre_db: str) -> str:
    return RUNA_LORE.get(nombre_db, '')