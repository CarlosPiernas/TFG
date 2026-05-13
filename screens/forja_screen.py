from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.modalview import ModalView
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp
from widgets.responsive import sw, sh, sf, sdp
from config import (
    PANEL_OSCURO, PANEL_MEDIO,
    COLOR_ANOMALIAS, COLOR_GUARDIANES, BLANCO, GRIS,
    FONDO_FORJA_GUARDIAN, FONDO_FORJA_ANOMALIA,
    SLOT_RUNA_GUARDIAN, SLOT_RUNA_ANOMALIA, SLOT_RUNA_RESULTADO,
    ICONO_FORJAR, MARCO_BOTON, BOTON_FORJAR,
    ICONO_TRANSMUTADOR,
    FLECHA_TRANSMUTAR_GUARDIAN, FLECHA_TRANSMUTAR_ANOMALIA,
    CABECERA_FORJA,
    PLACEHOLDER,
    icono_runa, nombre_runa,
)
from widgets.componentes import BotonRedondeado


# ── Image que se comporta como botón ───────────────────────────────────────
class IconoClicable(ButtonBehavior, Image):
    pass


# ── Slot de runa visual ────────────────────────────────────────────────────
class SlotRunaVisual(FloatLayout):
    def __init__(self, fondo_path, **kwargs):
        super().__init__(**kwargs)
        self.runa = None
        self._fondo_path = fondo_path

        self.imagenFondo = Image(
            source=fondo_path,
            allow_stretch=True,
            keep_ratio=True,
            mipmap=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(1, 1)
        )
        self.add_widget(self.imagenFondo)

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
        self.imagenRuna.source = icono_runa(runa.get('nombre', ''))
        self.imagenRuna.reload()
        self.imagenRuna.opacity = 1

    def limpiar(self):
        self.runa = None
        self.imagenRuna.source  = ''
        self.imagenRuna.opacity = 0

    def cambiar_fondo(self, fondo_path):
        self._fondo_path = fondo_path
        self.imagenFondo.source = fondo_path
        self.imagenFondo.reload()


