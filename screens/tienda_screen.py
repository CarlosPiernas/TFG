from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.modalview import ModalView
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

from widgets.componentes import BotonRedondeado
from config import (
    BLANCO, COLOR_GUARDIANES, FONDO_PRINCIPAL,
    FONDO_TIENDA, TITULO_TIENDA, BOTON_COMPRAR, BOTON_VOLVER,
    FRAGMENTO_ROJO, FRAGMENTO_AZUL, ICONO_TRANSMUTADOR,
    ICONO_MONEDA, TICKET_PERSONAJES, TICKET_ARMAS,
    PLACEHOLDER, LOGO_POCION
)

PRODUCTOS_MONEDAS = [
    {'id': 'pocion',           'nombre': 'Poción',           'icono': LOGO_POCION,        'precio': 30,  'icono_divisa': ICONO_MONEDA},
    {'id': 'transmutador',     'nombre': 'Transmutador',     'icono': ICONO_TRANSMUTADOR, 'precio': 100, 'icono_divisa': ICONO_MONEDA},
    {'id': 'ticket_personaje', 'nombre': 'Ticket Personaje', 'icono': TICKET_PERSONAJES,  'precio': 200, 'icono_divisa': ICONO_MONEDA},
    {'id': 'ticket_arma',      'nombre': 'Ticket Arma',      'icono': TICKET_ARMAS,       'precio': 150, 'icono_divisa': ICONO_MONEDA},
]

PRODUCTOS_FRAGMENTOS = [
    {'id': 'ticket_personaje_frags', 'nombre': 'Ticket Personaje', 'icono': TICKET_PERSONAJES, 'precio': 50, 'icono_divisa': FRAGMENTO_ROJO},
    {'id': 'ticket_arma_frags',      'nombre': 'Ticket Arma',      'icono': TICKET_ARMAS,      'precio': 50, 'icono_divisa': FRAGMENTO_AZUL},
]


class FilaProducto(BoxLayout):
    def __init__(self, producto, on_seleccionar, **kwargs):
        super().__init__(**kwargs)
        self.producto        = producto
        self.orientation     = 'horizontal'
        self.size_hint       = (0.4, None)
        self.height          = dp(62)
        self.padding         = [dp(12), dp(6)]
        self.spacing         = dp(8)
        self._seleccionado   = False
        self._on_seleccionar = on_seleccionar

        with self.canvas.before:
            self._color_bg = Color(0, 0, 0, 0)
            self._rect_bg  = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
        self.bind(
            pos=lambda *a: setattr(self._rect_bg, 'pos', self.pos),
            size=lambda *a: setattr(self._rect_bg, 'size', self.size)
        )

        self.add_widget(Image(
            source=producto['icono'],
            size_hint=(None, 1),
            width=dp(36),
            allow_stretch=True,
            keep_ratio=True,
            mipmap=True
        ))

        lbl_nombre = Label(
            text=producto['nombre'],
            font_size=dp(13),
            bold=True,
            color=BLANCO,
            size_hint=(1, 1),
            halign='left',
            valign='middle'
        )
        lbl_nombre.bind(size=lbl_nombre.setter('text_size'))
        self.add_widget(lbl_nombre)

        self.bind(on_touch_down=self._on_toque)

    def _on_toque(self, instance, touch):
        if self.collide_point(*touch.pos):
            self._on_seleccionar(self)
            return True

    def seleccionar(self):
        self._seleccionado  = True
        self._color_bg.rgba = (1, 1, 1, 0.15)

    def deseleccionar(self):
        self._seleccionado  = False
        self._color_bg.rgba = (0, 0, 0, 0)


