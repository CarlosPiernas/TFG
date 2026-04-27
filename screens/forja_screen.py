from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.modalview import ModalView
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp
from config import (
    FONDO_SELECCION, PANEL_OSCURO, PANEL_MEDIO,
    COLOR_ANOMALIAS, COLOR_GUARDIANES, BLANCO, GRIS
)
from widgets.componentes import BotonRedondeado


class SlotForja(Widget):
    def __init__(self, tipo='ingrediente', etiqueta='', **kwargs):
        super().__init__(**kwargs)
        self.tipo     = tipo
        self.etiqueta = etiqueta
        self.runa     = None  # dict de la runa asignada o None
        self.bind(pos=self._redibujar, size=self._redibujar)

    def asignar(self, runa: dict):
        # Asigna una runa al slot y actualiza la etiqueta visual
        self.runa     = runa
        self.etiqueta = runa.get('nombre', '?') if runa else ''
        self._redibujar()

    def limpiar(self):
        self.runa     = None
        self.etiqueta = self._etiqueta_default
        self._redibujar()

    def _redibujar(self, *args):
        self.canvas.clear()
        with self.canvas:
            if self.tipo == 'resultado':
                Color(0.1, 0.05, 0.15, 0.85)
            else:
                Color(0, 0, 0, 0.6)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])

            if self.runa and self.tipo == 'ingrediente':
                # Borde verde si tiene runa asignada
                Color(0.2, 0.8, 0.3, 0.9)
            elif self.tipo == 'resultado':
                Color(*COLOR_ANOMALIAS[:3], 0.8)
            else:
                Color(0.6, 0.45, 0.1, 0.6)
            Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, dp(10)),
                width=1.5
            )

        for child in list(self.children):
            self.remove_widget(child)

        # Texto del slot
        if self.runa:
            texto      = self.runa.get('nombre', '?')
            color_text = (0.3, 1.0, 0.4, 1)
        else:
            texto      = self.etiqueta
            color_text = (0.9, 0.75, 0.3, 0.7)

        lbl = Label(
            text=texto,
            font_size=dp(11),
            bold=True,
            color=color_text,
            pos=self.pos,
            size=self.size,
            halign='center',
            valign='middle'
        )
        lbl.bind(size=lbl.setter('text_size'))
        self.add_widget(lbl)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return True
        return super().on_touch_down(touch)


