from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from config import (
    FONDO_PRINCIPAL, PANEL_MEDIO, COLOR_ANOMALIAS, COLOR_GUARDIANES,
    BLANCO, LOGO_ANOMALIA, LOGO_GUARDIAN,
    SPRITE_ANOMALIA, SPRITE_GUARDIAN,
    NOMBRE_ANOMALIA, NOMBRE_GUARDIAN,
    FONDO_SELECCION
)
from widgets.componentes import BotonRedondeado

class PantallaSeleccion(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self._bg_rect = Rectangle(
                source=FONDO_SELECCION,
                pos=self.pos,
                size=self.size
            )
        self.bind(pos=self.actualizarFondo, size=self.actualizarFondo)
        contenedorPrincipal = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(10)
        )
        titulo = Label(
            text='ELIJA SU FACCIÓN',
            font_size=dp(28),
            bold=True,
            color=BLANCO,
            size_hint=(1, None),
            height=dp(60),
            halign='center',
            valign='middle'
        )
        titulo.bind(size=titulo.setter('text_size'))
        filaLogos = GridLayout(
            cols=2,
            spacing=dp(20),
            size_hint=(1, 0.7),
        )
        imgLogoGuardianes = Image(
            source=LOGO_GUARDIAN,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1)
        )
        imgLogoAnomalias = Image(
            source=LOGO_ANOMALIA,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1)
        )
        botonElegirGuardianes = BotonRedondeado(
            text='ELEGIR GUARDIANES',
            bg_color=PANEL_MEDIO,
            text_color=COLOR_GUARDIANES,
            radius=10,
            size_hint=(None, None),
            size=(dp(220), dp(50)),
            pos_hint={'center_x': 0.5},
            font_size=dp(14),
            bold=True
        )
        botonElegirGuardianes.bind(
            on_press=lambda _: self.elegirFaccion(NOMBRE_GUARDIAN, SPRITE_GUARDIAN, COLOR_GUARDIANES)
        )
        filaLogos.add_widget(imgLogoGuardianes)
        filaLogos.add_widget(imgLogoAnomalias)
        espaciador = Widget(size_hint=(1, None), height=dp(10))
        botonElegirAnomalias = BotonRedondeado(
            text='ELEGIR ANOMALÍAS',
            bg_color=PANEL_MEDIO,
            text_color=COLOR_ANOMALIAS,
            radius=10,
            size_hint=(None, None),
            size=(dp(220), dp(50)),
            pos_hint={'center_x': 0.5},
            font_size=dp(14),
            bold=True
        )
        botonElegirAnomalias.bind(
            on_press=lambda _: self.elegirFaccion(NOMBRE_ANOMALIA, SPRITE_ANOMALIA, COLOR_ANOMALIAS)
        )
        
        contenedorPrincipal.add_widget(titulo)
        contenedorPrincipal.add_widget(filaLogos)
        contenedorPrincipal.add_widget(espaciador)
        contenedorPrincipal.add_widget(botonElegirGuardianes)
        contenedorPrincipal.add_widget(botonElegirAnomalias)
        contenedorPrincipal.add_widget(Widget(size_hint=(1, None), height=dp(20)))
        self.add_widget(contenedorPrincipal)

    def actualizarFondo(self, *args):
        self._bg_rect.pos  = self.pos
        self._bg_rect.size = self.size
        self._bg_rect.source = FONDO_SELECCION

    def elegirFaccion(self, nombreFaccion, rutaSprite, colorAcento):
        pantallaHome = self.manager.get_screen('principal')
        pantallaHome.cargarPersonaje(nombreFaccion, rutaSprite, colorAcento)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'principal'