from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp
from config import (
    PANEL_OSCURO, PANEL_MEDIO,
    COLOR_ANOMALIAS, COLOR_GUARDIANES, BLANCO, GRIS,
    FONDO_FORJA_GUARDIAN, FONDO_FORJA_ANOMALIA,
    SLOT_RUNA_GUARDIAN, SLOT_RUNA_ANOMALIA, SLOT_RUNA_RESULTADO,
    ICONO_FORJAR, MARCO_BOTON, BOTON_FORJAR,
    ICONO_TRANSMUTADOR,
    FLECHA_TRANSMUTAR_GUARDIAN, FLECHA_TRANSMUTAR_ANOMALIA,
    PLACEHOLDER
)
from widgets.componentes import BotonRedondeado


# ── Slot de runa visual (fondo PNG + icono de la runa superpuesto) ─────────
class SlotRunaVisual(FloatLayout):
    """
    Slot decorativo redondo. Capas:
      1. Image con el PNG del altar (fondo)
      2. Image con el icono de la runa asignada (encima, centrada)
    Si no hay runa asignada, la capa 2 se oculta (opacity=0) para que no
    se vea ningún recuadro blanco/placeholder en pantalla.
    """
    def __init__(self, fondo_path, **kwargs):
        super().__init__(**kwargs)
        self.runa = None  # dict de la runa asignada o None
        self._fondo_path = fondo_path

        # Capa 1: fondo del slot (siempre visible)
        self.imagenFondo = Image(
            source=fondo_path,
            allow_stretch=True,
            keep_ratio=True,
            mipmap=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(1, 1)
        )
        self.add_widget(self.imagenFondo)

        # Capa 2: icono de la runa. Oculto al inicio (opacity=0).
        # Ocupa solo el círculo central del altar, no todo el slot.
        self.imagenRuna = Image(
            source='',
            allow_stretch=True,
            keep_ratio=True,
            mipmap=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.45, 0.45),
            opacity=0
        )
        self.add_widget(self.imagenRuna)

    def asignar(self, runa: dict):
        self.runa = runa
        # Cuando los iconos por runa estén listos, leer aquí:
        # self.imagenRuna.source = runa.get('icono', PLACEHOLDER)
        self.imagenRuna.source = PLACEHOLDER
        self.imagenRuna.reload()
        self.imagenRuna.opacity = 1

    def limpiar(self):
        self.runa = None
        self.imagenRuna.source  = ''
        self.imagenRuna.opacity = 0

    def cambiar_fondo(self, fondo_path):
        # Permite cambiar el PNG del altar (al cambiar de facción).
        self._fondo_path = fondo_path
        self.imagenFondo.source = fondo_path
        self.imagenFondo.reload()


# ── Botón con marco decorativo (PNG de fondo + texto encima) ───────────────
class BotonConMarco(FloatLayout):
    """
    Botón con un PNG de marco decorativo de fondo y texto encima.
    Capas:
      1. Image con el marco (PNG)
      2. Button transparente que recibe el click + Label con el texto
    """
    def __init__(self, texto='VOLVER', marco_path=MARCO_BOTON,
                 on_press_callback=None, **kwargs):
        super().__init__(**kwargs)
        self._on_press_callback = on_press_callback

        # Capa 1: marco decorativo
        self.imagenMarco = Image(
            source=marco_path,
            allow_stretch=True,
            keep_ratio=False,
            mipmap=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(1, 1)
        )
        self.add_widget(self.imagenMarco)

        # Capa 2: botón transparente con el texto encima
        self.boton = Button(
            text=texto,
            background_normal='',
            background_color=(0, 0, 0, 0),  # totalmente transparente
            color=BLANCO,
            font_size=dp(15),
            bold=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(1, 1)
        )
        if on_press_callback is not None:
            self.boton.bind(on_press=on_press_callback)
        self.add_widget(self.boton)