class PantallaForja(Screen):
    def __init__(self, gm=None, **kwargs):
        super().__init__(**kwargs)
        self.gm = gm

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self._bg_rect = Rectangle(source=FONDO_SELECCION, pos=self.pos, size=self.size)
        self.bind(pos=self._actualizarFondo, size=self._actualizarFondo)

        overlayWidget = Widget(size_hint=(1, 1))
        with overlayWidget.canvas:
            Color(0, 0, 0, 0.6)
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
        cajaTitulo = BoxLayout(size_hint=(1, None), height=dp(44), padding=[dp(8), dp(4)])
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

        # Contador de transmutadores
        self.etiquetaTransmutadores = Label(
            text='Transmutadores: —',
            font_size=dp(12),
            color=(0.9, 0.75, 0.3, 1),
            size_hint=(1, None),
            height=dp(24),
            halign='center',
            valign='middle'
        )
        self.etiquetaTransmutadores.bind(size=self.etiquetaTransmutadores.setter('text_size'))
        contenedorPrincipal.add_widget(self.etiquetaTransmutadores)

        # Panel central de combinación
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

        # Slots
        self.slotResultado = SlotForja(
            tipo='resultado',
            etiqueta='RESULTADO',
            size_hint=(None, None),
            size=(dp(80), dp(80)),
            pos_hint={'center_x': 0.5, 'center_y': 0.60}
        )
        self.slotIng1 = SlotForja(
            tipo='ingrediente',
            etiqueta='RUNA 1',
            size_hint=(None, None),
            size=(dp(70), dp(70)),
            pos_hint={'center_x': 0.25, 'center_y': 0.35}
        )
        self.slotIng2 = SlotForja(
            tipo='ingrediente',
            etiqueta='RUNA 2',
            size_hint=(None, None),
            size=(dp(70), dp(70)),
            pos_hint={'center_x': 0.75, 'center_y': 0.35}
        )
        # Guardar etiqueta default para limpiar
        self.slotIng1._etiqueta_default = 'RUNA 1'
        self.slotIng2._etiqueta_default = 'RUNA 2'
        self.slotResultado._etiqueta_default = 'RESULTADO'

        etiquetaFlecha = Label(
            text='↑',
            font_size=dp(22),
            color=(0.9, 0.75, 0.3, 0.6),
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            pos_hint={'center_x': 0.5, 'center_y': 0.47}
        )

        etiquetaInfo = Label(
            text='Pulsa una runa del inventario\npara asignarla al slot',
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
        panelCombinacion.add_widget(etiquetaFlecha)
        panelCombinacion.add_widget(etiquetaInfo)
        contenedorPrincipal.add_widget(panelCombinacion)

        # Lista de runas disponibles (scroll horizontal)
        from kivy.uix.scrollview import ScrollView
        scrollRunas = ScrollView(
            size_hint=(1, None),
            height=dp(60),
            do_scroll_x=True,
            do_scroll_y=False
        )
        self.filaRunas = BoxLayout(
            orientation='horizontal',
            size_hint=(None, 1),
            spacing=dp(6),
            padding=dp(4)
        )
        self.filaRunas.bind(minimum_width=self.filaRunas.setter('width'))
        scrollRunas.add_widget(self.filaRunas)
        contenedorPrincipal.add_widget(scrollRunas)

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
            self._rectBarraInf = RoundedRectangle(
                pos=barraInferior.pos, size=barraInferior.size,
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
            radius=8, size_hint=(1, 1), font_size=dp(11), bold=True
        )
        botonAtras.bind(on_press=self.volverAInventario)

        self.botonForjar = BotonRedondeado(
            text='⚒',
            bg_color=(*COLOR_ANOMALIAS[:3], 0.85),
            text_color=BLANCO,
            radius=50, size_hint=(None, 1), width=dp(54),
            font_size=dp(22), bold=True
        )
        self.botonForjar.bind(on_press=self.intentarForja)

        botonLimpiar = BotonRedondeado(
            text='LIMPIAR',
            bg_color=(0.05, 0.05, 0.1, 0.9),
            text_color=(*COLOR_GUARDIANES[:3], 1),
            radius=8, size_hint=(1, 1), font_size=dp(11), bold=True
        )
        botonLimpiar.bind(on_press=self.limpiarSlots)

        barraInferior.add_widget(botonAtras)
        barraInferior.add_widget(self.botonForjar)
        barraInferior.add_widget(botonLimpiar)
        contenedorPrincipal.add_widget(barraInferior)

        self.add_widget(overlayWidget)
        self.add_widget(contenedorPrincipal)

    # ── Kivy hooks ──────────────────────────────────────────

    def on_pre_enter(self, *args):
        self.limpiarSlots()
        self._refrescarTransmutadores()
        self._cargarRunasDisponibles()

    # ── Refresco de datos ────────────────────────────────────

    def _refrescarTransmutadores(self):
        if self.gm is None:
            return
        n = self.gm.get_transmutadores()
        self.etiquetaTransmutadores.text = f'Transmutadores: {n}'

    def _cargarRunasDisponibles(self):
        self.filaRunas.clear_widgets()
        if self.gm is None:
            return

        runas = self.gm.get_runas_basicas_jugador()
        if not runas:
            lbl = Label(
                text='No tienes runas básicas disponibles',
                font_size=dp(11),
                color=GRIS,
                size_hint=(None, 1),
                width=dp(200)
            )
            self.filaRunas.add_widget(lbl)
            return

        for runa in runas:
            btn = BotonRedondeado(
                text=runa.get('nombre', '?'),
                bg_color=(0.08, 0.08, 0.15, 0.95),
                text_color=(0.9, 0.75, 0.3, 1),
                radius=8,
                size_hint=(None, 1),
                width=dp(80),
                font_size=dp(10),
                bold=True
            )
            btn.bind(on_press=lambda _, r=runa: self._asignarRuna(r))
            self.filaRunas.add_widget(btn)

    def _asignarRuna(self, runa: dict):
        # Asigna al primer slot vacío; si ambos están llenos, reemplaza el slot 1
        if self.slotIng1.runa is None:
            self.slotIng1.asignar(runa)
        elif self.slotIng2.runa is None:
            self.slotIng2.asignar(runa)
        else:
            # Ambos llenos — reemplaza slot 1
            self.slotIng1.asignar(runa)
        # Limpiar resultado previo
        self.slotResultado.limpiar()

    # ── Acciones ─────────────────────────────────────────────

    def intentarForja(self, instance):
        if self.gm is None:
            return

        runa1 = self.slotIng1.runa
        runa2 = self.slotIng2.runa

        if runa1 is None or runa2 is None:
            self._mostrarPopup('Faltan runas', 'Coloca una runa en cada slot.', (0.7, 0.3, 0.1, 1))
            return

        resultado = self.gm.transmutar(runa1.get('nombre', ''), runa2.get('nombre', ''))

        if not resultado['ok']:
            self._mostrarPopup('Error', resultado['mensaje'], (0.7, 0.1, 0.1, 1))
            return

        # Mostrar resultado en el slot
        self.slotResultado.asignar(resultado['resultado'])
        self.slotIng1.limpiar()
        self.slotIng2.limpiar()

        color = (0.2, 0.8, 0.3, 1) if resultado['es_valida'] else (0.7, 0.1, 0.1, 1)
        self._mostrarPopup('Resultado', resultado['mensaje'], color)

        # Refrescar transmutadores y runas disponibles
        self._refrescarTransmutadores()
        self._cargarRunasDisponibles()

    def limpiarSlots(self, *args):
        self.slotIng1.runa     = None
        self.slotIng1.etiqueta = 'RUNA 1'
        self.slotIng1._redibujar()
        self.slotIng2.runa     = None
        self.slotIng2.etiqueta = 'RUNA 2'
        self.slotIng2._redibujar()
        self.slotResultado.runa     = None
        self.slotResultado.etiqueta = 'RESULTADO'
        self.slotResultado._redibujar()

    def _mostrarPopup(self, titulo, mensaje, color_titulo):
        from kivy.graphics import Color, RoundedRectangle
        modal = ModalView(size_hint=(0.8, 0.4), auto_dismiss=True, background_color=(0, 0, 0, 0))

        contenedor = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(12))
        with contenedor.canvas.before:
            Color(0.05, 0.05, 0.1, 0.97)
            RoundedRectangle(pos=contenedor.pos, size=contenedor.size, radius=[dp(16)])

        lbl_titulo = Label(
            text=titulo, font_size=dp(18), bold=True, color=color_titulo,
            size_hint=(1, None), height=dp(36), halign='center', valign='middle'
        )
        lbl_titulo.bind(size=lbl_titulo.setter('text_size'))

        lbl_msg = Label(
            text=mensaje, font_size=dp(12), color=BLANCO,
            size_hint=(1, 1), halign='center', valign='middle'
        )
        lbl_msg.bind(size=lbl_msg.setter('text_size'))

        btn = BotonRedondeado(
            text='OK', bg_color=COLOR_GUARDIANES, text_color=BLANCO,
            radius=10, size_hint=(1, None), height=dp(40),
            font_size=dp(13), bold=True
        )
        btn.bind(on_press=lambda _: modal.dismiss())

        contenedor.add_widget(lbl_titulo)
        contenedor.add_widget(lbl_msg)
        contenedor.add_widget(btn)
        modal.add_widget(contenedor)
        modal.open()

    # ── Helpers ───────────────────────────────────────────────

    def _actualizarCaja(self, widget, rect, borde):
        rect.pos  = widget.pos
        rect.size = widget.size
        borde.rounded_rectangle = (widget.x, widget.y, widget.width, widget.height, dp(10))

    def _actualizarPanel(self, panel):
        self._panelRect.pos  = panel.pos
        self._panelRect.size = panel.size
        self._panelBorde.rounded_rectangle = (panel.x, panel.y, panel.width, panel.height, dp(12))

    def _actualizarFondo(self, *args):
        self._bg_rect.pos  = self.pos
        self._bg_rect.size = self.size

    def volverAInventario(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'inventario'