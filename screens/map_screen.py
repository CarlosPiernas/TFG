# =============================================================================
# screens/map_screen.py
# Pantalla del mapa — Sprint 2
# Nodos estilo Candy Crush con estetica oscura y siniestra.
# Incluye modo Hard que cambia el aspecto visual de los nodos.
# =============================================================================

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.metrics import dp

from config import FONDO_SELECCION
from widgets.componentes import BotonRedondeado

# ── Datos de los nodos ────────────────────────────────────────────────────────
NODOS = [
    {'nombre': 'ENTRADA',    'icono': 'I',   'jefe': False},
    {'nombre': 'PASAJE',     'icono': 'II',  'jefe': False},
    {'nombre': 'CRIPTA',     'icono': 'III', 'jefe': False},
    {'nombre': 'ABISMO',     'icono': 'IV',  'jefe': False},
    {'nombre': 'JEFE FINAL', 'icono': 'V',   'jefe': True },
]

# Posiciones de cada nodo en porcentaje de pantalla (x, y)
POSICIONES = [
    (0.5,  0.13),
    (0.25, 0.30),
    (0.65, 0.47),
    (0.30, 0.63),
    (0.5,  0.80),
]

# ── Paleta modo NORMAL ────────────────────────────────────────────────────────
NORMAL_NODO_BLOQUEADO_FONDO  = (0.08, 0.08, 0.12, 0.92)
NORMAL_NODO_BLOQUEADO_BORDE  = (0.25, 0.25, 0.35, 1)
NORMAL_NODO_BLOQUEADO_TEXTO  = (0.4,  0.4,  0.5,  1)

NORMAL_NODO_LIBRE_FONDO      = (0.15, 0.05, 0.25, 0.95)
NORMAL_NODO_LIBRE_BORDE      = (0.6,  0.2,  0.85, 1)
NORMAL_NODO_LIBRE_TEXTO      = (0.8,  0.4,  1.0,  1)

NORMAL_NODO_JEFE_FONDO       = (0.35, 0.08, 0.0,  0.95)
NORMAL_NODO_JEFE_BORDE       = (0.85, 0.55, 0.0,  1)
NORMAL_NODO_JEFE_BORDE2      = (1.0,  0.8,  0.1,  1)
NORMAL_NODO_JEFE_TEXTO       = (1.0,  0.8,  0.1,  1)

NORMAL_LINEA_SOMBRA          = (0,    0,    0,    0.7)
NORMAL_LINEA_COLOR           = (0.45, 0.2,  0.6,  0.9)

NORMAL_ETIQUETA_JEFE         = (0.9,  0.75, 0.3,  1)
NORMAL_ETIQUETA_NODO         = (0.75, 0.75, 0.75, 1)

# ── Paleta modo HARD ─────────────────────────────────────────────────────────
# Todo se vuelve rojizo, oscuro y amenazante
HARD_NODO_BLOQUEADO_FONDO    = (0.12, 0.02, 0.02, 0.95)
HARD_NODO_BLOQUEADO_BORDE    = (0.35, 0.08, 0.08, 1)
HARD_NODO_BLOQUEADO_TEXTO    = (0.35, 0.1,  0.1,  1)

HARD_NODO_LIBRE_FONDO        = (0.35, 0.04, 0.04, 0.95)
HARD_NODO_LIBRE_BORDE        = (0.85, 0.15, 0.15, 1)
HARD_NODO_LIBRE_TEXTO        = (1.0,  0.4,  0.4,  1)

HARD_NODO_JEFE_FONDO         = (0.25, 0.02, 0.02, 0.98)
HARD_NODO_JEFE_BORDE         = (0.9,  0.05, 0.05, 1)
HARD_NODO_JEFE_BORDE2        = (1.0,  0.3,  0.0,  1)
HARD_NODO_JEFE_TEXTO         = (1.0,  0.3,  0.1,  1)

HARD_LINEA_SOMBRA            = (0.2,  0.0,  0.0,  0.8)
HARD_LINEA_COLOR             = (0.7,  0.1,  0.1,  0.9)

HARD_ETIQUETA_JEFE           = (1.0,  0.3,  0.1,  1)
HARD_ETIQUETA_NODO           = (0.75, 0.3,  0.3,  1)

