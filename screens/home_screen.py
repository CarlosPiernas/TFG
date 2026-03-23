from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp
 
from config import (
    FONDO_PRINCIPAL, PANEL_OSCURO, PANEL_MEDIO,
    COLOR_ANOMALIAS, COLOR_GUARDIANES, BLANCO, COLOR_CAMPAÑA, COLOR_VIDA
)
from widgets.componentes import BotonRedondeado
 
 
class PantallaPrincipal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
 
        # Fondo de pantalla
        with self.canvas.before:
            Color(*FONDO_PRINCIPAL)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.actualizarFondo, size=self.actualizarFondo)
 
        contenedorPrincipal = BoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(8)
        )
 
        # Nombre de facción/ barra de vida/ monedas
        barraEncabezado = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(40),
            spacing=dp(10)
        )
 
        # Nombre de la facción elegida — se rellena en cargarPersonaje()
        self.etiquetaFaccion = Label(
            text='',
            font_size=dp(12),
            bold=True,
            color=BLANCO,
            size_hint=(None, None),
            size=(dp(100), dp(35)),
            halign='left',
            valign='middle'
        )
        self.etiquetaFaccion.bind(size=self.etiquetaFaccion.setter('text_size'))
 
        # Barra de vida 
        barraVida = BoxLayout(
            size_hint=(None, None),
            size=(dp(120), dp(28)),
            padding=dp(3)
        )
 
        def actualizarBarraVida(*args):
            x, y = barraVida.pos
            w, h = barraVida.size
            barraVida.canvas.before.clear()
            with barraVida.canvas.before:
                Color(1, 1, 1, 1)
                Line(rounded_rectangle=(x, y, w, h, dp(5)), width=1.2)
                Color(*COLOR_VIDA)
                RoundedRectangle(
                    pos=(x + dp(3), y + dp(3)),
                    size=(w - dp(6), h - dp(6)),
                    radius=[dp(4)]
                )
 
        barraVida.bind(pos=actualizarBarraVida, size=actualizarBarraVida)
 
        # Monedas 
        etiquetaMonedas = BotonRedondeado(
            text='9999',
            bg_color=PANEL_OSCURO,
            text_color=COLOR_GUARDIANES,
            radius=10,
            size_hint=(None, None),
            size=(dp(100), dp(35)),
            font_size=dp(13),
            bold=True
        )
 
        barraEncabezado.add_widget(self.etiquetaFaccion)
        barraEncabezado.add_widget(barraVida)
        barraEncabezado.add_widget(Widget(size_hint=(1, 1)))
        barraEncabezado.add_widget(etiquetaMonedas)
 
        # Sprite del personaje 
        zonaCentral = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.5),
            spacing=dp(10)
        )
 
        # Sprite del personaje activo 
        self.imagenPersonaje = Image(
            source='',
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5}
        )
 
        zonaCentral.add_widget(self.imagenPersonaje)
 
        # Bloques de stats y runas 
        contenedorBloques = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.4),
            spacing=dp(10)
        )
 
        # Stats generales del personaje
        bloqueStats = BotonRedondeado(
            text='STATS GENERALES\n\nHP: 1250\nATK: 85\nDEF: 40\nSPD: 15',
            bg_color=PANEL_OSCURO,
            text_color=COLOR_GUARDIANES,
            radius=10,
            size_hint=(0.4, 1),
            font_size=dp(11)
        )
 
        # Slots de runas equipadas/ stats combinadas
        bloqueRunas = BoxLayout(orientation='vertical', size_hint=(0.6, 1), spacing=dp(5))
 
        filaSlots = BoxLayout(orientation='horizontal', size_hint=(1, 0.35), spacing=dp(5))
        for i in range(1, 4):
            slotRuna = BotonRedondeado(
                text=f'R{i}',
                bg_color=PANEL_MEDIO,
                radius=8,
                font_size=dp(10)
            )
            filaSlots.add_widget(slotRuna)
 
        # Stats combinadas de las runas equipadas 
        statsRunas = BotonRedondeado(
            text='STATS RUNAS\n\nATK - 32\nDEF - 5\nSPD - 40',
            bg_color=PANEL_OSCURO,
            text_color=COLOR_ANOMALIAS,
            radius=10,
            size_hint=(1, 0.65),
            font_size=dp(11)
        )
 
        bloqueRunas.add_widget(filaSlots)
        bloqueRunas.add_widget(statsRunas)
        contenedorBloques.add_widget(bloqueStats)
        contenedorBloques.add_widget(bloqueRunas)
 
        # Barra de navegación inferior 
        barraNavegacion = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(70),
            spacing=dp(10),
            padding=[dp(10), dp(10)]
        )
        with barraNavegacion.canvas.before:
            Color(*PANEL_OSCURO)
            self._navRect = RoundedRectangle(
                pos=barraNavegacion.pos,
                size=barraNavegacion.size,
                radius=[dp(20), dp(20), 0, 0]
            )
        barraNavegacion.bind(
            pos=lambda *a: setattr(self._navRect, 'pos', barraNavegacion.pos),
            size=lambda *a: setattr(self._navRect, 'size', barraNavegacion.size)
        )
 
        # Botón Gacha 
        botonGacha = BotonRedondeado(
            text='Gacha',
            bg_color=PANEL_MEDIO,
            text_color=BLANCO,
            radius=8,
            size_hint=(None, 1),
            width=dp(55),
            font_size=dp(20)
        )
        botonGacha.bind(on_press=lambda _: self.navegarA('gacha'))
 
        # Botón Campaña 
        botonCampana = BotonRedondeado(
            text='CAMPAÑA',
            bg_color=COLOR_CAMPAÑA,
            text_color=BLANCO,
            radius=8,
            size_hint=(1, 1),
            font_size=dp(13),
            bold=True
        )
        botonCampana.bind(on_press=lambda _: self.navegarA('mapa'))
 
        # Botón Volver 
        botonVolverSeleccion = BotonRedondeado(
            text='INV',
            bg_color=PANEL_MEDIO,
            text_color=BLANCO,
            radius=8,
            size_hint=(None, 1),
            width=dp(55),
            font_size=dp(20)
        )
        botonVolverSeleccion.bind(on_press=lambda _: self.navegarA('inventario'))
 
        barraNavegacion.add_widget(botonGacha)
        barraNavegacion.add_widget(botonCampana)
        barraNavegacion.add_widget(botonVolverSeleccion)
 
        contenedorPrincipal.add_widget(barraEncabezado)
        contenedorPrincipal.add_widget(zonaCentral)
        contenedorPrincipal.add_widget(contenedorBloques)
        contenedorPrincipal.add_widget(barraNavegacion)
 
        self.add_widget(contenedorPrincipal)
 
    def cargarPersonaje(self, nombreFaccion, rutaSprite, colorAcento):
        # Actualiza el sprite y el nombre de facción al llegar desde la selección
        self.imagenPersonaje.source = rutaSprite
        self.imagenPersonaje.reload()
        self.etiquetaFaccion.text  = nombreFaccion
        self.etiquetaFaccion.color = colorAcento
 
    def navegarA(self, pantalla):
        # Navega hacia la pantalla indicada con animación hacia la izquierda
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = pantalla
 
    def actualizarFondo(self, *args):
        self._bg_rect.pos  = self.pos
        self._bg_rect.size = self.size
 
    def volverASeleccion(self, instance):
        # Vuelve a la selección de facción con animación hacia la derecha
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'seleccion'