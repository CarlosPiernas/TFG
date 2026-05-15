from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from widgets.responsive import sw, sh, sf, sdp
from kivy.animation import Animation
from kivy.uix.image import Image
from config import (
    COLOR_ANOMALIAS, COLOR_GUARDIANES, BLANCO, PANEL_MEDIO,
    NOMBRE_ANOMALIA, NOMBRE_GUARDIAN,
    FONDO_SELECCION, LOGO_GUARDIAN, LOGO_ANOMALIA
)
from widgets.componentes import BotonRedondeado


# Textos informativos de cada facción
INFO_GUARDIANES = (
    "Guardianes\n\n"
    "Los protecctores de su.\n"
    "realidad desde sus inicios.\n"
    "\n"
    "Tras las constantes amenazas\n"
    "del vacío, desarrollarón\n"
    "tecnologías ancestrales y\n"
    "pulierón el uso de la magia.\n"
    "\n"
    "Ahora el caos ha regresado\n"
    "para consumir su realidad y\n"
    "usarán todo para pararlo,\n"
    "aunque sea su final..\n\n"
    "Unete a los Guardianes y ¡resiste!\n"
)

INFO_ANOMALIAS = (
    "ANOMALÍAS\n\n"
    "Entidades del caos.\n"
    "Invasores de realidades.\n"
    "\n"
    "Desde el inicio de los tiempos\n"
    "consimieron toda posibilidad\n"
    "de vida en cualquier realidad\n"
    "emergente.\n"
    "\n"
    "Ahora el Heraldo del caos ha\n"
    "fijado sus esfuerzos en\n"
    "consumir una realidad..\n\n"
    "Unete al Vacío y ¡conquistala!\n"
)


