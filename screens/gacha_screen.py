from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp
from kivy.clock import Clock
import os

from widgets.componentes import BotonRedondeado
from config import (
    PANEL_OSCURO, PANEL_MEDIO, COLOR_GUARDIANES, BLANCO, FONDO_PRINCIPAL,
    NOMBRE_ANOMALIA,
    FONDO_GACHA_ARMAS, FONDO_GACHA_ANOMALIA, FONDO_GACHA_GUARDIANES,
    TITULO_GACHA, TITULO_PERSONAJES, TITULO_ARMAS,
    BOTON_INVOCAR, BOTON_FORJAR, BOTON_TIENDA, BOTON_VOLVER,
    TICKET_PERSONAJES, TICKET_ARMAS,
    icono_arma, nombre_arma,
    icono_personaje, nombre_personaje,
)

COLOR_RAREZA = {
    'S': (1.0, 0.75, 0.0, 1),
    'A': (0.6, 0.2,  1.0, 1),
    'B': (0.4, 0.7,  1.0, 1),
}


class PantallaGacha(Screen):
    def __init__(self, gm=None, **kwargs):
        super().__init__(**kwargs)
        self.gm            = gm
        self.banner_actual = 'personajes'

        raiz = FloatLayout()

        # ── FONDO ─────────────────────────────────────────────────────────────
        self.fondo = Image(
            source=FONDO_GACHA_ANOMALIA,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0},
            mipmap=True
        )
        raiz.add_widget(self.fondo)

        self._frames_armas = sorted(
            [f'assets/fondos/fondo_gacha_armas/{f}'
             for f in os.listdir('assets/fondos/fondo_gacha_armas')
             if f.endswith('.png')],
            key=lambda x: int(x.split('_')[-1].replace('.png', ''))
        )
        self._frames_personajes = sorted(
            [f'assets/fondos/fondo_gacha_anomalia/{f}'
             for f in os.listdir('assets/fondos/fondo_gacha_anomalia')
             if f.endswith('.png')],
            key=lambda x: int(x.split('_')[-1].replace('.png', ''))
        )
        self._frames_guardianes = sorted(
            [f'assets/fondos/fondo_gacha_guardianes/{f}'
             for f in os.listdir('assets/fondos/fondo_gacha_guardianes')
             if f.endswith('.png')],
            key=lambda x: int(x.split('_')[-1].replace('.png', ''))
        )
        self._frame_actual      = 0
        self._anim_event        = None

        # ── TÍTULO GACHAPÓN ───────────────────────────────────────────────────
        raiz.add_widget(Image(
            source=TITULO_GACHA,
            size_hint=(0.95, 0.18),
            pos_hint={'center_x': 0.5, 'top': 1.0},
            allow_stretch=True,
            keep_ratio=True,
            mipmap=True
        ))

        # ── FONDO OSCURO TABS + TICKETS ───────────────────────────────────────
        fondoTabs = BoxLayout(
            size_hint=(1, 0.16),
            pos_hint={'x': 0, 'top': 0.84}
        )
        with fondoTabs.canvas.before:
            Color(0, 0, 0, 0.55)
            self._bgTabs = Rectangle(
                pos=fondoTabs.pos,
                size=fondoTabs.size
            )
        fondoTabs.bind(
            pos=lambda *a: setattr(self._bgTabs, 'pos', fondoTabs.pos),
            size=lambda *a: setattr(self._bgTabs, 'size', fondoTabs.size)
        )
        raiz.add_widget(fondoTabs)

        # ── TABS BANNERS ──────────────────────────────────────────────────────
        tabs = BoxLayout(
            orientation='horizontal',
            size_hint=(0.9, 0.10),
            pos_hint={'center_x': 0.5, 'top': 0.84},
            spacing=dp(8)
        )

        self.btn_personajes = Button(
            background_normal=TITULO_PERSONAJES,
            background_down=TITULO_PERSONAJES,
            background_color=(1, 1, 1, 1),
            border=(0, 0, 0, 0),
            size_hint=(1, 1),
            mipmap=True
        )
        self.btn_personajes.bind(on_press=lambda _: self.cambiar_banner('personajes'))

        self.btn_armas_tab = Button(
            background_normal=TITULO_ARMAS,
            background_down=TITULO_ARMAS,
            background_color=(1, 1, 1, 0.5),
            border=(0, 0, 0, 0),
            size_hint=(1, 1),
            mipmap=True
        )
        self.btn_armas_tab.bind(on_press=lambda _: self.cambiar_banner('armas'))

        tabs.add_widget(self.btn_personajes)
        tabs.add_widget(self.btn_armas_tab)
        raiz.add_widget(tabs)

        # ── FILA TICKETS — ancho completo con fondo oscuro ────────────────────
        filaTickets = BoxLayout(
            orientation='horizontal',
            size_hint=(0.9, 0.06),
            pos_hint={'center_x': 0.5, 'top': 0.75},
            spacing=dp(0),
            padding=[dp(10), dp(4)]
        )

        # Lado personajes
        ladoPersonajes = BoxLayout(orientation='horizontal', size_hint=(0.5, 1), spacing=dp(4))
        self.iconoTicketPersonajes = Image(
            source=TICKET_PERSONAJES,
            size_hint=(None, None),
            size=(dp(28), dp(28)),
            allow_stretch=True,
            keep_ratio=True,
            mipmap=True,
            pos_hint={'center_y': 0.5}
        )
        self.lblTicketsPersonajes = Label(
            text='0',
            font_size=dp(13),
            bold=True,
            color=COLOR_GUARDIANES,
            size_hint=(1, 1),
            halign='left',
            valign='middle'
        )
        self.lblTicketsPersonajes.bind(size=self.lblTicketsPersonajes.setter('text_size'))
        ladoPersonajes.add_widget(self.iconoTicketPersonajes)
        ladoPersonajes.add_widget(self.lblTicketsPersonajes)

        # Separador vertical
        separador = BoxLayout(size_hint=(None, 1), width=dp(1))
        with separador.canvas:
            Color(1, 1, 1, 0.3)
            Rectangle(pos=separador.pos, size=separador.size)
        separador.bind(
            pos=lambda *a: None,
            size=lambda *a: None
        )

        # Lado armas
        ladoArmas = BoxLayout(orientation='horizontal', size_hint=(0.5, 1), spacing=dp(4),
                              padding=[dp(8), 0])
        self.iconoTicketArmas = Image(
            source=TICKET_ARMAS,
            size_hint=(None, None),
            size=(dp(28), dp(28)),
            allow_stretch=True,
            keep_ratio=True,
            mipmap=True,
            pos_hint={'center_y': 0.5}
        )
        self.lblTicketsArmas = Label(
            text='0',
            font_size=dp(13),
            bold=True,
            color=COLOR_GUARDIANES,
            size_hint=(1, 1),
            halign='left',
            valign='middle'
        )
        self.lblTicketsArmas.bind(size=self.lblTicketsArmas.setter('text_size'))
        ladoArmas.add_widget(self.iconoTicketArmas)
        ladoArmas.add_widget(self.lblTicketsArmas)

        filaTickets.add_widget(ladoPersonajes)
        filaTickets.add_widget(separador)
        filaTickets.add_widget(ladoArmas)
        raiz.add_widget(filaTickets)

        # ── PITY ──────────────────────────────────────────────────────────────
        self.lblPity = Label(
            text='Próximo [b]S[/b] en: [color=#ffbf00]—[/color]',
            markup=True,
            font_size=dp(12),
            color=BLANCO,
            size_hint=(0.6, 0.05),
            pos_hint={'center_x': 0.5, 'y': 0.30},
            halign='center',
            valign='middle'
        )
        self.lblPity.bind(size=self.lblPity.setter('text_size'))
        raiz.add_widget(self.lblPity)

        # ── BOTÓN INVOCAR/FORJAR ──────────────────────────────────────────────
        self.btnAccion = Button(
            background_normal=BOTON_INVOCAR,
            background_down=BOTON_INVOCAR,
            background_color=(1, 1, 1, 1),
            border=(0, 0, 0, 0),
            size_hint=(0.65, 0.11),
            pos_hint={'center_x': 0.5, 'y': 0.17},
            mipmap=True
        )
        self.btnAccion.bind(on_press=self.ejecutar_tirada)
        raiz.add_widget(self.btnAccion)

        # ── FILA TIENDA + VOLVER ──────────────────────────────────────────────
        filaBotones = BoxLayout(
            orientation='horizontal',
            size_hint=(0.85, 0.11),
            pos_hint={'center_x': 0.5, 'y': 0.04},
            spacing=dp(10)
        )

        btnTienda = Button(
            background_normal=BOTON_TIENDA,
            background_down=BOTON_TIENDA,
            background_color=(1, 1, 1, 1),
            border=(0, 0, 0, 0),
            size_hint=(1, 1),
            mipmap=True
        )
        btnTienda.bind(on_press=lambda _: self.navegarA('tienda'))

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
        btnVolver.bind(on_press=self.ir_al_home)

        filaBotones.add_widget(btnTienda)
        filaBotones.add_widget(btnVolver)
        raiz.add_widget(filaBotones)

        self.add_widget(raiz)

    def _iniciar_animacion(self):
        if self._anim_event:
            self._anim_event.cancel()
        self._frame_actual = 0
        self._anim_event = Clock.schedule_interval(self._siguiente_frame, 1/12)

    def _siguiente_frame(self, dt):
        if self.banner_actual == 'armas':
            frames = self._frames_armas
        elif self.gm and self.gm.faccion == 'anomalia':
            frames = self._frames_personajes
        else:
            frames = self._frames_guardianes

        if not frames:
            return
        self._frame_actual = (self._frame_actual + 1) % len(frames)
        self.fondo.source = frames[self._frame_actual]

    # ── Ciclo de vida ─────────────────────────────────────────────────────────

    def on_pre_enter(self, *args):
        self._refrescar_fondo()
        self._refrescar_recursos()
        self._refrescar_pity()
        self._precargar_frames()
        self._iniciar_animacion()

    def _precargar_frames(self):
        import threading
        from kivy.core.image import Image as CoreImage

        def cargar():
            for lista in [self._frames_armas, self._frames_personajes, self._frames_guardianes]:
                for path in lista:
                    try:
                        CoreImage(path, mipmap=True)
                    except Exception:
                        pass

        threading.Thread(target=cargar, daemon=True).start()

    def on_leave(self, *args):
        if self._anim_event:
            self._anim_event.cancel()
            self._anim_event = None

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _refrescar_fondo(self):
        if self.gm is None:
            return
        if self.banner_actual == 'armas':
            self.fondo.source = FONDO_GACHA_ARMAS
        elif self.gm.faccion == 'anomalia':
            self.fondo.source = FONDO_GACHA_ANOMALIA
        else:
            self.fondo.source = FONDO_GACHA_GUARDIANES
        self.fondo.reload()

    def _refrescar_recursos(self):
        if self.gm is None:
            return
        recursos = self.gm.get_recursos()
        self.lblTicketsPersonajes.text = str(recursos.get('tickets_personaje', 0))
        self.lblTicketsArmas.text      = str(recursos.get('tickets_arma', 0))

    def _refrescar_pity(self):
        if self.gm is None:
            return
        from database.repositories import pity_repo
        from database.config import GACHA_MODE
        resultado = pity_repo.get_pity(1, self.banner_actual)
        contador  = resultado['pity_count'] if resultado else 0
        limite    = 5 if GACHA_MODE == 'simple' else 90
        faltan    = max(0, limite - contador)
        self.lblPity.text = (
            f'Próximo [b]S[/b] en: [color=#ffbf00]{faltan}[/color]'
        )

    # ── Banners ───────────────────────────────────────────────────────────────

    def cambiar_banner(self, tipo):
        self.banner_actual = tipo
        if tipo == 'personajes':
            self.btn_personajes.background_color = (1, 1, 1, 1)
            self.btn_armas_tab.background_color  = (1, 1, 1, 0.4)
            self.btnAccion.background_normal     = BOTON_INVOCAR
            self.btnAccion.background_down       = BOTON_INVOCAR
        else:
            self.btn_personajes.background_color = (1, 1, 1, 0.4)
            self.btn_armas_tab.background_color  = (1, 1, 1, 1)
            self.btnAccion.background_normal     = BOTON_FORJAR
            self.btnAccion.background_down       = BOTON_FORJAR
        self._refrescar_fondo()
        self._refrescar_recursos()
        self._refrescar_pity()

    # ── Navegación ────────────────────────────────────────────────────────────

    def navegarA(self, pantalla):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = pantalla

    def ir_al_home(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'principal'

    # ── Tirada ────────────────────────────────────────────────────────────────

    def ejecutar_tirada(self, instance):
        if self.gm is None:
            return
        resultado = self.gm.tirar_gacha(self.banner_actual)
        if 'error' in resultado:
            self._mostrar_popup('Error', resultado['error'], (0.7, 0.1, 0.1, 1))
            return

        # El nombre viene anidado en resultado["item"]["nombre"], no en el nivel superior.
        item      = resultado.get('item') or {}
        nombre_db = item.get('nombre', '?')
        rareza    = resultado.get('rareza') or item.get('rareza', 'B')
        es_frag   = resultado.get('fragmento') is not None

        # Resuelve icono y nombre legible según el banner.
        # Tanto si es nuevo como si es fragmento, mostramos el icono del item.
        if self.banner_actual == 'armas':
            icono_path     = icono_arma(nombre_db)
            nombre_display = nombre_arma(nombre_db)
            tipo_label     = 'arma'
        else:
            icono_path     = icono_personaje(nombre_db)
            nombre_display = nombre_personaje(nombre_db)
            tipo_label     = 'personaje'

        if es_frag:
            titulo = f'¡Fragmento {rareza}!'
            cuerpo = (
                f'Has recibido un fragmento de [b]{nombre_display}[/b]\n'
                f'porque ya tenías este {tipo_label}.'
            )
        else:
            titulo = f'¡{rareza}!'
            cuerpo = nombre_display

        self._mostrar_popup(
            titulo,
            cuerpo,
            COLOR_RAREZA.get(rareza, BLANCO),
            icono_path=icono_path,
        )
        self._refrescar_recursos()
        self._refrescar_pity()

    def _mostrar_popup(self, titulo, cuerpo, color_titulo, icono_path=None):
        modal = ModalView(
            size_hint=(0.8, 0.6 if icono_path else 0.45),
            auto_dismiss=True,
            background_color=(0, 0, 0, 0)
        )
        contenedor = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(12)
        )
        with contenedor.canvas.before:
            Color(0.05, 0.05, 0.1, 0.97)
            RoundedRectangle(pos=contenedor.pos, size=contenedor.size, radius=[dp(16)])

        lbl_titulo = Label(
            text=titulo,
            font_size=dp(22),
            bold=True,
            color=color_titulo,
            size_hint=(1, None),
            height=dp(40),
            halign='center',
            valign='middle'
        )
        lbl_titulo.bind(size=lbl_titulo.setter('text_size'))

        # Icono opcional (personajes o armas, tanto en nuevo como en fragmento)
        icono_widget = None
        if icono_path:
            icono_widget = Image(
                source=icono_path,
                allow_stretch=True,
                keep_ratio=True,
                mipmap=True,
                size_hint=(1, 1),
            )

        lbl_cuerpo = Label(
            text=cuerpo,
            font_size=dp(16),
            color=BLANCO,
            markup=True,
            size_hint=(1, None if icono_path else 1),
            height=dp(60) if icono_path else 0,
            halign='center',
            valign='middle'
        )
        lbl_cuerpo.bind(size=lbl_cuerpo.setter('text_size'))

        btn_cerrar = BotonRedondeado(
            text='CONTINUAR',
            bg_color=COLOR_GUARDIANES,
            text_color=FONDO_PRINCIPAL,
            radius=10,
            size_hint=(1, None),
            height=dp(44),
            font_size=dp(13),
            bold=True
        )
        btn_cerrar.bind(on_press=lambda _: modal.dismiss())

        contenedor.add_widget(lbl_titulo)
        if icono_widget is not None:
            contenedor.add_widget(icono_widget)
        contenedor.add_widget(lbl_cuerpo)
        contenedor.add_widget(btn_cerrar)
        modal.add_widget(contenedor)
        modal.open()