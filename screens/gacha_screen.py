# =============================================================================
# screens/gacha_screen.py
# Pantalla de gacha — Sprint 2
# Dos banners (personajes y armas), tirada x1 y animacion de resultado.
# =============================================================================

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.app import App

from widgets.componentes import PanelRedondeado, BotonRedondeado
from config import (
    PANEL_OSCURO, PANEL_MEDIO, COLOR_GUARDIANES,
    BLANCO, FONDO_PRINCIPAL, NOMBRE_ANOMALIA, FONDO_GACHA
)


class PantallaGacha(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout_principal = FloatLayout()

        # 1. FONDO — imagen por debajo de todos los elementos
        self.layout_principal.add_widget(Image(
            source=FONDO_GACHA,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        ))

        # 2. RECURSOS — tickets arriba a la derecha
        self.label_tickets = Label(
            text="Tickets: 10 [color=#ffbf00]♦[/color]",
            markup=True,
            font_size='18sp',
            size_hint=(None, None),
            size=(dp(150), dp(50)),
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

        # El nombre cambia segun la faccion en on_pre_enter
        self.btn_heroes = BotonRedondeado(
            text="HEROES",
            bg_color=PANEL_MEDIO,
            on_release=lambda x: self.cambiar_banner("personajes")
        )
        self.btn_armas = BotonRedondeado(
            text="ARMAS",
            bg_color=PANEL_OSCURO,
            on_release=lambda x: self.cambiar_banner("armas")
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
            text="Proximo [b]Grado S[/b] en: [color=#ffbf00]5[/color]",
            markup=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.pity_container.add_widget(self.label_pity)
        self.layout_principal.add_widget(self.pity_container)

        # 6. BOTON INVOCAR
        self.btn_invocar = BotonRedondeado(
            text="INVOCAR x1",
            size_hint=(0.7, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.15},
            bg_color=COLOR_GUARDIANES,
            text_color=FONDO_PRINCIPAL,
            radius=20,
            on_release=self.ejecutar_tirada
        )
        self.layout_principal.add_widget(self.btn_invocar)

        # 7. BOTON VOLVER AL MENU
        self.btn_volver = BotonRedondeado(
            text="MENU",
            size_hint=(0.7, 0.07),
            pos_hint={'center_x': 0.5, 'y': 0.05},
            bg_color=PANEL_OSCURO,
            on_release=self.ir_al_home
        )
        self.layout_principal.add_widget(self.btn_volver)

        self.add_widget(self.layout_principal)

    def on_pre_enter(self):
        # Ajusta el texto del banner segun la faccion elegida en Sprint 1
        app = App.get_running_app()
        if hasattr(app, 'faccion_elegida'):
            if app.faccion_elegida == NOMBRE_ANOMALIA:
                self.btn_heroes.text = "ANOMALIAS"
            else:
                self.btn_heroes.text = "HEROES"

    def ir_al_home(self, instance):
        self.manager.current = 'principal'

    def cambiar_banner(self, tipo):
        # Resalta visualmente el banner seleccionado
        if tipo == "personajes":
            self.btn_heroes.bg_color = PANEL_MEDIO
            self.btn_armas.bg_color  = PANEL_OSCURO
        else:
            self.btn_heroes.bg_color = PANEL_OSCURO
            self.btn_armas.bg_color  = PANEL_MEDIO

    def ejecutar_tirada(self, instance):
        # TODO: conectar con la logica de M2 para el Sprint 2
        print(f"M3: Iniciando animacion de gacha para {self.btn_heroes.text}...")