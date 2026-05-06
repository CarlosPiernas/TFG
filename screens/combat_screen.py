from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from widgets.responsive import sw, sh, sf, sdp

from config import (
    FONDO_PRINCIPAL, PANEL_OSCURO, PANEL_MEDIO,
    BLANCO, GRIS, COLOR_GUARDIANES, COLOR_ANOMALIAS
)
from widgets.componentes import BotonRedondeado

RUTA_JUGABLES = 'assets/personajes/PersonajesS/Jugable'
RUTA_ENEMIGOS = 'assets/personajes/PersonajesS/BOT'

ESTADO_IDLE    = 'idle'
ESTADO_DERROTA = 'defeat-removebg-preview'


def obtenerRutaSprite(nombrePersonaje, estado, esEnemigo=False):
    base = RUTA_ENEMIGOS if esEnemigo else RUTA_JUGABLES
    return f'{base}/{nombrePersonaje}/{nombrePersonaje}{estado}.png'


class _BarraVida(BoxLayout):
    def __init__(self, color, **kwargs):
        super().__init__(**kwargs)
        self.colorVida  = color
        self.porcentaje = 1.0
        self.bind(pos=self._dibujar, size=self._dibujar)

    def actualizarVida(self, porcentaje):
        self.porcentaje = max(0.0, min(1.0, porcentaje))
        self._dibujar()

    def _dibujar(self, *args):
        self.canvas.before.clear()
        x, y = self.pos
        w, h = self.size
        with self.canvas.before:
            Color(*PANEL_OSCURO)
            RoundedRectangle(pos=(x, y), size=(w, h), radius=[dp(4)])
            Color(*self.colorVida)
            RoundedRectangle(
                pos=(x + dp(2), y + dp(2)),
                size=(max(0, (w - dp(4)) * self.porcentaje), h - dp(4)),
                radius=[dp(3)]
            )


