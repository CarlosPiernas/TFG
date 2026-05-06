from kivy.uix.screenmanager import Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.core.image import Image as CoreImage
from widgets.responsive import sw, sh, sf, sdp
import os


class PantallaSplash(Screen):
    def __init__(self, gm=None, **kwargs):
        super().__init__(**kwargs)
        self.gm = gm
        self._touch_ready = False
        self._carga_completa = False
        self._auto_event = None

        # Lista de assets a precargar — se llena en on_enter
        self._assets_pendientes = []
        self._assets_total = 0
        self._assets_cargados = 0

        # Fondo negro puro
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._upd_bg, size=self._upd_bg)

        self.layout = FloatLayout()

        # Logo del juego centrado en la parte superior
        self.logo = Image(
            source='assets/logos/Logo_Juego.png',
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(0.7, 0.35),
            pos_hint={'center_x': 0.5, 'top': 0.88},
            opacity=0
        )

        # Subtítulo
        self.subtitulo = Label(
            text='ANOMALÍAS vs GUARDIANES\nDEL ESPACIO TIEMPO',
            font_size=sf(14),
            bold=True,
            color=(0.85, 0.75, 1, 1),
            halign='center',
            valign='middle',
            size_hint=(1, None),
            height=sh(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.47},
            opacity=0
        )
        self.subtitulo.bind(size=self.subtitulo.setter('text_size'))

        # ── Barra de progreso ────────────────────────────────────────────
        self.contenedorBarra = FloatLayout(
            size_hint=(0.7, None),
            height=sh(28),
            pos_hint={'center_x': 0.5, 'center_y': 0.20},
            opacity=0
        )
        self.contenedorBarra.bind(pos=self._dibujar_barra, size=self._dibujar_barra)
        self._progreso = 0.0

        self.lblProgreso = Label(
            text='Cargando recursos... 0%',
            font_size=sf(11),
            color=(1, 1, 1, 0.85),
            size_hint=(1, 1),
            halign='center',
            valign='middle'
        )
        self.lblProgreso.bind(size=self.lblProgreso.setter('text_size'))
        self.contenedorBarra.add_widget(self.lblProgreso)

        # Label de toque (oculto hasta que termine la carga)
        self.tap_label = Label(
            text='TOCA PARA CONTINUAR',
            font_size=sf(11),
            color=(1, 1, 1, 0.6),
            size_hint=(1, None),
            height=sh(20),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            opacity=0
        )

        self.layout.add_widget(self.logo)
        self.layout.add_widget(self.subtitulo)
        self.layout.add_widget(self.contenedorBarra)
        self.layout.add_widget(self.tap_label)
        self.add_widget(self.layout)

    def _upd_bg(self, *args):
        self._bg.pos = self.pos
        self._bg.size = self.size

    def _dibujar_barra(self, *args):
        c = self.contenedorBarra
        c.canvas.before.clear()
        with c.canvas.before:
            # Fondo barra
            Color(0.15, 0.15, 0.20, 0.85)
            RoundedRectangle(pos=c.pos, size=c.size, radius=[dp(6)])
            # Relleno
            Color(0.55, 0.30, 0.85, 1)  # morado tipo Anomalías
            RoundedRectangle(
                pos=c.pos,
                size=(c.width * self._progreso, c.height),
                radius=[dp(6)]
            )

    # ── Ciclo de vida ─────────────────────────────────────────────────────────

    def on_enter(self, *args):
        self._touch_ready = False
        self._carga_completa = False
        Clock.schedule_once(self._animar_entrada, 0.3)

    def on_leave(self, *args):
        if self._auto_event:
            self._auto_event.cancel()
            self._auto_event = None
        Animation.cancel_all(self.tap_label)

    # ── Animaciones de entrada ────────────────────────────────────────────────

    def _animar_entrada(self, dt):
        Animation(opacity=1, duration=1.0, t='in_out_quad').start(self.logo)
        Clock.schedule_once(self._mostrar_subtitulo, 0.5)

    def _mostrar_subtitulo(self, dt):
        Animation(opacity=1, duration=0.8, t='in_out_quad').start(self.subtitulo)
        Clock.schedule_once(self._iniciar_carga, 0.6)

    def _iniciar_carga(self, dt):
        # Mostrar la barra y empezar a precargar
        Animation(opacity=1, duration=0.4, t='in_out_quad').start(self.contenedorBarra)
        self._construir_lista_assets()
        # Cargamos en chunks pequeños cada frame para mantener la UI responsiva
        Clock.schedule_interval(self._cargar_chunk, 1 / 30)

    # ── Precarga ──────────────────────────────────────────────────────────────

    def _construir_lista_assets(self):
        # Recopila todos los frames de animación de los fondos de gacha
        # (son los pesados — el resto Kivy los carga en milisegundos).
        carpetas = [
            'assets/fondos/fondo_gacha_armas',
            'assets/fondos/fondo_gacha_anomalia',
            'assets/fondos/fondo_gacha_guardianes',
        ]
        for carpeta in carpetas:
            if not os.path.isdir(carpeta):
                continue
            for f in sorted(os.listdir(carpeta)):
                if f.endswith('.png'):
                    self._assets_pendientes.append(os.path.join(carpeta, f))
        self._assets_total = max(1, len(self._assets_pendientes))
        self._assets_cargados = 0

    def _cargar_chunk(self, dt):
        # Carga 2 imágenes por frame: ~60 imágenes/segundo a 30fps.
        # Lo suficientemente fluido para que la barra se mueva visiblemente
        # sin bloquear el render.
        for _ in range(2):
            if not self._assets_pendientes:
                break
            path = self._assets_pendientes.pop(0)
            try:
                CoreImage(path, mipmap=True)
            except Exception:
                pass
            self._assets_cargados += 1

        # Actualizar barra
        self._progreso = self._assets_cargados / self._assets_total
        pct = int(self._progreso * 100)
        self.lblProgreso.text = f'Cargando recursos... {pct}%'
        self._dibujar_barra()

        # Carga terminada
        if not self._assets_pendientes:
            self._progreso = 1.0
            self.lblProgreso.text = 'Listo'
            self._dibujar_barra()
            self._carga_completa = True
            Clock.schedule_once(self._mostrar_tap, 0.3)
            return False  # detiene el schedule_interval

    # ── Toque y navegación ────────────────────────────────────────────────────

    def _mostrar_tap(self, dt):
        # Ocultar la barra suavemente y mostrar el "toca para continuar"
        Animation(opacity=0, duration=0.4).start(self.contenedorBarra)
        self.tap_label.opacity = 1
        blink = (
            Animation(opacity=0.15, duration=0.7, t='in_out_sine') +
            Animation(opacity=0.65, duration=0.7, t='in_out_sine')
        )
        blink.repeat = True
        blink.start(self.tap_label)
        self._touch_ready = True
        # Auto-avance a los 3 segundos tras terminar la carga
        self._auto_event = Clock.schedule_once(self._navegar, 3.0)

    def on_touch_down(self, touch):
        if not self._touch_ready:
            return super().on_touch_down(touch)
        self._navegar()
        return True

    def _navegar(self, dt=None):
        if self._auto_event:
            self._auto_event.cancel()
            self._auto_event = None

        destino = 'principal' if (self.gm and self.gm.faccion) else 'seleccion'

        anim = Animation(opacity=0, duration=0.4, t='in_out_quad')
        anim.bind(on_complete=lambda *_: self._cambiar(destino))
        anim.start(self.layout)

    def _cambiar(self, destino):
        self.manager.transition = FadeTransition(duration=0.3)
        self.manager.current = destino