class PantallaSeleccion(Screen):
    def __init__(self, gm=None, **kwargs):
        super().__init__(**kwargs)
        self.gm = gm
        self._info_visible = None  # 'guardian' | 'anomalia' | None

        # Fondo
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self._bg_rect = Rectangle(
                source=FONDO_SELECCION,
                pos=self.pos,
                size=self.size
            )
        self.bind(pos=self._upd_bg, size=self._upd_bg)

        self.layout = FloatLayout()

        # ── Botón izquierdo — Guardianes ─────────────────────────────────
        self.btn_guardianes = Button(
            text='',
            background_normal='',
            background_color=(0, 0, 0, 0),
            size_hint=(0.5, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        self.btn_guardianes.bind(on_press=self._pulsar_guardianes)

        # ── Botón derecho — Anomalías ─────────────────────────────────────
        self.btn_anomalias = Button(
            text='',
            background_normal='',
            background_color=(0, 0, 0, 0),
            size_hint=(0.5, 1),
            pos_hint={'right': 1, 'y': 0}
        )
        self.btn_anomalias.bind(on_press=self._pulsar_anomalias)

        # ── Panel de info (oculto inicialmente) ───────────────────────────
        self.panel_info = FloatLayout(
            size_hint=(0.5, 1),
            pos_hint={'center_x': 0.75, 'top': 1},
            opacity=0
        )

        # Degradado negro apilado
        self.degradado = FloatLayout(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        capas = [0.82, 0.75, 0.68, 0.60, 0.52, 0.44, 0.36, 0.28, 0.20, 0.13, 0.07, 0.03, 0.01, 0.0]
        altura_capa = 1.0 / len(capas)
        for i, alpha in enumerate(capas):
            from kivy.uix.widget import Widget as W
            capa = W(
                size_hint=(1, altura_capa),
                pos_hint={'x': 0, 'top': 1.0 - i * altura_capa}
            )
            with capa.canvas:
                Color(0, 0, 0, alpha)
                self._capa_rect = Rectangle(pos=capa.pos, size=capa.size)
                def _bind(c):
                    with c.canvas:
                        col = Color(0, 0, 0, 0)
                    c.bind(
                        pos=lambda inst, val: setattr(inst.canvas.children[-2], 'pos', val),
                        size=lambda inst, val: setattr(inst.canvas.children[-2], 'size', val)
                    )
                _bind(capa)
            self.degradado.add_widget(capa)

        # Texto del lore — en el tercio superior
        self.label_info = Label(
            text='',
            font_size=dp(13),
            color=BLANCO,
            halign='center',
            valign='top',
            size_hint=(0.9, 0.45),
            pos_hint={'center_x': 0.5, 'top': 0.95},
            markup=True
        )
        self.label_info.bind(size=self.label_info.setter('text_size'))

        # FIX nº4: logo bajado de 'top': 0.55 a 'top': 0.38
        self.logo_faccion = Image(
            source='',
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(0.6, 0.22),
            pos_hint={'center_x': 0.5, 'top': 0.38}
        )

        self.panel_info.add_widget(self.degradado)
        self.panel_info.add_widget(self.label_info)
        self.panel_info.add_widget(self.logo_faccion)
        # ── Overlay oscuro izquierdo (se activa al pulsar Anomalías) ─────────
        self.overlay_izq = Widget(
            size_hint=(0.5, 1),
            pos_hint={'x': 0, 'y': 0},
            opacity=0
        )
        with self.overlay_izq.canvas:
            Color(0, 0, 0, 0.55)
            self._ovl_izq_rect = Rectangle(
                pos=self.overlay_izq.pos,
                size=self.overlay_izq.size
            )
        self.overlay_izq.bind(
            pos=lambda *a: setattr(self._ovl_izq_rect, 'pos', self.overlay_izq.pos),
            size=lambda *a: setattr(self._ovl_izq_rect, 'size', self.overlay_izq.size)
        )

        # ── Overlay oscuro derecho (se activa al pulsar Guardianes) ──────────
        self.overlay_der = Widget(
            size_hint=(0.5, 1),
            pos_hint={'right': 1, 'y': 0},
            opacity=0
        )
        with self.overlay_der.canvas:
            Color(0, 0, 0, 0.55)
            self._ovl_der_rect = Rectangle(
                pos=self.overlay_der.pos,
                size=self.overlay_der.size
            )
        self.overlay_der.bind(
            pos=lambda *a: setattr(self._ovl_der_rect, 'pos', self.overlay_der.pos),
            size=lambda *a: setattr(self._ovl_der_rect, 'size', self.overlay_der.size)
        )

        self.label_info = Label(
            text='',
            font_size=dp(13),
            color=BLANCO,
            halign='center',
            valign='top',
            size_hint=(0.9, 0.35),
            pos_hint={'center_x': 0.5, 'top': 0.92},
            markup=True
        )
        self.label_info.bind(size=self.label_info.setter('text_size'))
        self.panel_info.add_widget(self.label_info)

        self.layout.add_widget(self.btn_guardianes)
        self.layout.add_widget(self.btn_anomalias)
        self.layout.add_widget(self.overlay_izq)
        self.layout.add_widget(self.overlay_der)
        self.layout.add_widget(self.panel_info)
        self.add_widget(self.layout)

    # ── Fondo ─────────────────────────────────────────────────────────────────

    def _upd_bg(self, *args):
        self._bg_rect.pos  = self.pos
        self._bg_rect.size = self.size

    # ── Lógica de pulsación ───────────────────────────────────────────────────

    def _pulsar_guardianes(self, *args):
        if self._info_visible == 'guardian':
            self._mostrar_popup('guardian')
        else:
            self._mostrar_info(INFO_GUARDIANES, COLOR_GUARDIANES, 'guardian')

    def _pulsar_anomalias(self, *args):
        if self._info_visible == 'anomalia':
            self._mostrar_popup('anomalia')
        else:
            self._mostrar_info(INFO_ANOMALIAS, COLOR_ANOMALIAS, 'anomalia')

    def _mostrar_info(self, texto, color, faccion):
        self._info_visible = faccion
        self.label_info.text  = texto
        self.label_info.color = color
        self.logo_faccion.source = LOGO_GUARDIAN if faccion == 'guardian' else LOGO_ANOMALIA
        self.logo_faccion.reload()

        if faccion == 'guardian':
            self.panel_info.pos_hint = {'center_x': 0.75, 'top': 1}
            Animation(opacity=1, duration=0.3, t='in_out_quad').start(self.overlay_der)
            Animation(opacity=0, duration=0.3, t='in_out_quad').start(self.overlay_izq)
        else:
            self.panel_info.pos_hint = {'center_x': 0.25, 'top': 1}
            Animation(opacity=1, duration=0.3, t='in_out_quad').start(self.overlay_izq)
            Animation(opacity=0, duration=0.3, t='in_out_quad').start(self.overlay_der)

        Animation.cancel_all(self.panel_info)
        Animation(opacity=1, duration=0.3, t='in_out_quad').start(self.panel_info)

    def _mostrar_popup(self, faccion):
        nombre = NOMBRE_GUARDIAN if faccion == 'guardian' else NOMBRE_ANOMALIA
        color  = COLOR_GUARDIANES if faccion == 'guardian' else COLOR_ANOMALIAS
        sprite = None

        contenido = BoxLayout(orientation='vertical', spacing=dp(12), padding=dp(16))

        contenido.add_widget(Label(
            text=f'¿Quieres unirte a\n{nombre}?',
            font_size=sf(15),
            bold=True,
            color=color,
            halign='center',
            size_hint=(1, None),
            height=sh(60)
        ))

        fila_botones = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=sh(44),
            spacing=dp(10)
        )

        btn_si = BotonRedondeado(
            text='SÍ, UNIRME',
            bg_color=color,
            text_color=BLANCO,
            radius=8,
            size_hint=(0.5, 1),
            font_size=sf(13),
            bold=True
        )

        btn_no = BotonRedondeado(
            text='VOLVER',
            bg_color=PANEL_MEDIO,
            text_color=BLANCO,
            radius=8,
            size_hint=(0.5, 1),
            font_size=sf(13)
        )

        fila_botones.add_widget(btn_si)
        fila_botones.add_widget(btn_no)
        contenido.add_widget(fila_botones)

        popup = Popup(
            title='',
            content=contenido,
            size_hint=(0.78, None),
            height=sh(180),
            background='',
            background_color=(0.08, 0.08, 0.15, 0.97),
            separator_height=0
        )

        btn_si.bind(on_press=lambda _: self._confirmar(faccion, sprite, color, popup))
        btn_no.bind(on_press=lambda _: self._cerrar_popup(popup))

        popup.open()

    def _cerrar_popup(self, popup):
        popup.dismiss()
        Animation(opacity=0, duration=0.2).start(self.panel_info)
        Animation(opacity=0, duration=0.2).start(self.overlay_izq)
        Animation(opacity=0, duration=0.2).start(self.overlay_der)
        self._info_visible = None

    def _confirmar(self, faccion, sprite, color, popup):
        popup.dismiss()
        nombre = NOMBRE_GUARDIAN if faccion == 'guardian' else NOMBRE_ANOMALIA
        if self.gm is not None:
            self.gm.iniciar_juego(nombre)
        pantallaHome = self.manager.get_screen('principal')
        pantallaHome.cargarPersonaje(nombre, sprite, color)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'principal'

    # ── Salto automático si ya hay facción guardada ───────────────────────────

    def on_pre_enter(self, *args):
        if self.gm is not None and self.gm.faccion is not None:
            from kivy.clock import Clock
            Clock.schedule_once(self._navegar_a_home, 0)

    def _navegar_a_home(self, dt):
        faccion = self.gm.faccion
        sprite  = None
        nombre  = NOMBRE_GUARDIAN  if faccion != 'anomalia' else NOMBRE_ANOMALIA
        color   = COLOR_GUARDIANES if faccion != 'anomalia' else COLOR_ANOMALIAS
        pantallaHome = self.manager.get_screen('principal')
        pantallaHome.cargarPersonaje(nombre, sprite, color)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'principal'

    def actualizarFondo(self, *args):
        self._bg_rect.pos  = self.pos
        self._bg_rect.size = self.size