# ── Colores del boton de dificultad ──────────────────────────────────────────
BOTON_HARD_FONDO    = (0.55, 0.05, 0.05, 1)
BOTON_HARD_BORDE    = (0.85, 0.15, 0.15, 1)
BOTON_HARD_TEXTO    = (1.0,  0.85, 0.85, 1)

BOTON_NORMAL_FONDO  = (0.08, 0.08, 0.15, 1)
BOTON_NORMAL_BORDE  = (0.35, 0.35, 0.55, 1)
BOTON_NORMAL_TEXTO  = (0.7,  0.7,  0.85, 1)


class _NodoWidget(Widget):
    """
    Widget que representa un nodo del mapa.
    Acepta una paleta de colores para poder cambiar entre modo normal y hard.
    """
    def __init__(self, icono, jefe=False, desbloqueado=False, paleta=None, **kwargs):
        super().__init__(**kwargs)
        self.icono        = icono
        self.jefe         = jefe
        self.desbloqueado = desbloqueado
        self.paleta       = paleta or 'normal'
        self.bind(pos=self._dibujar, size=self._dibujar)

    def cambiarPaleta(self, paleta):
        # Cambia la paleta de colores y redibuja el nodo
        self.paleta = paleta
        self._dibujar()

    def _dibujar(self, *args):
        self.canvas.clear()
        x, y = self.pos
        w, h = self.size
        cx, cy = x + w / 2, y + h / 2
        r = min(w, h) / 2

        # Selecciona la paleta correcta segun el modo
        p = HARD_NODO_JEFE_FONDO if self.paleta == 'hard' else NORMAL_NODO_JEFE_FONDO

        with self.canvas:
            if self.jefe:
                fondo  = HARD_NODO_JEFE_FONDO  if self.paleta == 'hard' else NORMAL_NODO_JEFE_FONDO
                borde1 = HARD_NODO_JEFE_BORDE  if self.paleta == 'hard' else NORMAL_NODO_JEFE_BORDE
                borde2 = HARD_NODO_JEFE_BORDE2 if self.paleta == 'hard' else NORMAL_NODO_JEFE_BORDE2
                Color(*fondo)
                Ellipse(pos=(x, y), size=(w, h))
                Color(*borde1)
                Line(circle=(cx, cy, r - dp(3)), width=2.5)
                Color(*borde2)
                Line(circle=(cx, cy, r - dp(8)), width=1.2)
            elif self.desbloqueado:
                fondo  = HARD_NODO_LIBRE_FONDO  if self.paleta == 'hard' else NORMAL_NODO_LIBRE_FONDO
                borde  = HARD_NODO_LIBRE_BORDE  if self.paleta == 'hard' else NORMAL_NODO_LIBRE_BORDE
                Color(*fondo)
                Ellipse(pos=(x, y), size=(w, h))
                Color(*borde)
                Line(circle=(cx, cy, r - dp(3)), width=2.0)
            else:
                fondo  = HARD_NODO_BLOQUEADO_FONDO  if self.paleta == 'hard' else NORMAL_NODO_BLOQUEADO_FONDO
                borde  = HARD_NODO_BLOQUEADO_BORDE  if self.paleta == 'hard' else NORMAL_NODO_BLOQUEADO_BORDE
                Color(*fondo)
                Ellipse(pos=(x, y), size=(w, h))
                Color(*borde)
                Line(circle=(cx, cy, r - dp(3)), width=1.5)

        # Etiqueta con el icono del nodo
        for child in self.children[:]:
            self.remove_widget(child)

        if self.jefe:
            colorTexto = HARD_NODO_JEFE_TEXTO  if self.paleta == 'hard' else NORMAL_NODO_JEFE_TEXTO
        elif self.desbloqueado:
            colorTexto = HARD_NODO_LIBRE_TEXTO if self.paleta == 'hard' else NORMAL_NODO_LIBRE_TEXTO
        else:
            colorTexto = HARD_NODO_BLOQUEADO_TEXTO if self.paleta == 'hard' else NORMAL_NODO_BLOQUEADO_TEXTO

        lbl = Label(
            text=self.icono,
            font_size=dp(18) if self.jefe else dp(13),
            bold=True,
            color=colorTexto,
            pos=self.pos,
            size=self.size,
            halign='center',
            valign='middle'
        )
        lbl.bind(size=lbl.setter('text_size'))
        self.add_widget(lbl)