# ── Botón con marco decorativo ─────────────────────────────────────────────
class BotonConMarco(FloatLayout):
    def __init__(self, texto='VOLVER', marco_path=MARCO_BOTON,
                 on_press_callback=None, **kwargs):
        super().__init__(**kwargs)
        self._on_press_callback = on_press_callback

        self.imagenMarco = Image(
            source=marco_path,
            allow_stretch=True,
            keep_ratio=False,
            mipmap=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(1, 1)
        )
        self.add_widget(self.imagenMarco)

        self.boton = Button(
            text=texto,
            background_normal='',
            background_color=(0, 0, 0, 0),
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

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self._bg_rect = Rectangle(
                source=FONDO_FORJA_GUARDIAN,
                pos=self.pos,
                size=self.size
            )
        self.bind(pos=self._actualizarFondo, size=self._actualizarFondo)

        with self.canvas.before:
            Color(0, 0, 0, 0.35)
            self._overlay = Rectangle(pos=self.pos, size=self.size)
        self.bind(
            pos=lambda *a: setattr(self._overlay, 'pos', self.pos),
            size=lambda *a: setattr(self._overlay, 'size', self.size)
        )

        raiz = BoxLayout(orientation='vertical', spacing=0)

        cabecera = Image(
            source=CABECERA_FORJA,
            allow_stretch=True,
            keep_ratio=True,
            mipmap=True,
            size_hint=(1, 0.18)
        )

        filaContador = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.08),
            padding=[dp(8), dp(4)]
        )
        filaContador.add_widget(Widget(size_hint=(1, 1)))

        cerdaContador = BoxLayout(
            orientation='horizontal',
            size_hint=(None, 1),
            width=sw(110),
            spacing=dp(4),
            padding=[dp(10), dp(4)]
        )
        with cerdaContador.canvas.before:
            Color(0, 0, 0, 0.7)
            self._cerdaRect = RoundedRectangle(
                pos=cerdaContador.pos,
                size=cerdaContador.size,
                radius=[dp(14)]
            )
        cerdaContador.bind(
            pos=lambda *a: setattr(self._cerdaRect, 'pos', cerdaContador.pos),
            size=lambda *a: setattr(self._cerdaRect, 'size', cerdaContador.size)
        )

        self.iconoTransmutador = Image(
            source=ICONO_TRANSMUTADOR,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(None, 1),
            width=sw(28),
            mipmap=True
        )
        cerdaContador.add_widget(self.iconoTransmutador)

        self.etiquetaTransmutadores = Label(
            text=': 0',
            font_size=sf(15),
            bold=True,
            color=BLANCO,
            halign='left',
            valign='middle',
            size_hint=(1, 1)
        )
        self.etiquetaTransmutadores.bind(size=self.etiquetaTransmutadores.setter('text_size'))
        cerdaContador.add_widget(self.etiquetaTransmutadores)

        filaContador.add_widget(cerdaContador)
        filaContador.add_widget(Widget(size_hint=(1, 1)))

        zonaFusion = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.44),
            padding=[dp(12), dp(8)],
            spacing=dp(4)
        )

        columnaEntradas = BoxLayout(
            orientation='vertical',
            size_hint=(0.32, 1),
            spacing=dp(12),
            padding=[dp(8), dp(8)]
        )
        self.slotIng1 = SlotRunaVisual(SLOT_RUNA_GUARDIAN, size_hint=(1, 1))
        self.slotIng2 = SlotRunaVisual(SLOT_RUNA_GUARDIAN, size_hint=(1, 1))
        columnaEntradas.add_widget(self.slotIng1)
        columnaEntradas.add_widget(self.slotIng2)

        self.slotIng1.bind(on_touch_down=self._touchSlotIng1)
        self.slotIng2.bind(on_touch_down=self._touchSlotIng2)

        columnaFlecha = BoxLayout(
            orientation='vertical',
            size_hint=(0.36, 1),
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

        columnaResultado = BoxLayout(
            orientation='vertical',
            size_hint=(0.32, 1),
            padding=[dp(8), dp(8)]
        )
        columnaResultado.add_widget(Widget(size_hint=(1, 0.20)))
        self.slotResultado = SlotRunaVisual(SLOT_RUNA_RESULTADO, size_hint=(1, 0.60))
        columnaResultado.add_widget(self.slotResultado)
        columnaResultado.add_widget(Widget(size_hint=(1, 0.20)))

        zonaFusion.add_widget(columnaEntradas)
        zonaFusion.add_widget(columnaFlecha)
        zonaFusion.add_widget(columnaResultado)

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

        botonVolver = BotonConMarco(
            texto='VOLVER',
            marco_path=MARCO_BOTON,
            on_press_callback=self.volverAInventario,
            size_hint=(0.5, 1)
        )
        botonForjar = BotonConMarco(
            texto='FORJAR',
            marco_path=MARCO_BOTON,
            on_press_callback=self.intentarForja,
            size_hint=(0.5, 1)
        )

        botonera.add_widget(botonVolver)
        botonera.add_widget(botonForjar)

        raiz.add_widget(cabecera)
        raiz.add_widget(filaContador)
        raiz.add_widget(zonaFusion)
        raiz.add_widget(contenedorInventario)
        raiz.add_widget(botonera)
        self.add_widget(raiz)

    # ── Ciclo de vida ────────────────────────────────────────────────────

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
        self.etiquetaTransmutadores.text = f': {n}'

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
            self.filaRunas.add_widget(self._crearTarjetaRuna(runa))

    def _crearTarjetaRuna(self, runa: dict):
        """Tarjeta: icono arriba + nombre display (bonito) debajo."""
        contenedor = BoxLayout(
            orientation='vertical',
            size_hint=(None, 1),
            width=dp(90),
            padding=[dp(4), dp(4)],
            spacing=dp(2),
        )

        img = IconoClicable(
            source=icono_runa(runa.get('nombre', '')),
            allow_stretch=True,
            keep_ratio=True,
            mipmap=True,
            size_hint=(1, 0.65),
        )
        img.bind(on_press=lambda _, r=runa: self._asignarRuna(r))
        contenedor.add_widget(img)

        # ── CAMBIO: nombre_runa() en lugar de runa.get('nombre') ──────────
        btn = Button(
            text=nombre_runa(runa.get('nombre', '?')),
            background_color=(0.08, 0.08, 0.15, 0.95),
            background_normal='',
            color=(0.9, 0.75, 0.3, 1),
            font_size=dp(9),
            bold=True,
            size_hint=(1, 0.35),
        )
        btn.bind(on_press=lambda _, r=runa: self._asignarRuna(r))
        contenedor.add_widget(btn)

        return contenedor

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
                'Ups!',
                'Coloca una runa en cada slot.',
                (0.7, 0.3, 0.1, 1)
            )
            return

        resultado = self.gm.transmutar(runa1.get('nombre', ''), runa2.get('nombre', ''))

        if not resultado['ok']:
            self._mostrarPopup('Ups!', resultado['mensaje'], (0.7, 0.1, 0.1, 1))
            return

        self.slotResultado.asignar(resultado['resultado'])
        self.slotIng1.limpiar()
        self.slotIng2.limpiar()

        # ── CAMBIO: popup con icono + nombre display de la runa resultante
        runa_res     = resultado['resultado']
        nombre_res   = nombre_runa(runa_res.get('nombre', ''))
        icono_res    = icono_runa(runa_res.get('nombre', ''))
        es_valida    = resultado['es_valida']
        color_popup  = (0.2, 0.8, 0.3, 1) if es_valida else (0.7, 0.1, 0.1, 1)
        titulo_popup = 'Transmutacion exitosa' if es_valida else 'Transmutacion fallida'

        self._mostrarPopupResultado(titulo_popup, icono_res, nombre_res, color_popup)

        self._refrescarTransmutadores()
        self._cargarRunasDisponibles()

    # ── Popups ───────────────────────────────────────────────────────────

    def _mostrarPopupResultado(self, titulo, icono_path, nombre_display, color_titulo):
        """Popup de resultado de transmutación: icono grande + nombre display."""
        modal = ModalView(
            size_hint=(0.75, 0.45),
            auto_dismiss=True,
            background_color=(0, 0, 0, 0)
        )

        contenedor = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(10))
        with contenedor.canvas.before:
            Color(0.05, 0.05, 0.1, 0.97)
            self._popRect = RoundedRectangle(pos=contenedor.pos, size=contenedor.size, radius=[dp(16)])
        contenedor.bind(
            pos=lambda *a: setattr(self._popRect, 'pos', contenedor.pos),
            size=lambda *a: setattr(self._popRect, 'size', contenedor.size)
        )

        # Título
        lbl_titulo = Label(
            text=titulo,
            font_size=dp(16), bold=True, color=color_titulo,
            size_hint=(1, None), height=dp(30),
            halign='center', valign='middle'
        )
        lbl_titulo.bind(size=lbl_titulo.setter('text_size'))
        contenedor.add_widget(lbl_titulo)

        # Icono de la runa resultante
        img_resultado = Image(
            source=icono_path,
            allow_stretch=True,
            keep_ratio=True,
            mipmap=True,
            size_hint=(1, 1),
        )
        contenedor.add_widget(img_resultado)

        # Nombre display
        lbl_nombre = Label(
            text=nombre_display,
            font_size=dp(15), bold=True, color=BLANCO,
            size_hint=(1, None), height=dp(28),
            halign='center', valign='middle'
        )
        lbl_nombre.bind(size=lbl_nombre.setter('text_size'))
        contenedor.add_widget(lbl_nombre)

        # Botón OK
        btn = BotonRedondeado(
            text='OK', bg_color=COLOR_GUARDIANES, text_color=BLANCO,
            radius=10, size_hint=(0.5, None), height=dp(38),
            font_size=dp(13), bold=True,
            pos_hint={'center_x': 0.5}
        )
        btn.bind(on_press=lambda _: modal.dismiss())
        contenedor.add_widget(btn)

        modal.add_widget(contenedor)
        modal.open()

    def _mostrarPopup(self, titulo, mensaje, color_titulo):
        """Popup genérico de texto (errores, avisos)."""
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