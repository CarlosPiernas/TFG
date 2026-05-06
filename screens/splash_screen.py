from kivy.uix.screenmanager import Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from widgets.responsive import sw, sh, sf, sdp


class PantallaSplash(Screen):
    def __init__(self, gm=None, **kwargs):
        super().__init__(**kwargs)
        self.gm = gm
        self._auto_event = None
        self._touch_ready = False

        # Fondo negro puro
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._upd_bg, size=self._upd_bg)

        self.layout = FloatLayout()

        # Logo del juego centrado en la parte superior
        self.logo = Image(
            source='assets/logos/Logo_Juego.png',
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(0.7, 0.35),
            pos_hint={'center_x': 0.5, 'top': 0.88},
            opacity=0
        )

        # Subtítulo
        self.subtitulo = Label(
            text='ANOMALÍAS vs GUARDIANES\nDEL ESPACIO TIEMPO',
            font_size=sf(14),
            bold=True,
            color=(0.85, 0.75, 1, 1),
            halign='center',
            valign='middle',
            size_hint=(1, None),
            height=sh(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.47},
            opacity=0
        )
        self.subtitulo.bind(size=self.subtitulo.setter('text_size'))

        # Label de toque
        self.tap_label = Label(
            text='TOCA PARA CONTINUAR',
            font_size=sf(11),
            color=(1, 1, 1, 0.6),
            size_hint=(1, None),
            height=sh(20),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            opacity=0
        )

        self.layout.add_widget(self.logo)
        self.layout.add_widget(self.subtitulo)
        self.layout.add_widget(self.tap_label)
        self.add_widget(self.layout)

    def _upd_bg(self, *args):
        self._bg.pos = self.pos
        self._bg.size = self.size

    # ── Ciclo de vida ─────────────────────────────────────────────────────────

    def on_enter(self, *args):
        self._touch_ready = False
        Clock.schedule_once(self._animar_entrada, 0.3)

    def on_leave(self, *args):
        if self._auto_event:
            self._auto_event.cancel()
            self._auto_event = None
        Animation.cancel_all(self.tap_label)

    # ── Animaciones ───────────────────────────────────────────────────────────

    def _animar_entrada(self, dt):
        # Logo aparece primero
        Animation(opacity=1, duration=1.0, t='in_out_quad').start(self.logo)
        # Subtítulo medio segundo después
        Clock.schedule_once(self._mostrar_subtitulo, 0.5)

    def _mostrar_subtitulo(self, dt):
        Animation(opacity=1, duration=0.8, t='in_out_quad').start(self.subtitulo)
        Clock.schedule_once(self._mostrar_tap, 0.8)

    def _mostrar_tap(self, dt):
        self.tap_label.opacity = 1
        # Parpadeo en bucle
        blink = (
            Animation(opacity=0.15, duration=0.7, t='in_out_sine') +
            Animation(opacity=0.65, duration=0.7, t='in_out_sine')
        )
        blink.repeat = True
        blink.start(self.tap_label)

        self._touch_ready = True
        # Auto-avance a los 5 segundos
        self._auto_event = Clock.schedule_once(self._navegar, 5.0)

    # ── Navegación ────────────────────────────────────────────────────────────

    def on_touch_down(self, touch):
        if not self._touch_ready:
            return super().on_touch_down(touch)
        self._navegar()
        return True

    def _navegar(self, dt=None):
        if self._auto_event:
            self._auto_event.cancel()
            self._auto_event = None

        # Si ya hay facción registrada → home directamente
        # Si no → pantalla de selección de facción
        destino = 'principal' if (self.gm and self.gm.faccion) else 'seleccion'

        # Fade out del layout y luego cambia de pantalla
        anim = Animation(opacity=0, duration=0.4, t='in_out_quad')
        anim.bind(on_complete=lambda *_: self._cambiar(destino))
        anim.start(self.layout)

    def _cambiar(self, destino):
        self.manager.transition = FadeTransition(duration=0.3)
        self.manager.current = destino