class _LineasConexion(Widget):
    """
    Widget que dibuja las lineas que conectan los nodos del mapa.
    Tambien cambia de color segun el modo de dificultad.
    """
    def __init__(self, posiciones, paleta='normal', **kwargs):
        super().__init__(**kwargs)
        self.posiciones = posiciones
        self.paleta     = paleta
        self.bind(pos=self._dibujar, size=self._dibujar)

    def cambiarPaleta(self, paleta):
        self.paleta = paleta
        self._dibujar()

    def _dibujar(self, *args):
        self.canvas.clear()
        w, h = self.size
        x0, y0 = self.pos

        sombra = HARD_LINEA_SOMBRA if self.paleta == 'hard' else NORMAL_LINEA_SOMBRA
        color  = HARD_LINEA_COLOR  if self.paleta == 'hard' else NORMAL_LINEA_COLOR

        with self.canvas:
            for i in range(len(self.posiciones) - 1):
                px1, py1 = self.posiciones[i]
                px2, py2 = self.posiciones[i + 1]
                x1 = x0 + px1 * w
                y1 = y0 + py1 * h
                x2 = x0 + px2 * w
                y2 = y0 + py2 * h
                Color(*sombra)
                Line(points=[x1, y1, x2, y2], width=dp(3))
                Color(*color)
                Line(points=[x1, y1, x2, y2], width=dp(1.5))


class _BotonOvalo(Widget):
    """
    Boton con forma de ovalo dibujado en canvas.
    Detecta toques dentro del area del ovalo matematicamente.
    Cambia su texto y colores al pulsarlo para indicar el modo activo.
    """
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback  = callback
        self.modoHard  = False
        self.bind(pos=self._dibujar, size=self._dibujar)

    def _dibujar(self, *args):
        self.canvas.clear()
        x, y = self.pos
        w, h = self.size

        fondo  = BOTON_HARD_FONDO   if not self.modoHard else BOTON_NORMAL_FONDO
        borde  = BOTON_HARD_BORDE   if not self.modoHard else BOTON_NORMAL_BORDE
        texto  = 'HARD'             if not self.modoHard else 'NORMAL'
        colorT = BOTON_HARD_TEXTO   if not self.modoHard else BOTON_NORMAL_TEXTO

        with self.canvas:
            Color(*fondo)
            Ellipse(pos=(x, y), size=(w, h))
            Color(*borde)
            Line(ellipse=(x, y, w, h), width=dp(2))

        for child in self.children[:]:
            self.remove_widget(child)

        lbl = Label(
            text=texto,
            font_size=dp(12),
            bold=True,
            color=colorT,
            pos=self.pos,
            size=self.size,
            halign='center',
            valign='middle'
        )
        lbl.bind(size=lbl.setter('text_size'))
        self.add_widget(lbl)

    def on_touch_down(self, touch):
        # Comprueba si el toque cae dentro del ovalo usando la formula de la elipse
        x, y = self.pos
        w, h = self.size
        cx, cy = x + w / 2, y + h / 2
        rx, ry = w / 2, h / 2
        dx = (touch.x - cx) / rx
        dy = (touch.y - cy) / ry
        if dx * dx + dy * dy <= 1:
            self.modoHard = not self.modoHard
            self._dibujar()
            self.callback(self.modoHard)
            return True
        return super().on_touch_down(touch)


