from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.clock import Clock
import random

from config import (
    FONDO_PRINCIPAL, PANEL_OSCURO, PANEL_MEDIO,
    BLANCO, GRIS, COLOR_GUARDIANES, COLOR_ANOMALIAS,
    FONDO_HOME,
    BOTON_PELEAR_COMBATE, BOTON_VOLVER_COMBATE,
    BORDE_LOG_COMBATE, CUADRO_ESPECIAL_COMBATE,
    nombre_personaje, nombre_runa,
    DURACION_SPRITE_ACCION,
    ESTADO_IDLE, ESTADO_ATACANDO, ESTADO_BLOQUEANDO, ESTADO_DERROTA,
    ESTADO_COUNTER, ESTADO_DADO,
    ESTADO_IDLE_B, ESTADO_ATACANDO_B, ESTADO_BLOQUEANDO_B,
    PERSONAJES_CON_COUNTER, PERSONAJES_CON_DADO, PERSONAJES_CON_BERSERKER_B,
    obtenerRutaJugador, obtenerRutaEnemigo, obtenerFondoNodo, obtenerSpriteEnemigo,
    GUERRERO_SPAM_DURACION, GUERRERO_TRAMOS_ATK,
)
from widgets.componentes import BotonRedondeado
from widgets.responsive import sw, sh, sf, sdp

from logic.Combate.Encuentro import Encuentro
from logic.Clases.Guerrero import Guerrero
from logic.Clases.Mago import Mago
from logic.Clases.Asesino import Asesino

# ── Colores ───────────────────────────────────────────────────────────────────
COLOR_LOG           = (0, 0, 0, 1)
COLOR_BERSERKER_ON  = (1.0, 0.55, 0.0, 1)
COLOR_COUNTER_OK    = (0.3, 0.85, 1.0, 1)
COLOR_COUNTER_USADO = (0.5, 0.5,  0.5, 1)
COLOR_DADO_SUERTE   = (1.0, 0.85, 0.0, 1)
COLOR_DADO_FALLO    = (0.7, 0.7,  0.7, 1)

COLOR_BARRA_SPAM   = (0.86, 0.29, 0.29, 1)
COLOR_BARRA_TIMER  = (0.49, 0.47, 0.87, 1)
COLOR_BARRA_BG     = (0.12, 0.12, 0.18, 1)
COLOR_BARRA_BERSER = (0.73, 0.46, 0.09, 1)

# ── Assets del Mago ───────────────────────────────────────────────────────────
BOTON_LANZAR_HECHIZO = 'assets/Botones/BotonLanzarHechizo.png'
RUNAS_MAGO_RUTAS = [
    'assets/Botones/runa_azul.png',
    'assets/Botones/runa_rosa.png',
    'assets/Botones/runa_verde.png',
]


def _incremento_spam(atk):
    for limite, inc in GUERRERO_TRAMOS_ATK:
        if atk <= limite:
            return inc
    return GUERRERO_TRAMOS_ATK[-1][1]