class PantallaCombate(Screen):
    def __init__(self, gm=None, **kwargs):
        super().__init__(**kwargs)
        self.gm = gm
        self.nombreJugador = ''
        self.nombreEnemigo = 'PLACEHOLDER'
        self.vidaMaxJugador = 1  # para calcular porcentaje de barra
        self.vidaMaxEnemigo = 1

        with self.canvas.before:
            Color(*FONDO_PRINCIPAL)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.actualizarFondo, size=self.actualizarFondo)

        contenedorPrincipal = BoxLayout(
            orientation='vertical',
            padding=dp(8),
            spacing=dp(6)
        )

        self.etiquetaTurno = Label(
            text='TURNO 1',
            font_size=sf(16),
            bold=True,
            color=COLOR_GUARDIANES,
            size_hint=(1, None),
            height=sh(35),
            halign='center',
            valign='middle'
        )
        self.etiquetaTurno.bind(size=self.etiquetaTurno.setter('text_size'))

        zonaCombate = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.45),
            spacing=dp(8)
        )

        columnaJugador = BoxLayout(orientation='vertical', size_hint=(0.45, 1), spacing=dp(4))
        self.imagenJugador = Image(
            source=obtenerRutaSprite(self.nombreJugador, ESTADO_IDLE),
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 0.85)
        )
        self.barraVidaJugador = _BarraVida(color=COLOR_GUARDIANES, size_hint=(1, 0.15))
        columnaJugador.add_widget(self.imagenJugador)
        columnaJugador.add_widget(self.barraVidaJugador)

        etiquetaVS = Label(
            text='VS',
            font_size=dp(20),
            bold=True,
            color=GRIS,
            size_hint=(0.1, 1),
            halign='center',
            valign='middle'
        )
        etiquetaVS.bind(size=etiquetaVS.setter('text_size'))

        columnaEnemigo = BoxLayout(orientation='vertical', size_hint=(0.45, 1), spacing=dp(4))
        self.imagenEnemigo = Image(
            source='',
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 0.85)
        )
        self.barraVidaEnemigo = _BarraVida(color=COLOR_ANOMALIAS, size_hint=(1, 0.15))
        columnaEnemigo.add_widget(self.imagenEnemigo)
        columnaEnemigo.add_widget(self.barraVidaEnemigo)

        zonaCombate.add_widget(columnaJugador)
        zonaCombate.add_widget(etiquetaVS)
        zonaCombate.add_widget(columnaEnemigo)

        # Log de combate
        contenedorLog = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.35),
            spacing=dp(4),
            padding=dp(6)
        )
        with contenedorLog.canvas.before:
            Color(*PANEL_OSCURO)
            self._rectLog = RoundedRectangle(
                pos=contenedorLog.pos,
                size=contenedorLog.size,
                radius=[dp(10)]
            )
        contenedorLog.bind(
            pos=lambda *a: setattr(self._rectLog, 'pos', contenedorLog.pos),
            size=lambda *a: setattr(self._rectLog, 'size', contenedorLog.size)
        )

        etiquetaLog = Label(
            text='LOG DE COMBATE',
            font_size=sf(10),
            bold=True,
            color=COLOR_GUARDIANES,
            size_hint=(1, None),
            height=sh(24),
            halign='center',
            valign='middle'
        )
        etiquetaLog.bind(size=etiquetaLog.setter('text_size'))

        scrollLog = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.contenidoLog = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            spacing=dp(3)
        )
        self.contenidoLog.bind(minimum_height=self.contenidoLog.setter('height'))
        scrollLog.add_widget(self.contenidoLog)
        contenedorLog.add_widget(etiquetaLog)
        contenedorLog.add_widget(scrollLog)

        # Barra inferior
        barraInferior = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=sh(55),
            spacing=dp(10),
            padding=[dp(10), dp(6)]
        )
        with barraInferior.canvas.before:
            Color(*PANEL_OSCURO)
            self._rectBarra = RoundedRectangle(
                pos=barraInferior.pos,
                size=barraInferior.size,
                radius=[dp(20), dp(20), 0, 0]
            )
        barraInferior.bind(
            pos=lambda *a: setattr(self._rectBarra, 'pos', barraInferior.pos),
            size=lambda *a: setattr(self._rectBarra, 'size', barraInferior.size)
        )

        self.botonVolver = BotonRedondeado(
            text='MAPA',
            bg_color=PANEL_MEDIO,
            text_color=BLANCO,
            radius=8,
            size_hint=(1, 1),
            font_size=dp(12),
            bold=True
        )
        self.botonVolver.bind(on_press=self.volverAlMapa)

        self.botonCombate = BotonRedondeado(
            text='PELEAR',
            bg_color=COLOR_GUARDIANES,
            text_color=FONDO_PRINCIPAL,
            radius=8,
            size_hint=(1, 1),
            font_size=dp(12),
            bold=True
        )
        self.botonCombate.bind(on_press=self.ejecutarCombate)

        barraInferior.add_widget(self.botonVolver)
        barraInferior.add_widget(self.botonCombate)

        contenedorPrincipal.add_widget(self.etiquetaTurno)
        contenedorPrincipal.add_widget(zonaCombate)
        contenedorPrincipal.add_widget(contenedorLog)
        contenedorPrincipal.add_widget(barraInferior)

        self.add_widget(contenedorPrincipal)

    def on_pre_enter(self, *args):
        self.resetearUI()
        self.cargarDatosNodo()

    def resetearUI(self):
        # Limpia el log y resetea barras antes de cada combate
        self.limpiarLog()
        self.barraVidaJugador.actualizarVida(1.0)
        self.barraVidaEnemigo.actualizarVida(1.0)
        self.etiquetaTurno.text = 'TURNO 1'
        self.botonCombate.text = 'PELEAR'

    def cargarDatosNodo(self):
        if self.gm is None:
            return

        # Sprite del jugador
        info = self.gm.get_personaje_activo_info()
        if info:
            self.nombreJugador = info.get('nombre', 'NEXPAS')
            self.vidaMaxJugador = info.get('pv_base', 1)
            sprite = info.get('sprite', '')
            if sprite:
                self.imagenJugador.source = sprite
            elif self.nombreJugador:
                self.imagenJugador.source = obtenerRutaSprite(self.nombreJugador, ESTADO_IDLE)
            self.imagenJugador.reload()

        # Sprite del enemigo desde el nodo seleccionado
        nodo_id = getattr(self.gm, 'nodo_seleccionado', None)
        if nodo_id is not None:
            nodo = self.gm.get_nodo(nodo_id)
            if nodo and nodo.get('enemigo'):
                enemigo = nodo['enemigo']
                self.nombreEnemigo = enemigo.get('nombre', 'PLACEHOLDER')
                self.vidaMaxEnemigo = enemigo.get('pv', 1)
                self.imagenEnemigo.source = obtenerRutaSprite(
                    self.nombreEnemigo, ESTADO_IDLE, esEnemigo=True
                )
                self.imagenEnemigo.reload()

    def ejecutarCombate(self, instance):
        if self.gm is None:
            return

        nodo_id = getattr(self.gm, 'nodo_seleccionado', None)
        if nodo_id is None:
            self.añadirMensajeLog('⚠ No hay nodo seleccionado.')
            return

        self.limpiarLog()
        self.botonCombate.text = '...'

        resultado = self.gm.iniciar_combate(nodo_id)

        # Si el backend bloquea por vida insuficiente, mostrar mensaje
        # claro y resetear el botón. No es derrota: es un aviso.
        if resultado.get('vida_insuficiente'):
            for linea in resultado.get('log', []):
                self.añadirMensajeLog(linea)
            self.botonCombate.text = 'COMBATIR'
            return

        # Mostrar log línea a línea
        for linea in resultado.get('log', []):
            self.añadirMensajeLog(linea)

        # Actualizar turno final
        total_turnos = len([l for l in resultado.get('log', []) if 'Turno' in l])
        if total_turnos:
            self.etiquetaTurno.text = f'TURNO {total_turnos}'

        # Resultado final
        if resultado['victoria']:
            self.añadirMensajeLog('🏆 ¡VICTORIA!')
            recompensas = resultado.get('recompensas') or {}
            if recompensas:
                self.añadirMensajeLog(f"💰 Recompensas: {recompensas}")
            self.botonCombate.text = 'REPETIR'
        else:
            self.añadirMensajeLog('💀 DERROTA')
            self.botonCombate.text = 'REPETIR'

    def añadirMensajeLog(self, mensaje):
        etiqueta = Label(
            text=mensaje,
            font_size=sf(10),
            color=BLANCO,
            size_hint=(1, None),
            height=sh(20),
            halign='left',
            valign='middle'
        )
        etiqueta.bind(size=etiqueta.setter('text_size'))
        self.contenidoLog.add_widget(etiqueta)

    def limpiarLog(self):
        self.contenidoLog.clear_widgets()

    def volverAlMapa(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'mapa'

    def actualizarFondo(self, *args):
        self._bg_rect.pos  = self.pos
        self._bg_rect.size = self.size