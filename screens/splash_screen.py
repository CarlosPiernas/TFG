from kivy.uix.screenmanager import Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from widgets.responsive import sw, sh, sf, sdp
from config import FONDO_SPLASH, COLOR_ANOMALIAS, COLOR_GUARDIANES
import random


class PantallaSplash(Screen):
    def __init__(self, gm=None, **kwargs):
        super().__init__(**kwargs)
        self.gm = gm
        self._tick_event = None
        self._progreso = 0.0
        self._touch_ready = False

        with self.canvas.before:
            Color(0, 0, 0, 1)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._upd_bg, size=self._upd_bg)

        self.layout = FloatLayout()

        # 1. Fondo primero (capa más baja)
        self.fondo = Image(
            source=FONDO_SPLASH,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )

        # 2. Barra bg
        self.barra_bg = Widget(
            size_hint=(0.75, None),
            height=dp(10),
            pos_hint={'center_x': 0.5, 'y': 0.06}
        )
        with self.barra_bg.canvas:
            Color(0.15, 0.15, 0.15, 0.8)
            self._barra_bg_rect = RoundedRectangle(
                pos=self.barra_bg.pos,
                size=self.barra_bg.size,
                radius=[dp(5)]
            )
        self.barra_bg.bind(
            pos=lambda *a: setattr(self._barra_bg_rect, 'pos', self.barra_bg.pos),
            size=lambda *a: setattr(self._barra_bg_rect, 'size', self.barra_bg.size)
        )

        # 3. Barra fill
        self._color_barra = random.choice([COLOR_ANOMALIAS, COLOR_GUARDIANES])
        self.barra_fill = Widget(
            size_hint=(None, None),
            height=dp(10),
            width=0,
        )
        with self.barra_fill.canvas:
            self._color_inst = Color(*self._color_barra)
            self._barra_rect = RoundedRectangle(
                pos=self.barra_fill.pos,
                size=self.barra_fill.size,
                radius=[dp(5)]
            )
        self.barra_fill.bind(
            pos=lambda *a: setattr(self._barra_rect, 'pos', self.barra_fill.pos),
            size=lambda *a: setattr(self._barra_rect, 'size', self.barra_fill.size)
        )

        # 4. Tap label (capa más alta)
        self.tap_label = Label(
            text='TOCA PARA CONTINUAR',
            font_size=sf(11),
            color=(1, 1, 1, 0.6),
            size_hint=(1, None),
            height=sh(20),
            pos_hint={'center_x': 0.5, 'y': 0.02},
            opacity=0
        )

        self.layout.add_widget(self.fondo)
        self.layout.add_widget(self.barra_bg)
        self.layout.add_widget(self.barra_fill)
        self.layout.add_widget(self.tap_label)
        self.add_widget(self.layout)

    def _upd_bg(self, *args):
        self._bg.pos  = self.pos
        self._bg.size = self.size

    def on_enter(self, *args):
        self._progreso = 0.0
        self._touch_ready = False
        self._color_barra = random.choice([COLOR_ANOMALIAS, COLOR_GUARDIANES])
        self._color_inst.rgba = self._color_barra
        self._actualizar_barra()
        self._tick_event = Clock.schedule_once(self._tick, random.uniform(0.3, 0.6))

    def on_leave(self, *args):
        if self._tick_event:
            self._tick_event.cancel()
            self._tick_event = None
        Animation.cancel_all(self.tap_label)
        self._touch_ready = False
        self.tap_label.opacity = 0

    def _tick(self, dt):
        incremento = random.uniform(0.08, 0.22)
        self._progreso = min(self._progreso + incremento, 1.0)
        self._actualizar_barra()

        if self._progreso >= 1.0:
            Clock.schedule_once(self._mostrar_tap, 0.3)
        else:
            self._tick_event = Clock.schedule_once(self._tick, random.uniform(0.25, 0.55))

    def _actualizar_barra(self):
        def _upd(dt):
            bg_x = self.barra_bg.x
            bg_w = self.barra_bg.width
            fill_w = bg_w * self._progreso
            self.barra_fill.x      = bg_x
            self.barra_fill.width  = max(fill_w, dp(5))
            self.barra_fill.y      = self.barra_bg.y
            self.barra_fill.height = self.barra_bg.height
        Clock.schedule_once(_upd, 0)

    def _mostrar_tap(self, dt):
        self._touch_ready = True
        self.tap_label.opacity = 1
        blink = (
            Animation(opacity=0.15, duration=0.7, t='in_out_sine') +
            Animation(opacity=0.65, duration=0.7, t='in_out_sine')
        )
        blink.repeat = True
        blink.start(self.tap_label)

    def on_touch_down(self, touch):
        if not self._touch_ready:
            return super().on_touch_down(touch)
        self._navegar()
        return True

    def _navegar(self, dt=None):
        destino = 'principal' if (self.gm and self.gm.faccion) else 'seleccion'
        self.manager.transition = FadeTransition(duration=0.4)
        self.manager.current = destino