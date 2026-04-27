# =============================================================================
# screens/gacha_screen.py
# =============================================================================

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.metrics import dp

from widgets.componentes import PanelRedondeado, BotonRedondeado
from config import (
    PANEL_OSCURO, PANEL_MEDIO, COLOR_GUARDIANES,
    BLANCO, FONDO_PRINCIPAL, NOMBRE_ANOMALIA, FONDO_GACHA
)

# Color por rareza para el popup
COLOR_RAREZA = {
    'S': (1.0, 0.75, 0.0, 1),   # dorado
    'A': (0.6, 0.2,  1.0, 1),   # púrpura
    'B': (0.4, 0.7,  1.0, 1),   # azul
}


class PantallaGacha(Screen):
    def __init__(self, gm=None, **kwargs):
        super().__init__(**kwargs)
        self.gm             = gm
        self.banner_actual  = 'personajes'  # banner seleccionado actualmente

        self.layout_principal = FloatLayout()

        # 1. FONDO
        self.layout_principal.add_widget(Image(
            source=FONDO_GACHA,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        ))

        # 2. RECURSOS — tickets arriba a la derecha
        self.label_tickets = Label(
            text='Tickets: —',
            font_size='18sp',
            size_hint=(None, None),
            size=(dp(160), dp(50)),
            pos_hint={'right': 0.95, 'top': 0.98}
        )
        self.layout_principal.add_widget(self.label_tickets)

        # 3. SELECTOR DE BANNERS
        self.selector = BoxLayout(
            orientation='horizontal',
            size_hint=(0.9, 0.07),
            pos_hint={'center_x': 0.5, 'top': 0.90},
            spacing=dp(10)
        )
        self.btn_heroes = BotonRedondeado(
            text='PERSONAJES',
            bg_color=PANEL_MEDIO,
            on_release=lambda x: self.cambiar_banner('personajes')
        )
        self.btn_armas = BotonRedondeado(
            text='ARMAS',
            bg_color=PANEL_OSCURO,
            on_release=lambda x: self.cambiar_banner('armas')
        )
        self.selector.add_widget(self.btn_heroes)
        self.selector.add_widget(self.btn_armas)
        self.layout_principal.add_widget(self.selector)

        # 4. ARTE DEL BANNER
        self.banner_visual = Image(
            source='assets/logos/Logo_Anomalias.png',
            size_hint=(0.9, 0.40),
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            allow_stretch=True
        )
        self.layout_principal.add_widget(self.banner_visual)

        # 5. CONTADOR DE PITY
        self.pity_container = FloatLayout(
            size_hint=(0.8, 0.06),
            pos_hint={'center_x': 0.5, 'y': 0.30}
        )
        self.pity_container.add_widget(PanelRedondeado(bg_color=PANEL_OSCURO, radius=15))
        self.label_pity = Label(
            text='Próximo [b]Grado S[/b] en: [color=#ffbf00]—[/color]',
            markup=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.pity_container.add_widget(self.label_pity)
        self.layout_principal.add_widget(self.pity_container)

        # 6. BOTON INVOCAR
        self.btn_invocar = BotonRedondeado(
            text='INVOCAR x1',
            size_hint=(0.7, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.15},
            bg_color=COLOR_GUARDIANES,
            text_color=FONDO_PRINCIPAL,
            radius=20,
            on_release=self.ejecutar_tirada
        )
        self.layout_principal.add_widget(self.btn_invocar)

        # 7. BOTON VOLVER
        self.btn_volver = BotonRedondeado(
            text='MENU',
            size_hint=(0.7, 0.07),
            pos_hint={'center_x': 0.5, 'y': 0.05},
            bg_color=PANEL_OSCURO,
            on_release=self.ir_al_home
        )
        self.layout_principal.add_widget(self.btn_volver)

        self.add_widget(self.layout_principal)

    def on_pre_enter(self, *args):
        # Nombre del banner de personajes según facción
        if self.gm and self.gm.faccion:
            if self.gm.faccion == 'anomalia':
                self.btn_heroes.text = 'ANOMALÍAS'
            else:
                self.btn_heroes.text = 'GUARDIANES'

        # Actualizar tickets y pity
        self._refrescar_recursos()
        self._refrescar_pity()

    # ── Helpers de refresco ──────────────────────────────────

    def _refrescar_recursos(self):
        if self.gm is None:
            return
        recursos = self.gm.get_recursos()
        if self.banner_actual == 'personajes':
            tickets = recursos.get('tickets_personaje', 0)
        else:
            tickets = recursos.get('tickets_arma', 0)
        self.label_tickets.text = f'Tickets: {tickets}'

    def _refrescar_pity(self):
        if self.gm is None:
            return
        from database.repositories import pity_repo
        from database.config import GACHA_MODE
        resultado = pity_repo.get_pity(1, self.banner_actual)
        contador = resultado["pity_count"] if resultado else 0
        limite = 5 if GACHA_MODE == 'simple' else 90
        faltan = max(0, limite - contador)
        self.label_pity.text = (
            f'Próximo [b]Grado S[/b] en: [color=#ffbf00]{faltan}[/color]'
        )
        print(f"[DEBUG pity] contador={contador}, limite={limite}, faltan={faltan}")

    # ── Navegación y banners ─────────────────────────────────

    def cambiar_banner(self, tipo):
        self.banner_actual = tipo
        if tipo == 'personajes':
            self.btn_heroes.bg_color = PANEL_MEDIO
            self.btn_armas.bg_color  = PANEL_OSCURO
        else:
            self.btn_heroes.bg_color = PANEL_OSCURO
            self.btn_armas.bg_color  = PANEL_MEDIO
        self._refrescar_recursos()
        self._refrescar_pity()

    def ir_al_home(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'principal'

    # ── Tirada ───────────────────────────────────────────────

    def ejecutar_tirada(self, instance):
        if self.gm is None:
            return

        resultado = self.gm.tirar_gacha(self.banner_actual)

        if 'error' in resultado:
            self._mostrar_popup('Error', resultado['error'], (0.7, 0.1, 0.1, 1))
            return

        nombre  = resultado.get('nombre', '?')
        rareza  = resultado.get('rareza', 'B')
        tipo    = resultado.get('tipo', '')
        es_frag = resultado.get('fragmento', False)

        if es_frag:
            titulo  = f'✦ FRAGMENTO {rareza} ✦'
            cuerpo  = f'{nombre}\n\n(Ya lo tenías — recibes fragmento)'
        else:
            titulo  = f'✦ {rareza} ✦'
            cuerpo  = nombre

        color = COLOR_RAREZA.get(rareza, BLANCO)
        self._mostrar_popup(titulo, cuerpo, color)

        # Refrescar tickets y pity tras la tirada
        self._refrescar_recursos()
        self._refrescar_pity()

    def _mostrar_popup(self, titulo, cuerpo, color_titulo):
        modal = ModalView(
            size_hint=(0.8, 0.45),
            auto_dismiss=True,
            background_color=(0, 0, 0, 0)
        )

        contenedor = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(12)
        )
        with contenedor.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(0.05, 0.05, 0.1, 0.97)
            RoundedRectangle(pos=contenedor.pos, size=contenedor.size, radius=[dp(16)])
        contenedor.bind(
            pos=lambda *a: None,  # el canvas se redibuja solo al moverse
            size=lambda *a: None
        )

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

        lbl_cuerpo = Label(
            text=cuerpo,
            font_size=dp(16),
            color=BLANCO,
            size_hint=(1, 1),
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
        contenedor.add_widget(lbl_cuerpo)
        contenedor.add_widget(btn_cerrar)
        modal.add_widget(contenedor)
        modal.open()