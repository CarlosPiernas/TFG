from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp

from config import (
    FONDO_PRINCIPAL, PANEL_OSCURO, PANEL_MEDIO,
    COLOR_ANOMALIAS, COLOR_GUARDIANES, BLANCO
)
from widgets.componentes import BotonRedondeado


class PantallaInventario(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fondo de pantalla
        with self.canvas.before:
            Color(*FONDO_PRINCIPAL)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.actualizarFondo, size=self.actualizarFondo)

        # Contenedor que organiza todo en columna de arriba a abajo
        contenedorPrincipal = BoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(8)
        )

        # Título 
        etiquetaInventario = Label(
            text='INVENTARIO',
            font_size=dp(20),
            bold=True,
            color=BLANCO,
            size_hint=(1, None),
            height=dp(40),
            halign='center',
            valign='middle'
        )
        etiquetaInventario.bind(size=etiquetaInventario.setter('text_size'))

        contenedorPrincipal.add_widget(etiquetaInventario)

        # Botones de categoría 
        contenedorCategoria = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(40),
            spacing=dp(8)
        )

        botonPersonajes = BotonRedondeado(
            text='PERSONAJES',
            bg_color=PANEL_MEDIO,
            text_color=BLANCO,
            radius=8,
            size_hint=(1, 1),
            font_size=dp(11)
        )
        botonPersonajes.bind(on_press=lambda _: self.cambiarCategoria('personajes'))

        botonArmas = BotonRedondeado(
            text='ARMAS',
            bg_color=PANEL_MEDIO,
            text_color=BLANCO,
            radius=8,
            size_hint=(1, 1),
            font_size=dp(11)
        )
        botonArmas.bind(on_press=lambda _: self.cambiarCategoria('armas'))

        botonRunas = BotonRedondeado(
            text='RUNAS',
            bg_color=PANEL_MEDIO,
            text_color=BLANCO,
            radius=8,
            size_hint=(1, 1),
            font_size=dp(11)
        )
        botonRunas.bind(on_press=lambda _: self.cambiarCategoria('runas'))

        contenedorCategoria.add_widget(botonPersonajes)
        contenedorCategoria.add_widget(botonArmas)
        contenedorCategoria.add_widget(botonRunas)

        contenedorPrincipal.add_widget(contenedorCategoria)

        # Scroll horizontal 
        contenedorScroll = ScrollView(
            size_hint=(1, None),
            height=dp(100),
            do_scroll_x=True,
            do_scroll_y=False
        )

        self.filaArticulos = BoxLayout(
            orientation='horizontal',
            size_hint=(None, 1),
            spacing=dp(8),
            padding=dp(4)
        )
        self.filaArticulos.bind(minimum_width=self.filaArticulos.setter('width'))

        contenedorScroll.add_widget(self.filaArticulos)
        contenedorPrincipal.add_widget(contenedorScroll)

        # Panel central con imagen y stats 
        contenedorCentral = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            spacing=dp(8)
        )

        contenedorImagenStats = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.7),
            spacing=dp(8)
        )

        self.imagenArticulo = Image(
            source='',
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(0.5, 1)
        )

        self.etiquetaStats = Label(
            text='Selecciona un articulo',
            font_size=dp(11),
            color=BLANCO,
            size_hint=(0.5, 1),
            halign='left',
            valign='top'
        )
        self.etiquetaStats.bind(size=self.etiquetaStats.setter('text_size'))

        contenedorImagenStats.add_widget(self.imagenArticulo)
        contenedorImagenStats.add_widget(self.etiquetaStats)
        contenedorCentral.add_widget(contenedorImagenStats)

        # Hueco del lore 
        self.etiquetaLore = Label(
            text='',
            font_size=dp(10),
            color=BLANCO,
            size_hint=(1, 0.3),
            halign='left',
            valign='top'
        )
        self.etiquetaLore.bind(size=self.etiquetaLore.setter('text_size'))

        contenedorCentral.add_widget(self.etiquetaLore)
        contenedorPrincipal.add_widget(contenedorCentral)

        # Barra inferior 
        barraInferior = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(60),
            spacing=dp(8),
            padding=[dp(10), dp(8)]
        )
        with barraInferior.canvas.before:
            Color(*PANEL_OSCURO)
            self._rectBarraInferior = RoundedRectangle(
                pos=barraInferior.pos,
                size=barraInferior.size,
                radius=[dp(20), dp(20), 0, 0]
            )
        barraInferior.bind(
            pos=lambda *a: setattr(self._rectBarraInferior, 'pos', barraInferior.pos),
            size=lambda *a: setattr(self._rectBarraInferior, 'size', barraInferior.size)
        )

        botonAtras = BotonRedondeado(
            text='ATRAS',
            bg_color=PANEL_MEDIO,
            text_color=BLANCO,
            radius=8,
            size_hint=(1, 1),
            font_size=dp(11)
        )
        botonAtras.bind(on_press=self.volverAHome)

        botonForja = BotonRedondeado(
            text='FORJA',
            bg_color=PANEL_MEDIO,
            text_color=COLOR_ANOMALIAS,
            radius=8,
            size_hint=(1, 1),
            font_size=dp(11)
        )
        botonForja.bind(on_press=lambda _: self.navegarA('forja'))

        botonOk = BotonRedondeado(
            text='OK',
            bg_color=PANEL_MEDIO,
            text_color=COLOR_GUARDIANES,
            radius=8,
            size_hint=(1, 1),
            font_size=dp(11)
        )
        botonOk.bind(on_press=self.confirmarSeleccion)

        barraInferior.add_widget(botonAtras)
        barraInferior.add_widget(botonForja)
        barraInferior.add_widget(botonOk)
        contenedorPrincipal.add_widget(barraInferior)

        self.add_widget(contenedorPrincipal)

    # Métodos
    def actualizarFondo(self, *args):
        # Redibuja si cambia de tamaño
        self._bg_rect.pos  = self.pos
        self._bg_rect.size = self.size

    def cambiarCategoria(self, categoria):
        # Limpia el scroll y carga los artículos de la categoría seleccionada
        self.filaArticulos.clear_widgets()
        print(f'Categoria seleccionada: {categoria}')

    def confirmarSeleccion(self, instance):
        # Confirma el artículo seleccionado como equipado
        print('Articulo confirmado')

    def navegarA(self, pantalla):
        # Cambia a la pantalla indicada
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = pantalla

    def volverAHome(self, instance):
        # Vuelve a la pantalla principal
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'principal'