def _duracion_mago(magia):
    """Tiempo en segundos para repetir la secuencia, según la magia."""
    return max(2, 2 + int(magia) // 150)


# =============================================================================
# Widgets internos
# =============================================================================

class _BarraVida(BoxLayout):
    VELOCIDAD = 0.04

    def __init__(self, color, **kwargs):
        super().__init__(**kwargs)
        self.colorVida  = color
        self.porcentaje = 1.0
        self._objetivo  = 1.0
        self._animando  = None
        self.bind(pos=self._dibujar, size=self._dibujar)

    def setVidaInstantaneo(self, porcentaje):
        self._cancelar()
        self.porcentaje = self._objetivo = max(0.0, min(1.0, porcentaje))
        self._dibujar()

    def animarHasta(self, porcentaje):
        self._cancelar()
        self._objetivo = max(0.0, min(1.0, porcentaje))
        if abs(self._objetivo - self.porcentaje) < 0.005:
            self.porcentaje = self._objetivo
            self._dibujar()
            return
        self._animando = Clock.schedule_interval(self._tick, self.VELOCIDAD)

    def _tick(self, dt):
        paso = 0.03
        if self.porcentaje > self._objetivo:
            self.porcentaje = max(self._objetivo, self.porcentaje - paso)
        else:
            self.porcentaje = min(self._objetivo, self.porcentaje + paso)
        self._dibujar()
        if abs(self.porcentaje - self._objetivo) < 0.005:
            self.porcentaje = self._objetivo
            self._dibujar()
            self._cancelar()

    def _cancelar(self):
        if self._animando:
            self._animando.cancel()
            self._animando = None

    def _dibujar(self, *args):
        self.canvas.before.clear()
        x, y = self.pos
        w, h = self.size
        with self.canvas.before:
            Color(0.1, 0.1, 0.15, 1)
            RoundedRectangle(pos=(x, y), size=(w, h), radius=[dp(5)])
            Color(*self.colorVida)
            RoundedRectangle(
                pos=(x + dp(2), y + dp(2)),
                size=(max(0, (w - dp(4)) * self.porcentaje), h - dp(4)),
                radius=[dp(4)]
            )


class _BarraProgreso(BoxLayout):
    def __init__(self, color_relleno, **kwargs):
        super().__init__(**kwargs)
        self.color_relleno = color_relleno
        self.porcentaje    = 0.0
        self.bind(pos=self._dibujar, size=self._dibujar)

    def set_pct(self, pct):
        self.porcentaje = max(0.0, min(1.0, pct))
        self._dibujar()

    def _dibujar(self, *args):
        self.canvas.before.clear()
        x, y = self.pos
        w, h = self.size
        with self.canvas.before:
            Color(*COLOR_BARRA_BG)
            RoundedRectangle(pos=(x, y), size=(w, h), radius=[dp(6)])
            Color(*self.color_relleno)
            relleno = max(0, (w - dp(4)) * self.porcentaje)
            if relleno > 0:
                RoundedRectangle(
                    pos=(x + dp(2), y + dp(2)),
                    size=(relleno, h - dp(4)),
                    radius=[dp(5)]
                )


class _BotonImagen(FloatLayout):
    def __init__(self, texto, ruta_img, color_texto=None, font_size=None,
                 on_press=None, **kwargs):
        super().__init__(**kwargs)
        self._callback = on_press
        self._img = Image(
            source=ruta_img, allow_stretch=True, keep_ratio=False,
            size_hint=(1, 1), pos_hint={'x': 0, 'y': 0},
        )
        self._lbl = Label(
            text=texto, font_size=font_size or dp(18), bold=True,
            color=color_texto or BLANCO,
            size_hint=(1, 1), pos_hint={'x': 0, 'y': 0},
            halign='center', valign='middle',
        )
        self._lbl.bind(size=self._lbl.setter('text_size'))
        self.add_widget(self._img)
        self.add_widget(self._lbl)
        self.bind(on_touch_down=self._on_touch)

    def _on_touch(self, instance, touch):
        if self.collide_point(*touch.pos) and self._callback and not self.disabled:
            self._callback(self)
            return True

    @property
    def text(self):
        return self._lbl.text

    @text.setter
    def text(self, val):
        self._lbl.text = val

    @property
    def disabled(self):
        return self._img.opacity < 0.5

    @disabled.setter
    def disabled(self, val):
        self._img.opacity = 0.4 if val else 1.0
        self._lbl.opacity = 0.4 if val else 1.0


class _BotonRuna(BoxLayout):
    """
    Botón de runa para el minijuego del Mago.
    Estados:
      'normal'  → imagen sola
      'activo'  → overlay amarillo (secuencia mostrándose)
      'correcto'→ overlay verde (input correcto)
      'error'   → overlay rojo (fallo)
    """
    def __init__(self, ruta_img, on_press=None, **kwargs):
        super().__init__(**kwargs)
        self._callback   = on_press
        self._img_source = ruta_img
        self._estado     = 'normal'
        self.bind(pos=self._dibujar, size=self._dibujar,
                  on_touch_down=self._on_touch)

    def set_estado(self, estado):
        self._estado = estado
        self._dibujar()

    def _dibujar(self, *args):
        self.canvas.clear()
        x, y = self.pos
        w, h = self.size
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(source=self._img_source, pos=(x, y), size=(w, h))
            if self._estado == 'activo':
                Color(1, 1, 0, 0.50)
                RoundedRectangle(pos=(x, y), size=(w, h), radius=[dp(8)])
            elif self._estado == 'correcto':
                Color(0.2, 1, 0.3, 0.45)
                RoundedRectangle(pos=(x, y), size=(w, h), radius=[dp(8)])
            elif self._estado == 'error':
                Color(1, 0.1, 0.1, 0.60)
                RoundedRectangle(pos=(x, y), size=(w, h), radius=[dp(8)])

    def _on_touch(self, instance, touch):
        if self.collide_point(*touch.pos) and self._callback:
            self._callback(self)
            return True




class _BarraTiming(BoxLayout):
    """
    Barra con puntero oscilante y zona roja para el minijuego del Asesino.
    El jugador debe pulsar cuando el puntero está dentro de la zona roja.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_puntero = 0.0   # 0.0 → 1.0
        self.zona_ini    = 0.40  # inicio zona roja
        self.zona_fin    = 0.60  # fin zona roja
        self.bind(pos=self._dibujar, size=self._dibujar)

    def actualizar(self, pos_puntero=None, zona_ini=None, zona_fin=None):
        if pos_puntero is not None: self.pos_puntero = max(0.0, min(1.0, pos_puntero))
        if zona_ini    is not None: self.zona_ini    = zona_ini
        if zona_fin    is not None: self.zona_fin    = zona_fin
        self._dibujar()

    def puntero_en_zona(self):
        return self.zona_ini <= self.pos_puntero <= self.zona_fin

    def _dibujar(self, *args):
        self.canvas.before.clear()
        x, y = self.pos
        w, h = self.size
        with self.canvas.before:
            # Fondo
            Color(*COLOR_BARRA_BG)
            RoundedRectangle(pos=(x, y), size=(w, h), radius=[dp(6)])
            # Zona roja
            rx = x + self.zona_ini * w
            rw = (self.zona_fin - self.zona_ini) * w
            Color(0.90, 0.15, 0.15, 0.90)
            RoundedRectangle(pos=(rx, y + dp(2)), size=(rw, h - dp(4)), radius=[dp(4)])
            # Puntero blanco
            px = x + self.pos_puntero * w - dp(3)
            Color(1, 1, 1, 1)
            RoundedRectangle(pos=(px, y), size=(dp(6), h), radius=[dp(3)])

class _PopupBloqueado(ModalView):
    def __init__(self, **kwargs):
        super().__init__(size_hint=(0.75, None), height=sh(140),
                         background_color=(0, 0, 0, 0), **kwargs)
        caja = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(10))
        with caja.canvas.before:
            Color(*PANEL_OSCURO)
            self._r = RoundedRectangle(pos=caja.pos, size=caja.size, radius=[dp(12)])
        caja.bind(
            pos=lambda *a: setattr(self._r, 'pos', caja.pos),
            size=lambda *a: setattr(self._r, 'size', caja.size),
        )
        lbl = Label(
            text='No puedes retirarte durante el combate.\nTermina o pierde primero.',
            font_size=sf(12), color=BLANCO, halign='center', valign='middle', size_hint=(1, 1),
        )
        lbl.bind(size=lbl.setter('text_size'))
        btn = BotonRedondeado(
            text='ENTENDIDO', bg_color=COLOR_GUARDIANES, text_color=FONDO_PRINCIPAL,
            radius=8, size_hint=(0.5, None), height=sh(38), font_size=sf(11), bold=True,
            pos_hint={'center_x': 0.5},
        )
        btn.bind(on_press=lambda *a: self.dismiss())
        caja.add_widget(lbl)
        caja.add_widget(btn)
        self.add_widget(caja)


class _PopupResultado(ModalView):
    def __init__(self, victoria, lineas_recompensa=None, **kwargs):
        super().__init__(size_hint=(0.85, None), height=sh(280),
                         background_color=(0, 0, 0, 0), auto_dismiss=False, **kwargs)
        caja = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(12))
        with caja.canvas.before:
            Color(*PANEL_OSCURO)
            self._r = RoundedRectangle(pos=caja.pos, size=caja.size, radius=[dp(14)])
        caja.bind(
            pos=lambda *a: setattr(self._r, 'pos', caja.pos),
            size=lambda *a: setattr(self._r, 'size', caja.size),
        )
        color_titulo = COLOR_GUARDIANES if victoria else COLOR_ANOMALIAS
        texto_titulo = '¡VICTORIA!' if victoria else '¡DERROTA!'
        lbl_titulo = Label(
            text=texto_titulo, font_size=sf(32), bold=True, color=color_titulo,
            size_hint=(1, None), height=sh(50), halign='center', valign='middle',
        )
        lbl_titulo.bind(size=lbl_titulo.setter('text_size'))
        caja.add_widget(lbl_titulo)
        if victoria and lineas_recompensa:
            for linea in lineas_recompensa:
                lbl = Label(
                    text=linea, font_size=sf(13), bold=True, color=BLANCO,
                    size_hint=(1, None), height=sh(24), halign='center', valign='middle',
                )
                lbl.bind(size=lbl.setter('text_size'))
                caja.add_widget(lbl)
        else:
            lbl_sub = Label(
                text='Intentalo mas adelante', font_size=sf(14), color=GRIS,
                size_hint=(1, None), height=sh(28), halign='center', valign='middle',
            )
            lbl_sub.bind(size=lbl_sub.setter('text_size'))
            caja.add_widget(lbl_sub)
        btn = BotonRedondeado(
            text='CONTINUAR', bg_color=color_titulo, text_color=FONDO_PRINCIPAL,
            radius=8, size_hint=(0.5, None), height=sh(42), font_size=sf(12), bold=True,
            pos_hint={'center_x': 0.5},
        )
        btn.bind(on_press=lambda *a: self.dismiss())
        caja.add_widget(btn)
        self.add_widget(caja)


# =============================================================================
# Pantalla principal
# =============================================================================

class PantallaCombate(Screen):
    def __init__(self, gm=None, **kwargs):
        super().__init__(**kwargs)
        self.gm              = gm
        self.nombreJugador   = ''
        self.nombreEnemigo   = ''
        self.spriteEnemigo   = ''
        self.vidaMaxJugador  = 1
        self.vidaMaxEnemigo  = 1
        self._encuentro      = None
        self._en_combate     = False
        self._timer_sprite   = None
        self._timer_sprite_e = None
        self._counter_usado  = False

        # ── Estado minijuego Guerrero ─────────────────────────────────────────
        self._mj_activo      = False
        self._mj_iniciado    = False
        self._mj_barra       = 0.0
        self._mj_tiempo      = 0.0
        self._mj_duracion    = GUERRERO_SPAM_DURACION
        self._mj_timer       = None
        self._mj_atk_jugador = 0
        self._mj_berserker   = False

        # ── Estado minijuego Asesino ─────────────────────────────────────────
        self._asesino_activo    = False
        self._asesino_pos       = 0.0    # posición del puntero 0.0-1.0
        self._asesino_dir       = 1      # 1=derecha, -1=izquierda
        self._asesino_vel       = 0.5    # fracción de barra por segundo
        self._asesino_timer     = None

        # ── Estado minijuego Mago ─────────────────────────────────────────────
        self._asesino_activo = False
        self._asesino_pos    = 0.0
        self._asesino_dir    = 1
        self._mago_fase      = 'idle'   # 'idle' | 'mostrando' | 'esperando'
        self._mago_secuencia = []       # ej. [2, 0, 1]
        self._mago_input     = []       # lo que va pulsando el jugador
        self._mago_tiempo    = 0.0
        self._mago_duracion  = 3.0
        self._mago_timer     = None
        self._mago_show_ev   = None     # Clock event para mostrar secuencia

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self._bg = Rectangle(source=FONDO_HOME, pos=self.pos, size=self.size)
        self.bind(pos=self._actualizarFondo, size=self._actualizarFondo)

        raiz = BoxLayout(orientation='vertical', padding=dp(8), spacing=dp(4))

        # ── Fila de vida ──────────────────────────────────────────────────────
        filaVida = BoxLayout(orientation='horizontal', size_hint=(1, None),
                             height=sh(88), spacing=dp(6))
        colJ = BoxLayout(orientation='vertical', size_hint=(0.42, 1), spacing=dp(2))
        self.lblNombreJ = Label(text='', font_size=sf(13), color=COLOR_GUARDIANES, bold=True,
                                size_hint=(1, None), height=sh(30), halign='left', valign='middle')
        self.lblNombreJ.bind(size=self.lblNombreJ.setter('text_size'))
        self.barraJ = _BarraVida(color=COLOR_GUARDIANES, size_hint=(1, None), height=sh(32))
        colJ.add_widget(self.lblNombreJ)
        colJ.add_widget(self.barraJ)

        lblVS = Label(text='VS', font_size=sf(26), bold=True, color=BLANCO,
                      size_hint=(0.16, 1), halign='center', valign='middle')
        lblVS.bind(size=lblVS.setter('text_size'))

        colE = BoxLayout(orientation='vertical', size_hint=(0.42, 1), spacing=dp(2))
        self.lblNombreE = Label(text='', font_size=sf(13), color=COLOR_ANOMALIAS, bold=True,
                                size_hint=(1, None), height=sh(30), halign='right', valign='middle')
        self.lblNombreE.bind(size=self.lblNombreE.setter('text_size'))
        self.barraE = _BarraVida(color=COLOR_ANOMALIAS, size_hint=(1, None), height=sh(32))
        colE.add_widget(self.lblNombreE)
        colE.add_widget(self.barraE)

        filaVida.add_widget(colJ)
        filaVida.add_widget(lblVS)
        filaVida.add_widget(colE)

        # ── Zona sprites ──────────────────────────────────────────────────────
        self.zonaSprites = FloatLayout(size_hint=(1, 0.38))
        self.imgFondo = Image(source='', allow_stretch=True, keep_ratio=False,
                              size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        self.imgJugador = Image(source='', allow_stretch=True, keep_ratio=True,
                                size_hint=(0.60, 1.2), pos_hint={'x': -0.02, 'y': -0.08})
        self.imgEnemigo = Image(source='', allow_stretch=True, keep_ratio=True,
                                size_hint=(0.60, 1.2), pos_hint={'x': 0.42, 'y': -0.08})
        self.zonaSprites.add_widget(self.imgFondo)
        self.zonaSprites.add_widget(self.imgJugador)
        self.zonaSprites.add_widget(self.imgEnemigo)

        # ── Panel de minijuego ────────────────────────────────────────────────
        self.zonaMinijuego = BoxLayout(
            orientation='vertical', size_hint=(1, None), height=sh(165),
            spacing=dp(3), padding=[dp(10), dp(6)],
        )
        with self.zonaMinijuego.canvas.before:
            Color(0, 0, 0, 0.65)
            self._rectMJ = RoundedRectangle(
                pos=self.zonaMinijuego.pos, size=self.zonaMinijuego.size, radius=[dp(8)])
        self.zonaMinijuego.bind(
            pos=lambda *a: setattr(self._rectMJ, 'pos', self.zonaMinijuego.pos),
            size=lambda *a: setattr(self._rectMJ, 'size', self.zonaMinijuego.size),
        )

        # fila info: TURNO | barraTimer | habilidad
        filaInfo = BoxLayout(orientation='horizontal', size_hint=(1, None),
                             height=sh(32), spacing=dp(4))
        self.lblTurno = Label(
            text='TURNO 1', font_size=sf(12), bold=True, color=COLOR_GUARDIANES,
            size_hint=(0.28, 1), halign='left', valign='middle')
        self.lblTurno.bind(size=self.lblTurno.setter('text_size'))
        self.barraTimer = _BarraProgreso(
            color_relleno=COLOR_BARRA_TIMER,
            size_hint=(0.54, 0.65),
        )
        self.barraTimer.set_pct(0.0)
        self.lblHabilidad = Label(
            text='', font_size=sf(10), bold=True, color=GRIS,
            size_hint=(0.24, 1), halign='right', valign='middle', opacity=0)
        self.lblHabilidad.bind(size=self.lblHabilidad.setter('text_size'))
        filaInfo.add_widget(self.lblTurno)
        filaInfo.add_widget(self.barraTimer)
        filaInfo.add_widget(self.lblHabilidad)

        # ── Widgets GUERRERO ──────────────────────────────────────────────────
        self.barraSpam = _BarraProgreso(
            color_relleno=COLOR_BARRA_SPAM,
            size_hint=(1, None), height=sh(22),
        )
        self.barraSpam.set_pct(0.0)

        self.filaBtnGolpear = BoxLayout(orientation='horizontal',
                                        size_hint=(1, None), height=sh(52))
        _espLG = BoxLayout(size_hint=(0.2, 1))
        self.btnGolpear = _BotonImagen(
            texto='', ruta_img=BOTON_PELEAR_COMBATE, color_texto=BLANCO,
            font_size=dp(15), on_press=self._onTapGuerrero,
            size_hint=(0.6, 1),
        )
        _espRG = BoxLayout(size_hint=(0.2, 1))
        self.filaBtnGolpear.add_widget(_espLG)
        self.filaBtnGolpear.add_widget(self.btnGolpear)
        self.filaBtnGolpear.add_widget(_espRG)

        # ── Widgets MAGO ──────────────────────────────────────────────────────
        # 3 botones de runa
        self.filaRunas = BoxLayout(orientation='horizontal',
                                   size_hint=(1, None), height=0,
                                   spacing=dp(8), opacity=0)
        self.btnRunas = []
        for i, ruta in enumerate(RUNAS_MAGO_RUTAS):
            br = _BotonRuna(
                ruta_img=ruta,
                on_press=lambda inst, idx=i: self._onTapRuna(idx),
                size_hint=(0.33, 1),
            )
            self.btnRunas.append(br)
            self.filaRunas.add_widget(br)

        # botón lanzar hechizo
        self.filaBtnLanzar = BoxLayout(orientation='horizontal',
                                       size_hint=(1, None), height=0,
                                       spacing=dp(8), opacity=0)
        _espLM = BoxLayout(size_hint=(0.1, 1))
        self.btnLanzar = _BotonImagen(
            texto='', ruta_img=BOTON_LANZAR_HECHIZO, color_texto=BLANCO,
            font_size=dp(12), on_press=self._onTapLanzar,
            size_hint=(0.70, 1),
        )
        _espRM = BoxLayout(size_hint=(0.1, 1))
        self.filaBtnLanzar.add_widget(_espLM)
        self.filaBtnLanzar.add_widget(self.btnLanzar)
        self.filaBtnLanzar.add_widget(_espRM)

        # ── Widgets ASESINO ──────────────────────────────────────────────────
        self.barraTiming = _BarraTiming(size_hint=(1, None), height=0, opacity=0)

        self.filaBtnAtacar = BoxLayout(orientation='horizontal',
                                       size_hint=(1, None), height=0,
                                       spacing=dp(8), opacity=0)
        _espLA = BoxLayout(size_hint=(0.2, 1))
        self.btnAtacar = _BotonImagen(
            texto='', ruta_img='assets/Botones/BotonCuchillada.png', color_texto=BLANCO,
            font_size=dp(14), on_press=self._onTapAtacar,
            size_hint=(0.6, 1),
        )
        _espRA = BoxLayout(size_hint=(0.2, 1))
        self.filaBtnAtacar.add_widget(_espLA)
        self.filaBtnAtacar.add_widget(self.btnAtacar)
        self.filaBtnAtacar.add_widget(_espRA)

        # Añadir todos los widgets al panel
        self.zonaMinijuego.add_widget(filaInfo)
        self.zonaMinijuego.add_widget(self.barraSpam)
        self.zonaMinijuego.add_widget(self.filaBtnGolpear)
        self.zonaMinijuego.add_widget(self.filaRunas)
        self.zonaMinijuego.add_widget(self.filaBtnLanzar)
        self.zonaMinijuego.add_widget(self.barraTiming)
        self.zonaMinijuego.add_widget(self.filaBtnAtacar)

        # ── Zona log ──────────────────────────────────────────────────────────
        zonaLog = BoxLayout(orientation='vertical', size_hint=(1, 0.28),
                            padding=[dp(12), dp(6)], spacing=dp(2))
        with zonaLog.canvas.before:
            Color(0, 0, 0, 0.65)
            self._rectLog = RoundedRectangle(pos=zonaLog.pos, size=zonaLog.size, radius=[dp(8)])
        zonaLog.bind(
            pos=lambda *a: setattr(self._rectLog, 'pos', zonaLog.pos),
            size=lambda *a: setattr(self._rectLog, 'size', zonaLog.size),
        )
        lblLogTitulo = Label(text='EVENTOS DE COMBATE', font_size=sf(11), bold=True,
                             color=COLOR_GUARDIANES, size_hint=(1, None), height=sh(20),
                             halign='center', valign='middle')
        lblLogTitulo.bind(size=lblLogTitulo.setter('text_size'))
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.contenidoLog = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=dp(2))
        self.contenidoLog.bind(minimum_height=self.contenidoLog.setter('height'))
        scroll.add_widget(self.contenidoLog)
        zonaLog.add_widget(lblLogTitulo)
        zonaLog.add_widget(scroll)

        # ── Botón volver ──────────────────────────────────────────────────────
        filaBotones = BoxLayout(orientation='horizontal', size_hint=(1, None), height=sh(70),
                                spacing=dp(10), padding=[dp(8), dp(4)])
        self.btnVolver = _BotonImagen(
            texto='VOLVER', ruta_img=BOTON_VOLVER_COMBATE, color_texto=BLANCO,
            font_size=dp(16), on_press=self._onVolver, size_hint=(1, 1))
        filaBotones.add_widget(self.btnVolver)

        raiz.add_widget(filaVida)
        raiz.add_widget(self.zonaSprites)
        raiz.add_widget(self.zonaMinijuego)
        raiz.add_widget(zonaLog)
        raiz.add_widget(filaBotones)
        self.add_widget(raiz)

    # =========================================================================
    # Mostrar / ocultar paneles según clase
    # =========================================================================

    def _mostrarPanelGuerrero(self):
        self.barraTimer.opacity     = 1
        self.barraSpam.height       = sh(22);  self.barraSpam.opacity      = 1
        self.filaBtnGolpear.height  = sh(52);  self.filaBtnGolpear.opacity = 1
        self.filaRunas.height       = 0;       self.filaRunas.opacity      = 0
        self.filaBtnLanzar.height   = 0;       self.filaBtnLanzar.opacity  = 0

    def _mostrarPanelAsesino(self):
        self.barraSpam.height       = 0;       self.barraSpam.opacity      = 0
        self.filaBtnGolpear.height  = 0;       self.filaBtnGolpear.opacity = 0
        self.filaRunas.height       = 0;       self.filaRunas.opacity      = 0
        self.filaBtnLanzar.height   = 0;       self.filaBtnLanzar.opacity  = 0
        self.barraTimer.opacity     = 0
        self.barraTiming.height     = sh(44);  self.barraTiming.opacity    = 1
        self.filaBtnAtacar.height   = sh(52);  self.filaBtnAtacar.opacity  = 1

    def _mostrarPanelMago(self):
        self.barraTimer.opacity     = 1
        self.barraSpam.height       = 0;       self.barraSpam.opacity      = 0
        self.filaBtnGolpear.height  = 0;       self.filaBtnGolpear.opacity = 0
        self.filaRunas.height       = sh(58);  self.filaRunas.opacity      = 1
        self.filaBtnLanzar.height   = sh(46);  self.filaBtnLanzar.opacity  = 1

    def _ocultarPaneles(self):
        for w in [self.barraSpam, self.filaBtnGolpear,
                  self.filaRunas, self.filaBtnLanzar,
                  self.barraTiming, self.filaBtnAtacar]:
            w.height = 0; w.opacity = 0

    # =========================================================================
    # Ciclo de pantalla
    # =========================================================================

    def on_pre_enter(self, *args):
        self._reset()
        self._cargarDatos()

    def _reset(self):
        self._cancelarTimerSprite()
        self._cancelarTimerSpriteE()
        self._cancelarMJ()
        self._cancelarMJMago()
        self._cancelarMJAsesino()
        self._ocultarPaneles()
        self.limpiarLog()
        self.barraJ.setVidaInstantaneo(1.0)
        self.barraE.setVidaInstantaneo(1.0)
        self.lblTurno.text            = 'TURNO 1'
        self.barraTimer.set_pct(0.0)
        self.barraTimer.color_relleno = COLOR_BARRA_TIMER
        self.barraSpam.set_pct(0.0)
        self.btnGolpear.disabled      = False
        self.lblHabilidad.opacity     = 0
        self.lblHabilidad.text        = ''
        self._en_combate     = False
        self._encuentro      = None
        self.vidaMaxEnemigo  = 1
        self._counter_usado  = False
        self.spriteEnemigo   = ''
        self._mj_activo      = False
        self._mj_iniciado    = False
        self._mago_fase      = 'idle'
        self._mago_secuencia = []
        self._mago_input     = []
        self._asesino_activo = False
        self._asesino_pos    = 0.0
        self._asesino_dir    = 1
        for br in self.btnRunas:
            br.set_estado('normal')

    def _cargarDatos(self):
        if self.gm is None:
            return
        info = self.gm.get_personaje_activo_info()
        if info:
            self.nombreJugador   = info.get('nombre', '')
            self.lblNombreJ.text = nombre_personaje(self.nombreJugador) or self.nombreJugador
            vida_db     = self.gm.get_recursos() or {}
            vida_actual = vida_db.get('vida_actual', info.get('pv_base', 1))
            vida_max    = vida_db.get('vida_max',    info.get('pv_base', 1))
            self.vidaMaxJugador = max(1, vida_max)
            self.barraJ.setVidaInstantaneo(vida_actual / self.vidaMaxJugador)
            if self.nombreJugador:
                self.imgJugador.source = obtenerRutaJugador(self.nombreJugador, ESTADO_IDLE)
                self.imgJugador.reload()
        nodo_id = getattr(self.gm, 'nodo_seleccionado', None)
        if nodo_id is not None:
            nodo = self.gm.get_nodo(nodo_id)
            if nodo and nodo.get('enemigo'):
                enemigo = nodo['enemigo']
                self.nombreEnemigo  = enemigo.get('nombre', '')
                self.vidaMaxEnemigo = max(1, enemigo.get('pv', 1))
                self.barraE.setVidaInstantaneo(1.0)
                faccion = getattr(self.gm, 'faccion', None) or ''
                self.spriteEnemigo = obtenerSpriteEnemigo(nodo_id, faccion)
                partes = self.spriteEnemigo.split('_')
                nombre_key = '_'.join(p.capitalize() for p in partes)
                nombre_display_enemigo = nombre_personaje(nombre_key) or self.nombreEnemigo
                self.nombreEnemigo   = nombre_display_enemigo
                self.lblNombreE.text = nombre_display_enemigo
                self.imgEnemigo.source = obtenerRutaEnemigo(self.spriteEnemigo, ESTADO_IDLE)
                self.imgEnemigo.reload()
            faccion = getattr(self.gm, 'faccion', None)
            if faccion:
                self.imgFondo.source = obtenerFondoNodo(nodo_id, faccion)
                self.imgFondo.reload()

        # Mostrar el panel correcto según la clase del jugador
        nombre_lower = self.nombreJugador.lower()
        if 'mago' in nombre_lower:
            self._mostrarPanelMago()
            self.btnLanzar.disabled = False
        elif 'asesino' in nombre_lower:
            self._mostrarPanelAsesino()
            self.btnAtacar.disabled = False
            # Arrancar el puntero visual con velocidad por defecto
            self._asesino_activo = True
            self._asesino_pos    = 0.0
            self._asesino_dir    = 1
            self._asesino_vel    = 0.60
            ancho    = 0.12
            margen   = 0.05
            zona_ini = random.uniform(margen, 1.0 - ancho - margen)
            self.barraTiming.actualizar(pos_puntero=0.0,
                                        zona_ini=zona_ini,
                                        zona_fin=zona_ini + ancho)
            self._asesino_timer = Clock.schedule_interval(self._tickAsesino, 0.02)
        else:
            self._mostrarPanelGuerrero()
            self.btnGolpear.disabled = False

    # =========================================================================
    # Minijuego GUERRERO — spam de botón
    # =========================================================================

    def _iniciarTurnoGuerrero(self, jugador_obj):
        self._mostrarPanelGuerrero()
        self.lblHabilidad.font_size = sf(10)
        self._mj_activo      = True
        self._mj_iniciado    = False
        self._mj_barra       = 0.0
        self._mj_tiempo      = GUERRERO_SPAM_DURACION
        self._mj_duracion    = GUERRERO_SPAM_DURACION
        self._mj_berserker   = getattr(jugador_obj, 'berserker_activo', False)
        self._mj_atk_jugador = jugador_obj.atk
        color_spam = COLOR_BARRA_BERSER if self._mj_berserker else COLOR_BARRA_SPAM
        self.barraSpam.color_relleno  = color_spam
        self.barraTimer.set_pct(0.0)
        self.barraTimer.color_relleno = COLOR_BARRA_TIMER
        self.barraSpam.set_pct(0.0)
        self.btnGolpear.disabled = False

    def _onTapGuerrero(self, *args):
        if self._encuentro is None:
            self._arrancarEncuentro()
            if self._mj_activo and not self._mj_iniciado:
                self._mj_iniciado = True
                self._cancelarMJ()
                self._mj_timer = Clock.schedule_interval(self._tickTimerGuerrero, 0.1)
            self._sumarTapSpam()
            return
        if not self._mj_activo:
            return
        if not self._mj_iniciado:
            self._mj_iniciado = True
            self._cancelarMJ()
            self._mj_timer = Clock.schedule_interval(self._tickTimerGuerrero, 0.1)
        self._sumarTapSpam()

    def _sumarTapSpam(self):
        if not self._mj_activo:
            return
        inc = _incremento_spam(self._mj_atk_jugador)
        if self._mj_berserker:
            inc = int(inc * 1.5)
        self._mj_barra = min(1.0, self._mj_barra + inc / 100.0)
        self.barraSpam.set_pct(self._mj_barra)
        if self._mj_barra >= 1.0:
            self._resolverGuerrero(exito=True)

    def _tickTimerGuerrero(self, dt):
        if not self._mj_activo or not self._mj_iniciado:
            return
        self._mj_tiempo = max(0.0, self._mj_tiempo - 0.1)
        pct = self._mj_tiempo / max(0.01, self._mj_duracion)
        if self._mj_tiempo <= 1.0:
            self.barraTimer.color_relleno = (0.86, 0.20, 0.20, 1)
        self.barraTimer.set_pct(pct)
        if self._mj_tiempo <= 0:
            self._resolverGuerrero(exito=False)

    def _resolverGuerrero(self, exito):
        if not self._mj_activo:
            return
        self._cancelarMJ()
        self._mj_activo   = False
        self._mj_iniciado = False
        self.btnGolpear.disabled = True
        if self._encuentro is None:
            return
        vida_j_antes = self._encuentro.jugador.vida
        vida_e_antes = self._encuentro.enemigo.vida
        turno_actual = self._encuentro.turno
        r = self._encuentro.turno_paso(jugador_ataca=exito)
        self._procesarResultadoTurno(r, vida_j_antes, vida_e_antes,
                                     exito_minijuego=exito, turno_log=turno_actual)

    def _cancelarMJ(self):
        if self._mj_timer:
            self._mj_timer.cancel()
            self._mj_timer = None

    # =========================================================================
    # Minijuego MAGO — Simon Says con runas
    # =========================================================================

    def _iniciarTurnoMago(self, jugador_obj):
        self._mostrarPanelMago()
        self.lblHabilidad.font_size = sf(10)
        self._mago_fase      = 'idle'
        self._mago_secuencia = []
        self._mago_input     = []
        self._mago_duracion  = _duracion_mago(getattr(jugador_obj, 'magia', 100))
        self.barraTimer.set_pct(0.0)
        self.barraTimer.color_relleno = COLOR_BARRA_TIMER
        for br in self.btnRunas:
            br.set_estado('normal')
        if self._mago_fase == 'idle':
            self.btnLanzar.disabled = False

    def _onTapLanzar(self, *args):
        if self._mago_fase != 'idle':
            return
        if self._encuentro is None:
            self._arrancarEncuentro()
        self.btnLanzar.disabled = True
        self._mago_fase         = 'mostrando'
        self._mago_secuencia     = random.sample([0, 1, 2], 3)
        self._mago_input         = []
        self._mostrarSiguienteRuna(0)

    def _mostrarSiguienteRuna(self, paso):
        """Ilumina las runas en orden, una a una, cada 0.7s."""
        if paso >= len(self._mago_secuencia):
            # Secuencia mostrada — limpiar y activar timer para el jugador
            Clock.schedule_once(lambda dt: self._activarFaseJugador(), 0.3)
            return
        idx = self._mago_secuencia[paso]
        # Iluminar la runa actual
        for i, br in enumerate(self.btnRunas):
            br.set_estado('activo' if i == idx else 'normal')
        # Apagar y pasar a la siguiente
        self._mago_show_ev = Clock.schedule_once(
            lambda dt, p=paso: self._apagarYSiguiente(p), 0.30)

    def _apagarYSiguiente(self, paso):
        for br in self.btnRunas:
            br.set_estado('normal')
        self._mago_show_ev = Clock.schedule_once(
            lambda dt, p=paso+1: self._mostrarSiguienteRuna(p), 0.08)

    def _activarFaseJugador(self):
        """Activa el turno del jugador para repetir la secuencia."""
        self._mago_fase   = 'esperando'
        self._mago_tiempo = self._mago_duracion
        self.barraTimer.set_pct(1.0)
        self.barraTimer.color_relleno = COLOR_BARRA_TIMER
        self._mago_timer = Clock.schedule_interval(self._tickTimerMago, 0.1)

    def _tickTimerMago(self, dt):
        if self._mago_fase != 'esperando':
            return
        self._mago_tiempo = max(0.0, self._mago_tiempo - 0.1)
        pct = self._mago_tiempo / max(0.01, self._mago_duracion)
        if self._mago_tiempo <= 1.0:
            self.barraTimer.color_relleno = (0.86, 0.20, 0.20, 1)
        self.barraTimer.set_pct(pct)
        if self._mago_tiempo <= 0:
            self._resolverMago(exito=False)

    def _onTapRuna(self, idx):
        """El jugador pulsa una de las 3 runas."""
        if self._mago_fase != 'esperando':
            return
        if not self._mago_secuencia:
            return
        self._mago_input.append(idx)
        paso_actual = len(self._mago_input) - 1
        if paso_actual >= len(self._mago_secuencia):
            return

        if idx == self._mago_secuencia[paso_actual]:
            # Correcto hasta aquí
            self.btnRunas[idx].set_estado('correcto')
            if len(self._mago_input) == len(self._mago_secuencia):
                # ¡Secuencia completada!
                self._cancelarMJMago()
                Clock.schedule_once(lambda dt: self._resolverMago(exito=True), 0.3)
        else:
            # Error — poner todas en rojo y fallar
            self._cancelarMJMago()
            for br in self.btnRunas:
                br.set_estado('error')
            Clock.schedule_once(lambda dt: self._resolverMago(exito=False), 0.5)

    def _resolverMago(self, exito):
        if self._mago_fase == 'idle':
            return
        self._mago_fase = 'idle'
        self._cancelarMJMago()
        self.btnLanzar.disabled = True
        if self._encuentro is None:
            return
        vida_j_antes = self._encuentro.jugador.vida
        vida_e_antes = self._encuentro.enemigo.vida
        turno_actual = self._encuentro.turno
        r = self._encuentro.turno_paso(jugador_ataca=exito)
        self._procesarResultadoTurno(r, vida_j_antes, vida_e_antes,
                                     exito_minijuego=exito, turno_log=turno_actual)

    def _cancelarMJMago(self):
        if self._mago_timer:
            self._mago_timer.cancel()
            self._mago_timer = None
        if self._mago_show_ev:
            self._mago_show_ev.cancel()
            self._mago_show_ev = None

    # =========================================================================
    # Minijuego ASESINO — barra con puntero oscilante
    # =========================================================================

    def _iniciarTurnoAsesino(self, jugador_obj):
        self._cancelarMJAsesino()
        self._mostrarPanelAsesino()
        destreza = getattr(jugador_obj, 'destreza', 50)
        if destreza <= 20:
            vel = 1.60
        elif destreza <= 75:
            vel = 1.30
        elif destreza <= 150:
            vel = 1.00
        elif destreza <= 225:
            vel = 0.80
        else:
            vel = 0.60
        ancho = 0.10
        self._asesino_activo = True
        self._asesino_pos    = 0.0
        self._asesino_dir    = 1
        self._asesino_vel    = vel
        margen   = 0.05
        zona_ini = random.uniform(margen, 1.0 - ancho - margen)
        zona_fin = zona_ini + ancho
        self.barraTiming.actualizar(pos_puntero=0.0,
                                    zona_ini=zona_ini, zona_fin=zona_fin)
        self.btnAtacar.disabled = False
        self.lblHabilidad.font_size = sf(13)
        self.lblHabilidad.opacity   = 1
        self.lblHabilidad.text      = 'Esperando tirada...'
        self.lblHabilidad.color     = GRIS
        self._asesino_timer = Clock.schedule_interval(self._tickAsesino, 0.02)

    def _tickAsesino(self, dt):
        if not self._asesino_activo:
            return
        dt = min(dt, 0.05)  # limitar a 20fps mínimo para evitar saltos
        self._asesino_pos += self._asesino_dir * self._asesino_vel * dt
        if self._asesino_pos >= 1.0:
            self._asesino_pos = 1.0
            self._asesino_dir = -1
        elif self._asesino_pos <= 0.0:
            self._asesino_pos = 0.0
            self._asesino_dir = 1
        self.barraTiming.actualizar(pos_puntero=self._asesino_pos)

    def _onTapAtacar(self, *args):
        if not self._asesino_activo:
            return
        # Capturar el resultado ANTES de arrancar (arrancar reinicia la barra)
        exito = self.barraTiming.puntero_en_zona()
        if self._encuentro is None:
            self._arrancarEncuentro()
        self._resolverAsesino(exito)

    def _resolverAsesino(self, exito):
        if not self._asesino_activo:
            return
        self._cancelarMJAsesino()
        self._asesino_activo = False
        self.btnAtacar.disabled = True
        if self._encuentro is None:
            return
        vida_j_antes = self._encuentro.jugador.vida
        vida_e_antes = self._encuentro.enemigo.vida
        turno_actual = self._encuentro.turno
        r = self._encuentro.turno_paso(jugador_ataca=exito)
        self._procesarResultadoTurno(r, vida_j_antes, vida_e_antes,
                                     exito_minijuego=exito, turno_log=turno_actual)

    def _cancelarMJAsesino(self):
        if self._asesino_timer:
            self._asesino_timer.cancel()
            self._asesino_timer = None

    # =========================================================================
    # Arranque del encuentro
    # =========================================================================

    def _arrancarEncuentro(self):
        if self.gm is None:
            return
        nodo_id = getattr(self.gm, 'nodo_seleccionado', None)
        if nodo_id is None:
            self._log('No hay nodo seleccionado.')
            return
        resultado_init = self.gm.preparar_combate(nodo_id)
        if resultado_init is None:
            self._log('No se pudo iniciar el combate.')
            return
        jugador_obj = resultado_init.get('jugador')
        enemigo_obj = resultado_init.get('enemigo')
        if jugador_obj is None or enemigo_obj is None:
            self._log('Faltan datos de combate.')
            return

        prob_sorpresa = 0.0
        try:
            nodo_info = self.gm._mapa_repo.get_nodo(nodo_id)
            if nodo_info and nodo_info['estado'] == 'completado':
                intentos = nodo_info.get('intentos', 0)
                if intentos == 1:   prob_sorpresa = 0.10
                elif intentos == 2: prob_sorpresa = 0.20
                elif intentos >= 3: prob_sorpresa = 0.30
        except Exception:
            prob_sorpresa = 0.0

        self._encuentro = Encuentro()
        self._encuentro.preparar(jugador_obj, enemigo_obj, prob_sorpresa=prob_sorpresa)
        self._en_combate    = True
        self.vidaMaxEnemigo = max(1, enemigo_obj.vida_max)

        if isinstance(jugador_obj, (Guerrero, Mago, Asesino)):
            self.lblHabilidad.opacity = 1
            if isinstance(jugador_obj, Guerrero):
                self.lblHabilidad.text  = 'Berserker: inactivo'
                self.lblHabilidad.color = GRIS
            elif isinstance(jugador_obj, Mago):
                self.lblHabilidad.text  = 'Counter: DISPONIBLE'
                self.lblHabilidad.color = COLOR_COUNTER_OK
            elif isinstance(jugador_obj, Asesino):
                self.lblHabilidad.text  = 'Tirada: -- / --'
                self.lblHabilidad.color = GRIS

        if isinstance(jugador_obj, Guerrero):
            self._iniciarTurnoGuerrero(jugador_obj)
        elif isinstance(jugador_obj, Mago):
            self._iniciarTurnoMago(jugador_obj)
        elif isinstance(jugador_obj, Asesino):
            self._iniciarTurnoAsesino(jugador_obj)

    # =========================================================================
    # Procesado del resultado del turno
    # =========================================================================

    def _procesarResultadoTurno(self, r, vida_j_antes, vida_e_antes,
                                exito_minijuego=True, turno_log=None):
        turno_mostrar = turno_log if turno_log is not None else r['turno']
        self.lblTurno.text = f'TURNO {turno_mostrar}'
        self.barraJ.animarHasta(r['vida_jugador'] / max(1, self.vidaMaxJugador))
        self.barraE.animarHasta(r['vida_enemigo'] / max(1, r['vida_max_e']))

        jugador_obj = self._encuentro.jugador
        if self.lblHabilidad.opacity > 0:
            self._actualizarHabilidad(jugador_obj, r)

        nombre_j       = nombre_personaje(self.nombreJugador) or self.nombreJugador
        nombre_e       = self.nombreEnemigo
        jugador_golpeo = r['vida_enemigo'] < vida_e_antes
        enemigo_golpeo = r['vida_jugador'] < vida_j_antes

        self._log(f'Turno {turno_mostrar}')
        if not exito_minijuego:
            self._log(f'{nombre_j} cargo poco su golpe y no fue efectivo')
        else:
            self._log(f'{nombre_j} golpea con fuerza a {nombre_e}' if jugador_golpeo
                      else f'{nombre_j} ataca pero no logra superar la defensa de {nombre_e}')
        self._log(f'{nombre_e} golpea a {nombre_j}' if enemigo_golpeo
                  else f'{nombre_e} intenta golpear a {nombre_j} pero falla')

        for linea in r['lineas']:
            l = linea.strip()
            if not l: continue
            if l.lower().startswith('turno '): continue
            if 'golpea a' in l.lower() or 'golpea al' in l.lower(): continue
            if 'recibe el ataque' in l.lower(): continue
            nombre_e_interno = self._encuentro.enemigo.nombre if self._encuentro else ''
            self._log(l.replace(self.nombreJugador, nombre_j).replace(nombre_e_interno, nombre_e))
            
        self._logSeparador()
        self._resolverSpritePostTurno(vida_j_antes, vida_e_antes, r)
        self._resolverSpriteEnemigoPostTurno(vida_j_antes, vida_e_antes, r)

        if r['terminado']:
            self._en_combate = False
            self.btnGolpear.disabled = True
            self.btnLanzar.disabled  = True
            if self.gm:
                self.gm.persistir_vida_tras_combate(r['vida_jugador'], r['vida_max_j'])
            if r['victoria']:
                recompensas = self.gm.aplicar_recompensas_nodo(
                    getattr(self.gm, 'nodo_seleccionado', None)) if self.gm else {}
                lineas_rec = []
                if recompensas:
                    if recompensas.get('monedas'):
                        lineas_rec.append(f'Monedas: +{recompensas["monedas"]}')
                    if recompensas.get('runa'):
                        lineas_rec.append(f'Runa obtenida: {nombre_runa(recompensas["runa"])}')
                    if recompensas.get('ticket_personaje'):
                        lineas_rec.append('Ticket de personaje obtenido')
                    if recompensas.get('ticket_arma'):
                        lineas_rec.append('Ticket de arma obtenido')
                    if recompensas.get('transmutador'):
                        lineas_rec.append('Transmutador obtenido')
                    if recompensas.get('fragmentos_personaje'):
                        lineas_rec.append(f'Fragmentos de personaje: +{recompensas["fragmentos_personaje"]}')
                    if recompensas.get('fragmentos_arma'):
                        lineas_rec.append(f'Fragmentos de arma: +{recompensas["fragmentos_arma"]}')
                _PopupResultado(victoria=True, lineas_recompensa=lineas_rec).open()
            else:
                _PopupResultado(victoria=False).open()
        else:
            if isinstance(jugador_obj, Guerrero):
                Clock.schedule_once(
                    lambda dt: self._iniciarTurnoGuerrero(jugador_obj), 0.8)
            elif isinstance(jugador_obj, Mago):
                Clock.schedule_once(
                    lambda dt: self._iniciarTurnoMago(jugador_obj), 0.8)
            elif isinstance(jugador_obj, Asesino):
                Clock.schedule_once(
                    lambda dt: self._iniciarTurnoAsesino(jugador_obj), 0.8)

    # =========================================================================
    # Sprites jugador
    # =========================================================================

    def _cancelarTimerSprite(self):
        if self._timer_sprite:
            self._timer_sprite.cancel()
            self._timer_sprite = None

    def _setSpriteJugador(self, estado, retorno=None):
        self._cancelarTimerSprite()
        if not self.nombreJugador:
            return
        self.imgJugador.source = obtenerRutaJugador(self.nombreJugador, estado)
        self.imgJugador.reload()
        if retorno is not None:
            self._timer_sprite = Clock.schedule_once(
                lambda dt: self._setSpriteJugador(retorno), DURACION_SPRITE_ACCION)

    def _resolverSpritePostTurno(self, vida_j_antes, vida_e_antes, r):
        nombre_lower = self.nombreJugador.lower()
        if r['terminado'] and not r['victoria']:
            self._setSpriteJugador(ESTADO_DERROTA)
            return
        jugador_ataco   = r['vida_enemigo'] < vida_e_antes
        jugador_recibio = r['vida_jugador'] < vida_j_antes
        if r['counter'] and nombre_lower in PERSONAJES_CON_COUNTER:
            self._setSpriteJugador(ESTADO_COUNTER, retorno=ESTADO_IDLE)
            return
        if r['dado'] and nombre_lower in PERSONAJES_CON_DADO:
            self._setSpriteJugador(ESTADO_DADO, retorno=ESTADO_IDLE)
            return
        if r['berserker'] and nombre_lower in PERSONAJES_CON_BERSERKER_B:
            if jugador_ataco:
                self._setSpriteJugador(ESTADO_ATACANDO_B, retorno=ESTADO_IDLE_B)
            elif jugador_recibio:
                self._setSpriteJugador(ESTADO_BLOQUEANDO_B, retorno=ESTADO_IDLE_B)
            else:
                self._setSpriteJugador(ESTADO_IDLE_B)
            return
        if jugador_ataco:
            self._setSpriteJugador(ESTADO_ATACANDO, retorno=ESTADO_IDLE)
        elif jugador_recibio:
            self._setSpriteJugador(ESTADO_BLOQUEANDO, retorno=ESTADO_IDLE)

    # =========================================================================
    # Sprites enemigo
    # =========================================================================

    def _cancelarTimerSpriteE(self):
        if self._timer_sprite_e:
            self._timer_sprite_e.cancel()
            self._timer_sprite_e = None

    def _setSpriteEnemigo(self, estado, retorno=None):
        self._cancelarTimerSpriteE()
        if not self.spriteEnemigo:
            return
        self.imgEnemigo.source = obtenerRutaEnemigo(self.spriteEnemigo, estado)
        self.imgEnemigo.reload()
        if retorno is not None:
            self._timer_sprite_e = Clock.schedule_once(
                lambda dt: self._setSpriteEnemigo(retorno), DURACION_SPRITE_ACCION)

    def _resolverSpriteEnemigoPostTurno(self, vida_j_antes, vida_e_antes, r):
        if r['terminado'] and r['victoria']:
            self._setSpriteEnemigo(ESTADO_DERROTA)
            return
        enemigo_ataco   = r['vida_jugador'] < vida_j_antes
        enemigo_recibio = r['vida_enemigo'] < vida_e_antes
        if enemigo_ataco:
            self._setSpriteEnemigo(ESTADO_ATACANDO, retorno=ESTADO_IDLE)
        elif enemigo_recibio:
            self._setSpriteEnemigo(ESTADO_BLOQUEANDO, retorno=ESTADO_IDLE)

    # =========================================================================
    # Panel habilidad especial
    # =========================================================================

    def _actualizarHabilidad(self, jugador_obj, r):
        if isinstance(jugador_obj, Guerrero):
            if r['berserker']:
                self.lblHabilidad.text  = 'BERSERKER ACTIVO'
                self.lblHabilidad.color = COLOR_BERSERKER_ON
            else:
                self.lblHabilidad.text  = 'Berserker: inactivo'
                self.lblHabilidad.color = GRIS
        elif isinstance(jugador_obj, Mago):
            if r['counter']:
                self._counter_usado = True
            self.lblHabilidad.text  = ('Counter: YA USADO' if self._counter_usado
                                       else 'Counter: DISPONIBLE')
            self.lblHabilidad.color = (COLOR_COUNTER_USADO if self._counter_usado
                                       else COLOR_COUNTER_OK)
        elif isinstance(jugador_obj, Asesino):
            resultado = r['dado_resultado']
            destreza  = jugador_obj.destreza
            if r['dado']:
                self.lblHabilidad.text  = f'Tirada: {resultado}/{destreza}  SUERTE!'
                self.lblHabilidad.color = COLOR_DADO_SUERTE
            else:
                self.lblHabilidad.text  = f'Tirada: {resultado}/{destreza}'
                self.lblHabilidad.color = COLOR_DADO_FALLO

    # =========================================================================
    # Botón volver
    # =========================================================================

    def _onVolver(self, *args):
        if self._en_combate:
            _PopupBloqueado().open()
            return
        self._cancelarTimerSprite()
        self._cancelarTimerSpriteE()
        self._cancelarMJ()
        self._cancelarMJMago()
        self._cancelarMJAsesino()
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current    = 'mapa'

    # =========================================================================
    # Log de combate
    # =========================================================================

    def _log(self, texto):
        lbl = Label(
            text=texto, font_size=sf(12), bold=True, color=BLANCO,
            size_hint=(1, None), height=sh(22), halign='left', valign='top',
            text_size=(None, None),
        )
        lbl.bind(texture_size=lambda inst, val: setattr(inst, 'height', max(sh(22), val[1] + dp(4))))
        lbl.bind(width=lambda inst, val: setattr(inst, 'text_size', (val, None)))
        self.contenidoLog.add_widget(lbl, index=0)
        Clock.schedule_once(
            lambda dt: setattr(self.contenidoLog.parent, 'scroll_y', 0), 0.05)

    def limpiarLog(self):
        self.contenidoLog.clear_widgets()

    def _logSeparador(self):
        lbl = Label(text='', size_hint=(1, None), height=sh(8))
        self.contenidoLog.add_widget(lbl, index=0)

    def _actualizarFondo(self, *args):
        self._bg.pos  = self.pos
        self._bg.size = self.size