class PantallaMapa(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fondo con imagen
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self._bg_rect = Rectangle(source=FONDO_SELECCION, pos=self.pos, size=self.size)
        self.bind(pos=self._actualizarFondo, size=self._actualizarFondo)

        raiz = FloatLayout()

        # Overlay oscuro encima del fondo
        overlayWidget = Widget(size_hint=(1, 1))
        with overlayWidget.canvas:
            Color(0, 0, 0, 0.45)
            self._overlay = Rectangle(pos=overlayWidget.pos, size=overlayWidget.size)
        overlayWidget.bind(
            pos=lambda *a: setattr(self._overlay, 'pos', overlayWidget.pos),
            size=lambda *a: setattr(self._overlay, 'size', overlayWidget.size)
        )
        raiz.add_widget(overlayWidget)

        # Lineas de conexion — se guardan para poder cambiar su paleta
        self.lineasConexion = _LineasConexion(
            POSICIONES, paleta='normal',
            size_hint=(1, 1), pos_hint={'x': 0, 'y': 0}
        )
        raiz.add_widget(self.lineasConexion)

        # Titulo
        titulo = Label(
            text='— CAMPAÑA —',
            font_size=dp(22),
            bold=True,
            color=(0.9, 0.75, 0.3, 1),
            size_hint=(1, None),
            height=dp(50),
            pos_hint={'x': 0, 'top': 0.97},
            halign='center',
            valign='middle'
        )
        titulo.bind(size=titulo.setter('text_size'))
        raiz.add_widget(titulo)

        # Nodos — se guardan en lista para poder cambiar su paleta despues
        self.listaNodos     = []
        self.listaEtiquetas = []

        for i, (datos, (px, py)) in enumerate(zip(NODOS, POSICIONES)):
            jefe = datos['jefe']
            tam  = dp(75) if jefe else dp(55)

            nodo = _NodoWidget(
                icono=datos['icono'],
                jefe=jefe,
                desbloqueado=(i == 0),
                paleta='normal',
                size_hint=(None, None),
                size=(tam, tam),
                pos_hint={'center_x': px, 'center_y': py}
            )
            raiz.add_widget(nodo)
            self.listaNodos.append(nodo)

            etiqueta = Label(
                text=datos['nombre'],
                font_size=dp(9),
                bold=jefe,
                color=NORMAL_ETIQUETA_JEFE if jefe else NORMAL_ETIQUETA_NODO,
                size_hint=(None, None),
                size=(dp(90), dp(18)),
                pos_hint={'center_x': px, 'center_y': py - 0.07},
                halign='center',
                valign='middle'
            )
            etiqueta.bind(size=etiqueta.setter('text_size'))
            raiz.add_widget(etiqueta)
            self.listaEtiquetas.append((etiqueta, jefe))

        # Boton volver — parte inferior izquierda
        botonVolver = BotonRedondeado(
            text='VOLVER',
            bg_color=(0.05, 0.05, 0.1, 0.9),
            text_color=(0.9, 0.75, 0.3, 1),
            radius=8,
            size_hint=(None, None),
            size=(dp(100), dp(36)),
            pos_hint={'x': 0.04, 'y': 0.02},
            font_size=dp(12),
            bold=True
        )
        botonVolver.bind(on_press=lambda _: self.navegarA('principal'))
        raiz.add_widget(botonVolver)

        # Boton Hard/Normal — parte derecha central, forma de ovalo
        self.botonDificultad = _BotonOvalo(
            callback=self.cambiarDificultad,
            size_hint=(None, None),
            size=(dp(80), dp(44)),
            pos_hint={'right': 0.96, 'center_y': 0.47}
        )
        raiz.add_widget(self.botonDificultad)

        self.add_widget(raiz)

    def cambiarDificultad(self, modoHard):
        """
        Cambia la paleta visual de todos los nodos y lineas del mapa.
        Cuando modoHard es True todo se vuelve rojizo y amenazante.
        Cuando es False vuelve a los colores normales purpura/dorado.
        TODO: avisar a M2 del modo activo para cargar enemigos correctos.
        """
        paleta = 'hard' if modoHard else 'normal'

        # Cambia todos los nodos
        for nodo in self.listaNodos:
            nodo.cambiarPaleta(paleta)

        # Cambia las lineas de conexion
        self.lineasConexion.cambiarPaleta(paleta)

        # Cambia el color de las etiquetas de nombre
        for etiqueta, jefe in self.listaEtiquetas:
            if modoHard:
                etiqueta.color = HARD_ETIQUETA_JEFE if jefe else HARD_ETIQUETA_NODO
            else:
                etiqueta.color = NORMAL_ETIQUETA_JEFE if jefe else NORMAL_ETIQUETA_NODO

    def _actualizarFondo(self, *args):
        self._bg_rect.pos  = self.pos
        self._bg_rect.size = self.size

    def navegarA(self, pantalla):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = pantalla