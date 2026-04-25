from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line, Ellipse
from kivy.metrics import dp
from config import (
    FONDO_SELECCION, PANEL_OSCURO, PANEL_MEDIO,
    COLOR_ANOMALIAS, COLOR_GUARDIANES, BLANCO, GRIS
)
from widgets.componentes import BotonRedondeado


# ──────────────────────────────────────────────
#  Widget auxiliar: slot de ingrediente/resultado
# ──────────────────────────────────────────────
class SlotForja(Widget):
    """
    Cuadrado redondeado clicable que representa un slot de la forja.
    tipo: 'ingrediente' (borde dorado tenue) | 'resultado' (borde dorado brillante)
    """

    def __init__(self, tipo='ingrediente', etiqueta='', **kwargs):
        super().__init__(**kwargs)
        self.tipo = tipo
        self.etiqueta = etiqueta
        self.item = None  # guardará el item asignado
        self.bind(pos=self._redibujar, size=self._redibujar)

    def _redibujar(self, *args):
        self.canvas.clear()
        with self.canvas:
            # Fondo del slot
            if self.tipo == 'resultado':
                Color(0.1, 0.05, 0.15, 0.85)
            else:
                Color(0, 0, 0, 0.6)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])

            # Borde
            if self.tipo == 'resultado':
                Color(*COLOR_ANOMALIAS[:3], 0.8)
            else:
                Color(0.6, 0.45, 0.1, 0.6)
            Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, dp(10)),
                width=1.5
            )

        # Etiqueta de tipo (a / b)
        self.canvas.after.clear()
        # La etiqueta se pinta via Label hijo para no complicar el canvas
        self._actualizar_label()

    def _actualizar_label(self):
        # Elimina labels anteriores
        for child in list(self.children):
            self.remove_widget(child)

        if self.etiqueta:
            lbl = Label(
                text=self.etiqueta,
                font_size=dp(14),
                bold=True,
                color=(0.9, 0.75, 0.3, 0.7),
                pos=self.pos,
                size=self.size,
                halign='center',
                valign='middle'
            )
            lbl.text_size = lbl.size
            lbl.bind(size=lbl.setter('text_size'))
            self.add_widget(lbl)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return True
        return super().on_touch_down(touch)


