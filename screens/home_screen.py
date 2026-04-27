from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp
from config import (
    FONDO_PRINCIPAL, PANEL_OSCURO, PANEL_MEDIO,
    COLOR_ANOMALIAS, COLOR_GUARDIANES, BLANCO, COLOR_CAMPAÑA, COLOR_VIDA,
    FONDO_ANOMALIAS, FONDO_GUARDIANES, NOMBRE_ANOMALIA
)
from widgets.componentes import BotonRedondeado


class PantallaPrincipal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self._bg_rect = Rectangle(source='', pos=self.pos, size=self.size)
        self.bind(pos=self.actualizarFondo, size=self.actualizarFondo)

        contenedorPrincipal = BoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(8)
        )

        # Barra superior con fondo oscuro semitransparente
        barraEncabezado = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(44),
            spacing=dp(10),
            padding=[dp(8), dp(4)]
        )
        with barraEncabezado.canvas.before:
            Color(0, 0, 0, 0.6)
            self._headerRect = RoundedRectangle(
                pos=barraEncabezado.pos,
                size=barraEncabezado.size,
                radius=[dp(8)]
            )
        barraEncabezado.bind(
            pos=lambda *a: setattr(self._headerRect, 'pos', barraEncabezado.pos),
            size=lambda *a: setattr(self._headerRect, 'size', barraEncabezado.size)
        )

        self.etiquetaFaccion = Label(
            text='',
            font_size=dp(13),
            bold=True,
            color=BLANCO,
            size_hint=(None, None),
            size=(dp(110), dp(36)),
            halign='left',
            valign='middle'
        )
        self.etiquetaFaccion.bind(size=self.etiquetaFaccion.setter('text_size'))

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

        etiquetaMonedas = BotonRedondeado(
            text='9999',
            bg_color=(0.05, 0.05, 0.1, 0.85),
            text_color=COLOR_GUARDIANES,
            radius=8,
            size_hint=(None, None),
            size=(dp(90), dp(34)),
            font_size=dp(13),
            bold=True
        )

        barraEncabezado.add_widget(self.etiquetaFaccion)
        barraEncabezado.add_widget(barraVida)
        barraEncabezado.add_widget(Widget(size_hint=(1, 1)))
        barraEncabezado.add_widget(etiquetaMonedas)

        # Caja del personaje con borde y fondo semitransparente
        cajaPersonaje = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.45),
            padding=dp(2)
        )
        with cajaPersonaje.canvas.before:
            Color(0, 0, 0, 0.45)
            self._cajaRect = RoundedRectangle(
                pos=cajaPersonaje.pos,
                size=cajaPersonaje.size,
                radius=[dp(3)]
            )
            Color(1, 1, 1, 0.15)
            self._cajaBorde = Line(
                rounded_rectangle=(
                    cajaPersonaje.x, cajaPersonaje.y,
                    cajaPersonaje.width, cajaPersonaje.height,
                    dp(3)
                ),
                width=1.2
            )
        cajaPersonaje.bind(
            pos=self._actualizarCajaPersonaje,
            size=self._actualizarCajaPersonaje
        )

        self.imagenPersonaje = Image(
            source='',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5}
        )
        cajaPersonaje.add_widget(self.imagenPersonaje)

        # Bloques de stats con mayor opacidad
        contenedorBloques = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.35),
            spacing=dp(8)
        )

        bloqueStats = BotonRedondeado(
            text='STATS GENERALES\n\nHP: 1250\nATK: 85\nDEF: 40\nSPD: 15',
            bg_color=(0.05, 0.08, 0.12, 0.95),
            text_color=COLOR_GUARDIANES,
            radius=10,
            size_hint=(0.4, 1),
            font_size=dp(11),
            halign='left',
            valign='top',
            padding=(dp(15), dp(15))
        )
        bloqueStats.bind(size=lambda instance, value: setattr(instance, 'text_size', value))

        bloqueRunas = BoxLayout(orientation='vertical', size_hint=(0.6, 1), spacing=dp(5))

        filaSlots = BoxLayout(orientation='horizontal', size_hint=(1, 0.35), spacing=dp(5))
        for i in range(1, 4):
            slotRuna = BotonRedondeado(
                text=f'R{i}',
                bg_color=(0.1, 0.12, 0.18, 0.95),
                radius=8,
                font_size=dp(10)
            )
            filaSlots.add_widget(slotRuna)

        statsRunas = BotonRedondeado(
            text='STATS RUNAS\n\nATK - 32\nDEF - 5\nSPD - 40',
            bg_color=(0.05, 0.08, 0.12, 0.95),
            text_color=COLOR_ANOMALIAS,
            radius=10,
            size_hint=(1, 0.65),
            font_size=dp(11)
        )

        bloqueRunas.add_widget(filaSlots)
        bloqueRunas.add_widget(statsRunas)
        contenedorBloques.add_widget(bloqueStats)
        contenedorBloques.add_widget(bloqueRunas)

        # Barra de navegación
        barraNavegacion = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(70),
            spacing=dp(10),
            padding=[dp(10), dp(10)]
        )
        with barraNavegacion.canvas.before:
            Color(0, 0, 0, 0.85)
            self._navRect = RoundedRectangle(
                pos=barraNavegacion.pos,
                size=barraNavegacion.size,
                radius=[dp(20), dp(20), 0, 0]
            )
        barraNavegacion.bind(
            pos=lambda *a: setattr(self._navRect, 'pos', barraNavegacion.pos),
            size=lambda *a: setattr(self._navRect, 'size', barraNavegacion.size)
        )

        botonGacha = BotonRedondeado(
            text='Gacha',
            bg_color=PANEL_MEDIO,
            text_color=BLANCO,
            radius=8,
            size_hint=(None, 1),
            width=dp(55),
            font_size=dp(13)
        )
        botonGacha.bind(on_press=lambda _: self.navegarA('gacha'))

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

        botonVolverSeleccion = BotonRedondeado(
            text='INV',
            bg_color=PANEL_MEDIO,
            text_color=BLANCO,
            radius=8,
            size_hint=(None, 1),
            width=dp(55),
            font_size=dp(13)
        )
        botonVolverSeleccion.bind(on_press=lambda _: self.navegarA('inventario'))

        barraNavegacion.add_widget(botonGacha)
        barraNavegacion.add_widget(botonCampana)
        barraNavegacion.add_widget(botonVolverSeleccion)

        contenedorPrincipal.add_widget(barraEncabezado)
        contenedorPrincipal.add_widget(cajaPersonaje)
        contenedorPrincipal.add_widget(contenedorBloques)
        contenedorPrincipal.add_widget(barraNavegacion)

        self.add_widget(contenedorPrincipal)

    def _actualizarCajaPersonaje(self, instance, value):
        self._cajaRect.pos  = instance.pos
        self._cajaRect.size = instance.size
        self._cajaBorde.rounded_rectangle = (
            instance.x, instance.y,
            instance.width, instance.height,
            dp(3)
        )

    def cargarPersonaje(self, nombreFaccion, rutaSprite, colorAcento):
        self.imagenPersonaje.source = rutaSprite
        self.imagenPersonaje.reload()
        self.etiquetaFaccion.text  = nombreFaccion
        self.etiquetaFaccion.color = colorAcento
        if nombreFaccion == NOMBRE_ANOMALIA:
            self._bg_rect.source = FONDO_ANOMALIAS
        else:
            self._bg_rect.source = FONDO_GUARDIANES

    def navegarA(self, pantalla):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = pantalla

    def actualizarFondo(self, *args):
        self._bg_rect.pos  = self.pos
        self._bg_rect.size = self.size

    def volverASeleccion(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'seleccion'