class PantallaForja(Screen):
    def __init__(self, gm=None, **kwargs):
        super().__init__(**kwargs)
        self.gm = gm

        # ── Fondo de pantalla (cambia según facción en on_pre_enter) ──────
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self._bg_rect = Rectangle(
                source=FONDO_FORJA_GUARDIAN,
                pos=self.pos,
                size=self.size
            )
        self.bind(pos=self._actualizarFondo, size=self._actualizarFondo)

        # Velo oscuro para mejorar contraste del contenido sobre el fondo
        with self.canvas.before:
            Color(0, 0, 0, 0.35)
            self._overlay = Rectangle(pos=self.pos, size=self.size)
        self.bind(
            pos=lambda *a: setattr(self._overlay, 'pos', self.pos),
            size=lambda *a: setattr(self._overlay, 'size', self.size)
        )

        raiz = BoxLayout(orientation='vertical', spacing=0)

        # ══════════════════════════════════════════════════════════════════
        # CABECERA (12%) — Título "FORJA"
        # ══════════════════════════════════════════════════════════════════
        cabecera = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.12),
            padding=[dp(8), dp(8)]
        )
        with cabecera.canvas.before:
            Color(0, 0, 0, 0.55)
            self._cabRect = Rectangle(pos=cabecera.pos, size=cabecera.size)
        cabecera.bind(
            pos=lambda *a: setattr(self._cabRect, 'pos', cabecera.pos),
            size=lambda *a: setattr(self._cabRect, 'size', cabecera.size)
        )

        lblTitulo = Label(
            text='— FORJA —',
            font_size=dp(22),
            bold=True,
            color=COLOR_GUARDIANES,
            halign='center',
            valign='middle'
        )
        lblTitulo.bind(size=lblTitulo.setter('text_size'))
        cabecera.add_widget(lblTitulo)

        # ══════════════════════════════════════════════════════════════════
        # CONTADOR DE TRANSMUTADORES (8%) — "Transmutadores: N" + icono
        # ══════════════════════════════════════════════════════════════════
        filaContador = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.08),
            padding=[dp(20), dp(4)],
            spacing=dp(8)
        )
        filaContador.add_widget(Widget(size_hint=(1, 1)))

        self.etiquetaTransmutadores = Label(
            text='Transmutadores: 0',
            font_size=dp(14),
            bold=True,
            color=BLANCO,
            halign='right',
            valign='middle',
            size_hint=(None, 1),
            width=dp(180)
        )
        self.etiquetaTransmutadores.bind(size=self.etiquetaTransmutadores.setter('text_size'))
        filaContador.add_widget(self.etiquetaTransmutadores)

        self.iconoTransmutador = Image(
            source=ICONO_TRANSMUTADOR,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(None, 1),
            width=dp(32),
            mipmap=True
        )
        filaContador.add_widget(self.iconoTransmutador)

        filaContador.add_widget(Widget(size_hint=(1, 1)))

        # ══════════════════════════════════════════════════════════════════
        # ZONA DE FUSIÓN (50%) — Runa1+Runa2 (izq) → Resultado (der)
        # ══════════════════════════════════════════════════════════════════
        zonaFusion = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.50),
            padding=[dp(12), dp(8)],
            spacing=dp(4)
        )

        # Columna izquierda: dos slots de entrada apilados
        columnaEntradas = BoxLayout(
            orientation='vertical',
            size_hint=(0.35, 1),
            spacing=dp(12),
            padding=[dp(8), dp(8)]
        )
        self.slotIng1 = SlotRunaVisual(SLOT_RUNA_GUARDIAN, size_hint=(1, 1))
        self.slotIng2 = SlotRunaVisual(SLOT_RUNA_GUARDIAN, size_hint=(1, 1))
        columnaEntradas.add_widget(self.slotIng1)
        columnaEntradas.add_widget(self.slotIng2)

        # Click en slot lleno → limpiar ese slot
        self.slotIng1.bind(on_touch_down=self._touchSlotIng1)
        self.slotIng2.bind(on_touch_down=self._touchSlotIng2)

        # Columna central: flecha decorativa (PNG, cambia según facción)
        columnaFlecha = BoxLayout(
            orientation='vertical',
            size_hint=(0.30, 1),
            padding=[dp(2), dp(8)]
        )
        self.imgFlecha = Image(
            source=FLECHA_TRANSMUTAR_GUARDIAN,
            allow_stretch=True,
            keep_ratio=True,
            mipmap=True,
            size_hint=(1, 1)
        )
        columnaFlecha.add_widget(self.imgFlecha)

        # Columna derecha: slot resultado (más pequeño, centrado verticalmente)
        columnaResultado = BoxLayout(
            orientation='vertical',
            size_hint=(0.35, 1),
            padding=[dp(8), dp(8)]
        )
        columnaResultado.add_widget(Widget(size_hint=(1, 0.20)))
        self.slotResultado = SlotRunaVisual(SLOT_RUNA_RESULTADO, size_hint=(1, 0.60))
        columnaResultado.add_widget(self.slotResultado)
        columnaResultado.add_widget(Widget(size_hint=(1, 0.20)))

        zonaFusion.add_widget(columnaEntradas)
        zonaFusion.add_widget(columnaFlecha)
        zonaFusion.add_widget(columnaResultado)

        # ══════════════════════════════════════════════════════════════════
        # INVENTARIO DE RUNAS (15%) — scroll horizontal con runas básicas
        # ══════════════════════════════════════════════════════════════════
        contenedorInventario = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.15),
            padding=[dp(8), dp(4)]
        )
        with contenedorInventario.canvas.before:
            Color(0, 0, 0, 0.55)
            self._invRect = Rectangle(pos=contenedorInventario.pos, size=contenedorInventario.size)
        contenedorInventario.bind(
            pos=lambda *a: setattr(self._invRect, 'pos', contenedorInventario.pos),
            size=lambda *a: setattr(self._invRect, 'size', contenedorInventario.size)
        )

        scrollInv = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=True,
            do_scroll_y=False,
            bar_width=dp(4)
        )
        self.filaRunas = BoxLayout(
            orientation='horizontal',
            size_hint=(None, 1),
            spacing=dp(8),
            padding=[dp(6), dp(2)]
        )
        self.filaRunas.bind(minimum_width=self.filaRunas.setter('width'))
        scrollInv.add_widget(self.filaRunas)
        contenedorInventario.add_widget(scrollInv)

        # ══════════════════════════════════════════════════════════════════
        # BOTONERA INFERIOR (15%) — [Volver con marco]   [Forjar (icono yunque)]
        # ══════════════════════════════════════════════════════════════════
        botonera = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.15),
            padding=[dp(20), dp(10)],
            spacing=dp(20)
        )
        with botonera.canvas.before:
            Color(0, 0, 0, 0.55)
            self._botRect = Rectangle(pos=botonera.pos, size=botonera.size)
        botonera.bind(
            pos=lambda *a: setattr(self._botRect, 'pos', botonera.pos),
            size=lambda *a: setattr(self._botRect, 'size', botonera.size)
        )

        # Botón VOLVER — con marco decorativo Boton.png + texto "VOLVER" encima
        botonVolver = BotonConMarco(
            texto='VOLVER',
            marco_path=MARCO_BOTON,
            on_press_callback=self.volverAInventario,
            size_hint=(0.5, 1)
        )

        # Botón FORJAR — con marco decorativo BotonForjar.png + texto "FORJAR"
        botonForjar = BotonConMarco(
            texto='FORJAR',
            marco_path=BOTON_FORJAR,
            on_press_callback=self.intentarForja,
            size_hint=(0.5, 1)
        )

        botonera.add_widget(botonVolver)
        botonera.add_widget(botonForjar)

        # ══════════════════════════════════════════════════════════════════
        # MONTAJE FINAL: cabecera (12) + contador (8) + fusión (50) +
        #                inventario (15) + botonera (15) = 100%
        # ══════════════════════════════════════════════════════════════════
        raiz.add_widget(cabecera)
        raiz.add_widget(filaContador)
        raiz.add_widget(zonaFusion)
        raiz.add_widget(contenedorInventario)
        raiz.add_widget(botonera)
        self.add_widget(raiz)

    # ── Eventos del ciclo de vida ────────────────────────────────────────

    def on_pre_enter(self, *args):
        self._aplicarFaccion()
        self.limpiarSlots()
        self._refrescarTransmutadores()
        self._cargarRunasDisponibles()

    def _aplicarFaccion(self):
        if self.gm is None:
            return
        if self.gm.faccion == 'anomalia':
            self._bg_rect.source = FONDO_FORJA_ANOMALIA
            slot_path = SLOT_RUNA_ANOMALIA
            self.imgFlecha.source = FLECHA_TRANSMUTAR_ANOMALIA
        else:
            self._bg_rect.source = FONDO_FORJA_GUARDIAN
            slot_path = SLOT_RUNA_GUARDIAN
            self.imgFlecha.source = FLECHA_TRANSMUTAR_GUARDIAN

        self.slotIng1.cambiar_fondo(slot_path)
        self.slotIng2.cambiar_fondo(slot_path)
        self.imgFlecha.reload()

    # ── Refresco de datos ────────────────────────────────────────────────

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
                width=dp(100),
                font_size=dp(10),
                bold=True
            )
            btn.bind(on_press=lambda _, r=runa: self._asignarRuna(r))
            self.filaRunas.add_widget(btn)

    # ── Asignación / limpieza de slots ───────────────────────────────────

    def _asignarRuna(self, runa: dict):
        if self.slotIng1.runa is None:
            self.slotIng1.asignar(runa)
        elif self.slotIng2.runa is None:
            self.slotIng2.asignar(runa)
        else:
            self.slotIng1.asignar(runa)
        self.slotResultado.limpiar()

    def _touchSlotIng1(self, instance, touch):
        # Click en slot lleno → limpiar ese slot.
        if instance.collide_point(*touch.pos) and instance.runa is not None:
            instance.limpiar()
            return True
        return False

    def _touchSlotIng2(self, instance, touch):
        if instance.collide_point(*touch.pos) and instance.runa is not None:
            instance.limpiar()
            return True
        return False

    def limpiarSlots(self, *args):
        self.slotIng1.limpiar()
        self.slotIng2.limpiar()
        self.slotResultado.limpiar()

    # ── Acción principal: transmutar ─────────────────────────────────────

    def intentarForja(self, instance):
        if self.gm is None:
            return

        runa1 = self.slotIng1.runa
        runa2 = self.slotIng2.runa

        if runa1 is None or runa2 is None:
            self._mostrarPopup(
                'Faltan runas',
                'Coloca una runa en cada slot.',
                (0.7, 0.3, 0.1, 1)
            )
            return

        resultado = self.gm.transmutar(runa1.get('nombre', ''), runa2.get('nombre', ''))

        if not resultado['ok']:
            self._mostrarPopup('Error', resultado['mensaje'], (0.7, 0.1, 0.1, 1))
            return

        self.slotResultado.asignar(resultado['resultado'])
        self.slotIng1.limpiar()
        self.slotIng2.limpiar()

        color = (0.2, 0.8, 0.3, 1) if resultado['es_valida'] else (0.7, 0.1, 0.1, 1)
        self._mostrarPopup('Resultado', resultado['mensaje'], color)

        self._refrescarTransmutadores()
        self._cargarRunasDisponibles()

    # ── Popup auxiliar ───────────────────────────────────────────────────

    def _mostrarPopup(self, titulo, mensaje, color_titulo):
        modal = ModalView(
            size_hint=(0.8, 0.4),
            auto_dismiss=True,
            background_color=(0, 0, 0, 0)
        )

        contenedor = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(12))
        with contenedor.canvas.before:
            Color(0.05, 0.05, 0.1, 0.97)
            self._popRect = RoundedRectangle(pos=contenedor.pos, size=contenedor.size, radius=[dp(16)])
        contenedor.bind(
            pos=lambda *a: setattr(self._popRect, 'pos', contenedor.pos),
            size=lambda *a: setattr(self._popRect, 'size', contenedor.size)
        )

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

    # ── Helpers ──────────────────────────────────────────────────────────

    def _actualizarFondo(self, *args):
        self._bg_rect.pos  = self.pos
        self._bg_rect.size = self.size

    def volverAInventario(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'inventario'