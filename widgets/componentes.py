from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

from config import PANEL_OSCURO, PANEL_MEDIO, BLANCO

class PanelRedondeado(Widget):
    def __init__(self, bg_color=PANEL_OSCURO, radius=10, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        self.radius = radius
        self.bind(pos=self.redibujarFondo, size=self.redibujarFondo)

    def redibujarFondo(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size,
                             radius=[dp(self.radius)])


class BotonRedondeado(Button):
    def __init__(self, bg_color=PANEL_MEDIO, text_color=BLANCO,
                 radius=10, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color  = (0, 0, 0, 0)
        self.color             = text_color
        self.bold              = True
        self._bg_color         = bg_color
        self._radius           = radius
        self.bind(pos=self.redibujarFondo, size=self.redibujarFondo)

    def redibujarFondo(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self._bg_color)
            RoundedRectangle(pos=self.pos, size=self.size,
                             radius=[dp(self._radius)])