class PantallaTienda(Screen):
    def __init__(self, gm=None, **kwargs):
        super().__init__(**kwargs)
        self.gm                 = gm
        self._fila_seleccionada = None

        raiz = FloatLayout()

        # ── FONDO ─────────────────────────────────────────────────────────────
        raiz.add_widget(Image(
            source=FONDO_TIENDA,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0},
            mipmap=True
        ))

        # ── TÍTULO ────────────────────────────────────────────────────────────
        raiz.add_widget(Image(
            source=TITULO_TIENDA,
            size_hint=(0.7, 0.1),
            pos_hint={'center_x': 0.5, 'top': 1.0},
            allow_stretch=True,
            keep_ratio=True,
            mipmap=True
        ))

        # ── FILAS DE PRODUCTOS ────────────────────────────────────────────────
        todos = PRODUCTOS_MONEDAS + PRODUCTOS_FRAGMENTOS
        tops  = [0.88, 0.79, 0.70, 0.61, 0.52, 0.43]

        self._filas = []
        for i, p in enumerate(todos):
            fila = FilaProducto(p, self._seleccionar_producto)
            fila.pos_hint = {'center_x': 0.55, 'top': tops[i]}
            self._filas.append(fila)
            raiz.add_widget(fila)

        # ── RECURSOS ──────────────────────────────────────────────────────────    
        filaRecursos = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.05),
            pos_hint={'center_x': 0.5, 'y': 0.32},
            spacing=dp(12),
            padding=[dp(16), 0]
        )
        with filaRecursos.canvas.before:
            Color(0, 0, 0, 0.55)
            self._bgRecursos = RoundedRectangle(
                pos=filaRecursos.pos,
                size=filaRecursos.size,
                radius=[dp(0)]
            )
        filaRecursos.bind(
            pos=lambda *a: setattr(self._bgRecursos, 'pos', filaRecursos.pos),
            size=lambda *a: setattr(self._bgRecursos, 'size', filaRecursos.size)
        )

        def _recurso_widget(icono, attr):
            fila = BoxLayout(orientation='horizontal', size_hint=(None, 1), width=dp(80), spacing=dp(4))
            fila.add_widget(Image(source=icono, size_hint=(None, 1), width=dp(20), allow_stretch=True, keep_ratio=True, mipmap=True))
            lbl = Label(font_size=dp(12), bold=True, color=COLOR_GUARDIANES, size_hint=(1, 1), halign='left', valign='middle')
            lbl.bind(size=lbl.setter('text_size'))
            fila.add_widget(lbl)
            setattr(self, attr, lbl)
            return fila

        filaRecursos.add_widget(Widget(size_hint=(1, 1)))
        filaRecursos.add_widget(_recurso_widget(ICONO_MONEDA,   'lblMonedas'))
        filaRecursos.add_widget(_recurso_widget(FRAGMENTO_ROJO, 'lblFragRojos'))
        filaRecursos.add_widget(_recurso_widget(FRAGMENTO_AZUL, 'lblFragAzules'))
        filaRecursos.add_widget(Widget(size_hint=(1, 1)))
        raiz.add_widget(filaRecursos)

        # ── BOTÓN COMPRAR ─────────────────────────────────────────────────────
        panelComprar = BoxLayout(
            orientation='horizontal',
            size_hint=(0.88, 0.09),
            pos_hint={'center_x': 0.5, 'y': 0.20},
            spacing=dp(8)
        )

        self.btnComprar = Button(
            background_normal=BOTON_COMPRAR,
            background_down=BOTON_COMPRAR,
            background_color=(1, 1, 1, 0.5),
            border=(0, 0, 0, 0),
            size_hint=(1, 1),
            mipmap=True
        )
        self.btnComprar.bind(on_press=self._confirmar_compra)

        self.filaPrecioSeleccionado = BoxLayout(
            orientation='horizontal',
            size_hint=(None, 1),
            width=dp(80),
            spacing=dp(4)
        )
        self.lblPrecioSeleccionado = Label(
            text='',
            font_size=dp(14),
            bold=True,
            color=COLOR_GUARDIANES,
            size_hint=(1, 1),
            halign='right',
            valign='middle'
        )
        self.lblPrecioSeleccionado.bind(size=self.lblPrecioSeleccionado.setter('text_size'))
        self.iconoDivisaSeleccionada = Image(
            source=ICONO_MONEDA,
            size_hint=(None, 1),
            width=dp(24),
            allow_stretch=True,
            keep_ratio=True,
            mipmap=True
        )
        self.filaPrecioSeleccionado.add_widget(self.lblPrecioSeleccionado)
        self.filaPrecioSeleccionado.add_widget(self.iconoDivisaSeleccionada)
        panelComprar.add_widget(self.btnComprar)
        panelComprar.add_widget(self.filaPrecioSeleccionado)
        raiz.add_widget(panelComprar)

        # ── NAVEGACIÓN ────────────────────────────────────────────────────────
        barraNav = BoxLayout(
            orientation='horizontal',
            size_hint=(0.88, 0.10),
            pos_hint={'center_x': 0.5, 'y': 0.08},
            spacing=dp(10)
        )

        btnVolver = Button(
            text='VOLVER',
            background_normal=BOTON_VOLVER,
            background_down=BOTON_VOLVER,
            background_color=(1, 1, 1, 1),
            color=BLANCO,
            bold=True,
            font_size=dp(13),
            border=(0, 0, 0, 0),
            size_hint=(1, 1),
            mipmap=True
        )
        btnVolver.bind(on_press=self._ir_al_gacha_o_home)
        barraNav.add_widget(btnVolver)
        raiz.add_widget(barraNav)

        self.add_widget(raiz)

    # ── Ciclo de vida ─────────────────────────────────────────────────────────

    def on_pre_enter(self, *args):
        self._refrescar_recursos()
        self._deseleccionar_todo()

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _refrescar_recursos(self):
        if self.gm is None:
            return
        r = self.gm.get_recursos_tienda()
        self.lblMonedas.text    = str(r.get('monedas', 0))
        self.lblFragRojos.text  = str(r.get('fragmentos_rojos', 0))
        self.lblFragAzules.text = str(r.get('fragmentos_azules', 0))

    def _seleccionar_producto(self, fila):
        if self._fila_seleccionada and self._fila_seleccionada != fila:
            self._fila_seleccionada.deseleccionar()
        if self._fila_seleccionada == fila:
            fila.deseleccionar()
            self._fila_seleccionada = None
            self._desactivar_boton_comprar()
            return
        fila.seleccionar()
        self._fila_seleccionada = fila
        self._activar_boton_comprar(fila.producto)

    def _activar_boton_comprar(self, producto):
        self.btnComprar.background_color    = (1, 1, 1, 1)
        self.lblPrecioSeleccionado.text     = str(producto['precio'])
        self.iconoDivisaSeleccionada.source = producto['icono_divisa']
        self.iconoDivisaSeleccionada.reload()

    def _desactivar_boton_comprar(self):
        self.btnComprar.background_color = (1, 1, 1, 0.5)
        self.lblPrecioSeleccionado.text  = ''

    def _deseleccionar_todo(self):
        for fila in self._filas:
            fila.deseleccionar()
        self._fila_seleccionada = None
        self._desactivar_boton_comprar()

    # ── Compra ────────────────────────────────────────────────────────────────

    def _confirmar_compra(self, instance):
        if self._fila_seleccionada is None:
            self._mostrar_resultado({"ok": False, "mensaje": "Selecciona un producto primero."})
            return
        producto = self._fila_seleccionada.producto

        modal = ModalView(size_hint=(0.8, 0.3), auto_dismiss=True, background_color=(0, 0, 0, 0))
        contenedor = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(12))
        with contenedor.canvas.before:
            Color(0.05, 0.05, 0.1, 0.97)
            RoundedRectangle(pos=contenedor.pos, size=contenedor.size, radius=[dp(16)])

        lbl = Label(
            text=f"¿Comprar {producto['nombre']} por {producto['precio']}?",
            font_size=dp(14), bold=True, color=BLANCO,
            size_hint=(1, 1), halign='center', valign='middle'
        )
        lbl.bind(size=lbl.setter('text_size'))

        filaBtns = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(44), spacing=dp(10))
        btnSi = BotonRedondeado(text='COMPRAR', bg_color=COLOR_GUARDIANES, text_color=(0, 0, 0, 1), radius=8, size_hint=(1, 1), font_size=dp(13), bold=True)
        btnNo = BotonRedondeado(text='CANCELAR', bg_color=(0.3, 0.1, 0.1, 1), text_color=BLANCO, radius=8, size_hint=(1, 1), font_size=dp(13))
        btnSi.bind(on_press=lambda _: self._ejecutar_compra(producto, modal))
        btnNo.bind(on_press=lambda _: modal.dismiss())
        filaBtns.add_widget(btnSi)
        filaBtns.add_widget(btnNo)
        contenedor.add_widget(lbl)
        contenedor.add_widget(filaBtns)
        modal.add_widget(contenedor)
        modal.open()

    def _ejecutar_compra(self, producto, modal):
        modal.dismiss()
        if self.gm is None:
            return
        pid = producto['id']
        if pid == 'pocion':
            resultado = self.gm.comprar_pocion()
        elif pid == 'ticket_personaje':
            resultado = self.gm.comprar_ticket_personaje(con_fragmentos=False)
        elif pid == 'ticket_arma':
            resultado = self.gm.comprar_ticket_arma(con_fragmentos=False)
        elif pid == 'transmutador':
            resultado = self.gm.comprar_transmutador()
        elif pid == 'ticket_personaje_frags':
            resultado = self.gm.comprar_ticket_personaje(con_fragmentos=True)
        elif pid == 'ticket_arma_frags':
            resultado = self.gm.comprar_ticket_arma(con_fragmentos=True)
        else:
            resultado = {"ok": False, "mensaje": "Producto desconocido."}
        self._mostrar_resultado(resultado)
        self._refrescar_recursos()
        self._deseleccionar_todo()

    def _mostrar_resultado(self, resultado):
        modal = ModalView(size_hint=(0.75, 0.25), auto_dismiss=True, background_color=(0, 0, 0, 0))
        contenedor = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        with contenedor.canvas.before:
            Color(0.05, 0.05, 0.1, 0.97)
            RoundedRectangle(pos=contenedor.pos, size=contenedor.size, radius=[dp(16)])
        color = (0.2, 0.8, 0.3, 1) if resultado['ok'] else (0.8, 0.2, 0.2, 1)
        lbl = Label(text=resultado['mensaje'], font_size=dp(13), color=color, size_hint=(1, 1), halign='center', valign='middle')
        lbl.bind(size=lbl.setter('text_size'))
        btn = BotonRedondeado(text='OK', bg_color=COLOR_GUARDIANES, text_color=(0, 0, 0, 1), radius=8, size_hint=(0.5, None), height=dp(40), pos_hint={'center_x': 0.5}, font_size=dp(13), bold=True)
        btn.bind(on_press=lambda _: modal.dismiss())
        contenedor.add_widget(lbl)
        contenedor.add_widget(btn)
        modal.add_widget(contenedor)
        modal.open()

    # ── Navegación ────────────────────────────────────────────────────────────

    def _navegar(self, pantalla):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = pantalla

    def _ir_al_gacha_o_home(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        if self.manager.get_screen('gacha'):
            self.manager.current = 'gacha'
        else:
            self.manager.current = 'principal'