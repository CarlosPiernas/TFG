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
    NOMBRE_ANOMALIA, NOMBRE_GUARDIAN
)
from widgets.componentes import BotonRedondeado
 
 
class PantallaSeleccion(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
 
        # Fondo de pantalla
        with self.canvas.before:
            Color(*FONDO_PRINCIPAL)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.actualizarFondo, size=self.actualizarFondo)
 
        contenedorPrincipal = BoxLayout(
            orientation='vertical',
            padding=dp(40),
            spacing=dp(20)
        )
 
        # Título
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
 
        # Logos de cada facción
        filaLogos = GridLayout(
            cols=2,
            spacing=dp(20),
            size_hint=(1, 1),
            height=dp(260)
        )
 
        imgLogoAnomalias = Image(
            source=LOGO_ANOMALIA,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1)
        )
 
        imgLogoGuardianes = Image(
            source=LOGO_GUARDIAN,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1)
        )
 
        filaLogos.add_widget(imgLogoAnomalias)
        filaLogos.add_widget(imgLogoGuardianes)
 
        espaciador = Widget(size_hint=(1, 1))
 
        # Botones de elección de facción
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
 
        contenedorPrincipal.add_widget(titulo)
        contenedorPrincipal.add_widget(filaLogos)
        contenedorPrincipal.add_widget(espaciador)
        contenedorPrincipal.add_widget(botonElegirAnomalias)
        contenedorPrincipal.add_widget(botonElegirGuardianes)
        contenedorPrincipal.add_widget(Widget(size_hint=(1, None), height=dp(20)))
 
        self.add_widget(contenedorPrincipal)
 
    def actualizarFondo(self, *args):
        self._bg_rect.pos  = self.pos
        self._bg_rect.size = self.size
 
    def elegirFaccion(self, nombreFaccion, rutaSprite, colorAcento):
        # Pasa los datos a la PantallaPrincipal 
        pantallaHome = self.manager.get_screen('principal')
        pantallaHome.cargarPersonaje(nombreFaccion, rutaSprite, colorAcento)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'principal'