# ──────────────────────────────────────────────
#  Pantalla principal de la Forja
# ──────────────────────────────────────────────
class PantallaForja(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ── Fondo ──────────────────────────────
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self._bg_rect = Rectangle(source=FONDO_SELECCION, pos=self.pos, size=self.size)
        self.bind(pos=self._actualizarFondo, size=self._actualizarFondo)

        # Overlay oscuro
        overlayWidget = Widget(size_hint=(1, 1))
        with overlayWidget.canvas:
            Color(0, 0, 0, 0.6)
            self._overlay = Rectangle(pos=overlayWidget.pos, size=overlayWidget.size)
        overlayWidget.bind(
            pos=lambda *a: setattr(self._overlay, 'pos', overlayWidget.pos),
            size=lambda *a: setattr(self._overlay, 'size', overlayWidget.size)
        )

        # ── Contenedor principal ────────────────
        contenedorPrincipal = BoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(8)
        )

        # ── Título ──────────────────────────────
        cajaTitulo = BoxLayout(
            size_hint=(1, None),
            height=dp(44),
            padding=[dp(8), dp(4)]
        )
        with cajaTitulo.canvas.before:
            Color(0, 0, 0, 0.6)
            self._titleRect = RoundedRectangle(pos=cajaTitulo.pos, size=cajaTitulo.size, radius=[dp(8)])
            Color(0.6, 0.45, 0.1, 0.5)
            self._titleBorde = Line(
                rounded_rectangle=(cajaTitulo.x, cajaTitulo.y, cajaTitulo.width, cajaTitulo.height, dp(8)),
                width=1.2
            )
        cajaTitulo.bind(
            pos=lambda *a: self._actualizarCaja(cajaTitulo, self._titleRect, self._titleBorde),
            size=lambda *a: self._actualizarCaja(cajaTitulo, self._titleRect, self._titleBorde)
        )
        etiquetaTitulo = Label(
            text='— FORJA —',
            font_size=dp(18),
            bold=True,
            color=(0.9, 0.75, 0.3, 1),
            size_hint=(1, 1),
            halign='center',
            valign='middle'
        )
        etiquetaTitulo.bind(size=etiquetaTitulo.setter('text_size'))
        cajaTitulo.add_widget(etiquetaTitulo)
        contenedorPrincipal.add_widget(cajaTitulo)

        # ── Panel central de combinación ─────────
        panelCombinacion = FloatLayout(size_hint=(1, 1))
        with panelCombinacion.canvas.before:
            Color(0, 0, 0, 0.5)
            self._panelRect = RoundedRectangle(
                pos=panelCombinacion.pos, size=panelCombinacion.size, radius=[dp(12)]
            )
            Color(0.6, 0.45, 0.1, 0.35)
            self._panelBorde = Line(
                rounded_rectangle=(
                    panelCombinacion.x, panelCombinacion.y,
                    panelCombinacion.width, panelCombinacion.height, dp(12)
                ),
                width=1.0
            )
        panelCombinacion.bind(
            pos=lambda *a: self._actualizarPanel(panelCombinacion),
            size=lambda *a: self._actualizarPanel(panelCombinacion)
        )

        # Slot resultado (a) — centro
        self.slotResultado = SlotForja(
            tipo='resultado',
            etiqueta='a',
            size_hint=(None, None),
            size=(dp(80), dp(80)),
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        # Slot ingrediente 1 (b) — arriba derecha
        self.slotIng1 = SlotForja(
            tipo='ingrediente',
            etiqueta='b',
            size_hint=(None, None),
            size=(dp(70), dp(70)),
            pos_hint={'center_x': 0.75, 'center_y': 0.72}
        )

        # Slot ingrediente 2 (b) — abajo centro-izquierda
        self.slotIng2 = SlotForja(
            tipo='ingrediente',
            etiqueta='b',
            size_hint=(None, None),
            size=(dp(70), dp(70)),
            pos_hint={'center_x': 0.42, 'center_y': 0.32}
        )

        # Etiqueta de instrucción
        etiquetaInfo = Label(
            text='Selecciona dos ingredientes\npara combinar',
            font_size=dp(10),
            color=(0.7, 0.65, 0.5, 0.9),
            size_hint=(0.9, None),
            height=dp(30),
            pos_hint={'center_x': 0.5, 'top': 0.18},
            halign='center',
            valign='middle'
        )
        etiquetaInfo.bind(size=etiquetaInfo.setter('text_size'))

        panelCombinacion.add_widget(self.slotIng1)
        panelCombinacion.add_widget(self.slotIng2)
        panelCombinacion.add_widget(self.slotResultado)
        panelCombinacion.add_widget(etiquetaInfo)

        # Etiqueta de flechas decorativas (dibujadas sobre el panel)
        self._flechaLabel = Label(
            text='→',
            font_size=dp(22),
            color=(0.9, 0.75, 0.3, 0.6),
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            pos_hint={'center_x': 0.62, 'center_y': 0.64}
        )
        panelCombinacion.add_widget(self._flechaLabel)

        self._flechaLabel2 = Label(
            text='↗',
            font_size=dp(22),
            color=(0.9, 0.75, 0.3, 0.6),
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            pos_hint={'center_x': 0.47, 'center_y': 0.44}
        )
        panelCombinacion.add_widget(self._flechaLabel2)

        contenedorPrincipal.add_widget(panelCombinacion)

        # ── Barra inferior ───────────────────────
        barraInferior = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(60),
            spacing=dp(8),
            padding=[dp(10), dp(8)]
        )
        with barraInferior.canvas.before:
            Color(0, 0, 0, 0.85)
            self._rectBarraInf = RoundedRectangle(
                pos=barraInferior.pos,
                size=barraInferior.size,
                radius=[dp(20), dp(20), 0, 0]
            )
        barraInferior.bind(
            pos=lambda *a: setattr(self._rectBarraInf, 'pos', barraInferior.pos),
            size=lambda *a: setattr(self._rectBarraInf, 'size', barraInferior.size)
        )

        botonAtras = BotonRedondeado(
            text='ATRÁS',
            bg_color=(0.05, 0.05, 0.1, 0.9),
            text_color=(0.9, 0.75, 0.3, 1),
            radius=8,
            size_hint=(1, 1),
            font_size=dp(11),
            bold=True
        )
        botonAtras.bind(on_press=self.volverAInventario)

        # Botón circular central de forjar
        self.botonForjar = BotonRedondeado(
            text='⚒',
            bg_color=(*COLOR_ANOMALIAS[:3], 0.85),
            text_color=BLANCO,
            radius=50,          # muy redondeado → círculo
            size_hint=(None, 1),
            width=dp(54),
            font_size=dp(22),
            bold=True
        )
        self.botonForjar.bind(on_press=self.intentarForja)

        botonCargas = BotonRedondeado(
            text='Nº CARGAS',
            bg_color=(0.05, 0.05, 0.1, 0.9),
            text_color=(*COLOR_GUARDIANES[:3], 1),
            radius=8,
            size_hint=(1, 1),
            font_size=dp(11),
            bold=True
        )
        botonCargas.bind(on_press=self.mostrarCargas)

        barraInferior.add_widget(botonAtras)
        barraInferior.add_widget(self.botonForjar)
        barraInferior.add_widget(botonCargas)
        contenedorPrincipal.add_widget(barraInferior)

        self.add_widget(overlayWidget)
        self.add_widget(contenedorPrincipal)

    # ── Helpers de canvas ──────────────────────

    def _actualizarCaja(self, widget, rect, borde):
        rect.pos  = widget.pos
        rect.size = widget.size
        borde.rounded_rectangle = (
            widget.x, widget.y, widget.width, widget.height, dp(10)
        )

    def _actualizarPanel(self, panel):
        self._panelRect.pos  = panel.pos
        self._panelRect.size = panel.size
        self._panelBorde.rounded_rectangle = (
            panel.x, panel.y, panel.width, panel.height, dp(12)
        )

    def _actualizarFondo(self, *args):
        self._bg_rect.pos  = self.pos
        self._bg_rect.size = self.size

    # ── Lógica de forja ────────────────────────

    def intentarForja(self, instance):
        """
        Aquí irá la lógica real cuando esté conectada a la base de datos.
        Por ahora imprime el estado de los slots.
        """
        ing1 = self.slotIng1.item
        ing2 = self.slotIng2.item
        print(f'[Forja] Intentando combinar: {ing1} + {ing2}')
        if ing1 and ing2:
            # TODO: llamar al sistema de recetas y rellenar slotResultado
            pass
        else:
            print('[Forja] Faltan ingredientes')

    def mostrarCargas(self, instance):
        """Mostrará las cargas disponibles de forja (pendiente de BD)."""
        print('[Forja] Mostrando cargas disponibles')

    def volverAInventario(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'inventario'