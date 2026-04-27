from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp
from config import (
    FONDO_SELECCION, PANEL_OSCURO, PANEL_MEDIO,
    COLOR_ANOMALIAS, COLOR_GUARDIANES, BLANCO
)
from widgets.componentes import BotonRedondeado


class PantallaInventario(Screen):
    def __init__(self, gm=None, **kwargs):
        super().__init__(**kwargs)
        self.gm              = gm
        self.categoriaActual = 'personajes'
        self.itemSeleccionado = None  # dict del item actualmente seleccionado

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self._bg_rect = Rectangle(source=FONDO_SELECCION, pos=self.pos, size=self.size)
        self.bind(pos=self.actualizarFondo, size=self.actualizarFondo)

        overlayWidget = Widget(size_hint=(1, 1))
        with overlayWidget.canvas:
            Color(0, 0, 0, 0.55)
            self._overlay = Rectangle(pos=overlayWidget.pos, size=overlayWidget.size)
        overlayWidget.bind(
            pos=lambda *a: setattr(self._overlay, 'pos', overlayWidget.pos),
            size=lambda *a: setattr(self._overlay, 'size', overlayWidget.size)
        )

        contenedorPrincipal = BoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(8)
        )

        # Título
        cajaTitle = BoxLayout(size_hint=(1, None), height=dp(44), padding=[dp(8), dp(4)])
        with cajaTitle.canvas.before:
            Color(0, 0, 0, 0.6)
            self._titleRect = RoundedRectangle(pos=cajaTitle.pos, size=cajaTitle.size, radius=[dp(8)])
            Color(0.6, 0.45, 0.1, 0.5)
            self._titleBorde = Line(
                rounded_rectangle=(cajaTitle.x, cajaTitle.y, cajaTitle.width, cajaTitle.height, dp(8)),
                width=1.2
            )
        cajaTitle.bind(
            pos=lambda *a: self._actualizarCaja(cajaTitle, self._titleRect, self._titleBorde),
            size=lambda *a: self._actualizarCaja(cajaTitle, self._titleRect, self._titleBorde)
        )
        etiquetaInventario = Label(
            text='— INVENTARIO —',
            font_size=dp(18),
            bold=True,
            color=(0.9, 0.75, 0.3, 1),
            size_hint=(1, 1),
            halign='center',
            valign='middle'
        )
        etiquetaInventario.bind(size=etiquetaInventario.setter('text_size'))
        cajaTitle.add_widget(etiquetaInventario)
        contenedorPrincipal.add_widget(cajaTitle)

        # Botones de categoría
        contenedorCategoria = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(38),
            spacing=dp(8)
        )
        for texto, categoria in [('PERSONAJES', 'personajes'), ('ARMAS', 'armas'), ('RUNAS', 'runas')]:
            btn = BotonRedondeado(
                text=texto,
                bg_color=(0.05, 0.05, 0.1, 0.9),
                text_color=(0.9, 0.75, 0.3, 1),
                radius=6,
                size_hint=(1, 1),
                font_size=dp(11),
                bold=True
            )
            btn.bind(on_press=lambda _, c=categoria: self.cambiarCategoria(c))
            contenedorCategoria.add_widget(btn)
        contenedorPrincipal.add_widget(contenedorCategoria)

        # Scroll horizontal de artículos
        contenedorScroll = ScrollView(
            size_hint=(1, None),
            height=dp(110),
            do_scroll_x=True,
            do_scroll_y=False
        )
        with contenedorScroll.canvas.before:
            Color(0, 0, 0, 0.5)
            self._scrollRect = RoundedRectangle(pos=contenedorScroll.pos, size=contenedorScroll.size, radius=[dp(8)])
            Color(0.6, 0.45, 0.1, 0.4)
            self._scrollBorde = Line(
                rounded_rectangle=(
                    contenedorScroll.x, contenedorScroll.y,
                    contenedorScroll.width, contenedorScroll.height, dp(8)
                ),
                width=1.0
            )
        contenedorScroll.bind(
            pos=lambda *a: self._actualizarCaja(contenedorScroll, self._scrollRect, self._scrollBorde),
            size=lambda *a: self._actualizarCaja(contenedorScroll, self._scrollRect, self._scrollBorde)
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

        # Panel central imagen + stats
        contenedorCentral = BoxLayout(orientation='vertical', size_hint=(1, 1), spacing=dp(8))
        contenedorImagenStats = BoxLayout(orientation='horizontal', size_hint=(1, 0.7), spacing=dp(8))

        cajaImagen = BoxLayout(size_hint=(0.5, 1), padding=dp(4))
        with cajaImagen.canvas.before:
            Color(0, 0, 0, 0.5)
            self._imgRect = RoundedRectangle(pos=cajaImagen.pos, size=cajaImagen.size, radius=[dp(10)])
            Color(0.6, 0.45, 0.1, 0.4)
            self._imgBorde = Line(
                rounded_rectangle=(cajaImagen.x, cajaImagen.y, cajaImagen.width, cajaImagen.height, dp(10)),
                width=1.0
            )
        cajaImagen.bind(
            pos=lambda *a: self._actualizarCaja(cajaImagen, self._imgRect, self._imgBorde),
            size=lambda *a: self._actualizarCaja(cajaImagen, self._imgRect, self._imgBorde)
        )
        self.imagenArticulo = Image(source='', allow_stretch=True, keep_ratio=True, size_hint=(1, 1))
        cajaImagen.add_widget(self.imagenArticulo)

        cajaStats = BoxLayout(size_hint=(0.5, 1), padding=dp(8))
        with cajaStats.canvas.before:
            Color(0, 0, 0, 0.5)
            self._statsRect = RoundedRectangle(pos=cajaStats.pos, size=cajaStats.size, radius=[dp(10)])
            Color(0.6, 0.45, 0.1, 0.4)
            self._statsBorde = Line(
                rounded_rectangle=(cajaStats.x, cajaStats.y, cajaStats.width, cajaStats.height, dp(10)),
                width=1.0
            )
        cajaStats.bind(
            pos=lambda *a: self._actualizarCaja(cajaStats, self._statsRect, self._statsBorde),
            size=lambda *a: self._actualizarCaja(cajaStats, self._statsRect, self._statsBorde)
        )
        self.etiquetaStats = Label(
            text='Selecciona\nun artículo',
            font_size=dp(11),
            color=(0.85, 0.85, 0.85, 1),
            size_hint=(1, 1),
            halign='left',
            valign='top'
        )
        self.etiquetaStats.bind(size=self.etiquetaStats.setter('text_size'))
        cajaStats.add_widget(self.etiquetaStats)

        contenedorImagenStats.add_widget(cajaImagen)
        contenedorImagenStats.add_widget(cajaStats)
        contenedorCentral.add_widget(contenedorImagenStats)

        # Lore
        cajaLore = BoxLayout(size_hint=(1, 0.3), padding=dp(8))
        with cajaLore.canvas.before:
            Color(0, 0, 0, 0.5)
            self._loreRect = RoundedRectangle(pos=cajaLore.pos, size=cajaLore.size, radius=[dp(10)])
            Color(0.6, 0.45, 0.1, 0.3)
            self._loreBorde = Line(
                rounded_rectangle=(cajaLore.x, cajaLore.y, cajaLore.width, cajaLore.height, dp(10)),
                width=1.0
            )
        cajaLore.bind(
            pos=lambda *a: self._actualizarCaja(cajaLore, self._loreRect, self._loreBorde),
            size=lambda *a: self._actualizarCaja(cajaLore, self._loreRect, self._loreBorde)
        )
        self.etiquetaLore = Label(
            text='',
            font_size=dp(10),
            color=(0.7, 0.65, 0.5, 1),
            size_hint=(1, 1),
            halign='left',
            valign='top'
        )
        self.etiquetaLore.bind(size=self.etiquetaLore.setter('text_size'))
        cajaLore.add_widget(self.etiquetaLore)
        contenedorCentral.add_widget(cajaLore)
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
            Color(0, 0, 0, 0.85)
            self._rectBarraInferior = RoundedRectangle(
                pos=barraInferior.pos, size=barraInferior.size,
                radius=[dp(20), dp(20), 0, 0]
            )
        barraInferior.bind(
            pos=lambda *a: setattr(self._rectBarraInferior, 'pos', barraInferior.pos),
            size=lambda *a: setattr(self._rectBarraInferior, 'size', barraInferior.size)
        )

        botonAtras = BotonRedondeado(
            text='MENÚ', bg_color=(0.05, 0.05, 0.1, 0.9),
            text_color=(0.9, 0.75, 0.3, 1), radius=8,
            size_hint=(1, 1), font_size=dp(11), bold=True
        )
        botonAtras.bind(on_press=self.volverAHome)

        botonForja = BotonRedondeado(
            text='FORJA', bg_color=(0.05, 0.05, 0.1, 0.9),
            text_color=COLOR_ANOMALIAS, radius=8,
            size_hint=(1, 1), font_size=dp(11), bold=True
        )
        botonForja.bind(on_press=lambda _: self.navegarA('forja'))

        self.botonOk = BotonRedondeado(
            text='EQUIPAR', bg_color=(0.05, 0.05, 0.1, 0.9),
            text_color=COLOR_GUARDIANES, radius=8,
            size_hint=(1, 1), font_size=dp(11), bold=True
        )
        self.botonOk.bind(on_press=self.confirmarSeleccion)

        barraInferior.add_widget(botonAtras)
        barraInferior.add_widget(botonForja)
        barraInferior.add_widget(self.botonOk)
        contenedorPrincipal.add_widget(barraInferior)

        self.add_widget(overlayWidget)
        self.add_widget(contenedorPrincipal)

    # ── Kivy hooks ──────────────────────────────────────────

    def on_pre_enter(self, *args):
        self.cambiarCategoria(self.categoriaActual)

    # ── Lógica de categorías ─────────────────────────────────

    def cambiarCategoria(self, categoria):
        self.categoriaActual  = categoria
        self.itemSeleccionado = None
        self.filaArticulos.clear_widgets()
        self.etiquetaStats.text = 'Selecciona\nun artículo'
        self.etiquetaLore.text  = ''
        self.imagenArticulo.source = ''

        if self.gm is None:
            return

        if categoria == 'personajes':
            items = self.gm.get_personajes_jugador()
            self.botonOk.text = 'SELECCIONAR'  # cambia personaje activo
        elif categoria == 'armas':
            items = self.gm.get_armas_jugador()
            self.botonOk.text = 'EQUIPAR'
        else:
            items = self.gm.get_runas_jugador()
            self.botonOk.text = 'EQUIPAR'

        for item in items:
            self._crearTarjeta(item, categoria)

    def _crearTarjeta(self, item, categoria):
        # Tarjeta pequeña en el scroll horizontal
        tarjeta = BotonRedondeado(
            text=item.get('nombre', '?'),
            bg_color=(0.08, 0.08, 0.15, 0.95),
            text_color=(0.9, 0.75, 0.3, 1),
            radius=8,
            size_hint=(None, 1),
            width=dp(80),
            font_size=dp(9),
            bold=True
        )
        tarjeta.bind(on_press=lambda _, i=item: self.seleccionarItem(i))
        self.filaArticulos.add_widget(tarjeta)

    def seleccionarItem(self, item):
        self.itemSeleccionado = item

        # Stats según categoría
        if self.categoriaActual == 'personajes':
            texto = (
                f"{item.get('nombre', '?')}\n"
                f"Clase: {item.get('clase', '?')}\n"
                f"Rareza: {item.get('rareza', '?')}\n\n"
                f"HP:  {item.get('pv_base', '—')}\n"
                f"ATK: {item.get('atk_base', '—')}\n"
                f"DEF: {item.get('defensa_base', '—')}"
            )
        elif self.categoriaActual == 'armas':
            texto = (
                f"{item.get('nombre', '?')}\n"
                f"Rareza: {item.get('rareza', '?')}\n\n"
                f"+ATK:  {item.get('bonus_atk', 0)}\n"
                f"+DEF:  {item.get('bonus_def', 0)}\n"
                f"+MAGIA:{item.get('bonus_magia', 0)}"
            )
        else:
            texto = (
                f"{item.get('nombre', '?')}\n\n"
                f"+ATK:     {item.get('bonus_atk', 0)}\n"
                f"+DEF:     {item.get('bonus_def', 0)}\n"
                f"+MAGIA:   {item.get('bonus_magia', 0)}\n"
                f"+DESTREZA:{item.get('bonus_destreza', 0)}"
            )

        self.etiquetaStats.text = texto
        self.etiquetaLore.text  = item.get('lore', '')

        # Sprite si existe
        sprite = item.get('sprite', '')
        self.imagenArticulo.source = sprite or ''
        if sprite:
            self.imagenArticulo.reload()

    # ── Acciones ─────────────────────────────────────────────

    def confirmarSeleccion(self, instance):
        if self.gm is None or self.itemSeleccionado is None:
            return

        inv_id = self.itemSeleccionado.get('inv_id')
        if inv_id is None:
            return

        if self.categoriaActual == 'personajes':
            self.gm.cambiar_personaje_activo(inv_id)

        elif self.categoriaActual == 'armas':
            resultado = self.gm.equipar_arma(inv_id)
            print(f"[Inventario] {resultado.get('mensaje', '')}")

        elif self.categoriaActual == 'runas':
            # Slot 1 si no hay ninguna equipada, slot 2 si ya hay una
            equipo = self.gm.get_personaje_activo_info() or {}
            runas_equipadas = [
                e for e in equipo.get('equipo', [])
                if 'runa' in e.get('slot', '')
            ]
            slot = 2 if len(runas_equipadas) >= 1 else 1
            resultado = self.gm.equipar_runa(inv_id, slot)
            print(f"[Inventario] {resultado.get('mensaje', '')}")

        # Refrescar la vista
        self.cambiarCategoria(self.categoriaActual)

    # ── Helpers ───────────────────────────────────────────────

    def _actualizarCaja(self, widget, rect, borde):
        rect.pos  = widget.pos
        rect.size = widget.size
        borde.rounded_rectangle = (
            widget.x, widget.y, widget.width, widget.height, dp(10)
        )

    def actualizarFondo(self, *args):
        self._bg_rect.pos  = self.pos
        self._bg_rect.size = self.size

    def navegarA(self, pantalla):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = pantalla

    def volverAHome(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'principal'