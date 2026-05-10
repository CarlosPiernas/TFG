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

from config import (
    FONDO_PRINCIPAL, PANEL_OSCURO, PANEL_MEDIO,
    BLANCO, GRIS, COLOR_GUARDIANES, COLOR_ANOMALIAS
)
from widgets.componentes import BotonRedondeado
from widgets.responsive import sw, sh, sf, sdp

from logic.Combate.Encuentro import Encuentro

# ─────────────────────────────────────────────────────────────────────────────
# RUTAS DE SPRITES Y FONDOS
# ─────────────────────────────────────────────────────────────────────────────
RUTA_FONDOS_NODOS = 'assets/fondos/FondosNodos'

ESTADO_IDLE    = 'idle'
ESTADO_DERROTA = 'derrota'


def obtenerRutaJugador(nombre, estado):
    n = nombre.lower()
    return f'assets/characters/{n}/{n}_{estado}.png'


def obtenerRutaEnemigo(nombre, estado):
    return f'assets/personajes/PersonajesS/BOT/{nombre}/{nombre}{estado}.png'


def obtenerFondoNodo(nodo_id: int, faccion: str) -> str:
    fac = 'Guardianes' if 'guardian' in (faccion or '').lower() else 'Anomalias'
    if nodo_id <= 4:
        nombre = f'Nodo1-4{fac}.jpg'
    elif nodo_id == 5:
        nombre = f'Nodo5{fac}.jpg'
    elif nodo_id <= 9:
        nombre = f'Nodo6-9{fac}.jpg'
    else:
        nombre = f'Nodo10{fac}.jpg'
    return f'{RUTA_FONDOS_NODOS}/{nombre}'


# ─────────────────────────────────────────────────────────────────────────────
# BARRA DE VIDA con animación suave
# ─────────────────────────────────────────────────────────────────────────────

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


# ─────────────────────────────────────────────────────────────────────────────
# POPUP bloqueado durante combate
# ─────────────────────────────────────────────────────────────────────────────

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


# ─────────────────────────────────────────────────────────────────────────────
# PANTALLA DE COMBATE
# ─────────────────────────────────────────────────────────────────────────────

class PantallaCombate(Screen):
    def __init__(self, gm=None, **kwargs):
        super().__init__(**kwargs)
        self.gm             = gm
        self.nombreJugador  = ''
        self.nombreEnemigo  = ''
        self.vidaMaxJugador = 1
        self.vidaMaxEnemigo = 1   # se actualiza con vida_max_e del Encuentro al primer turno
        self._encuentro     = None
        self._en_combate    = False

        with self.canvas.before:
            Color(*FONDO_PRINCIPAL)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._actualizarFondo, size=self._actualizarFondo)

        raiz = BoxLayout(orientation='vertical', padding=dp(8), spacing=dp(5))

        # ── 1. BARRAS DE VIDA + VS ─────────────────────────────────────────────
        filaVida = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=sh(38),
            spacing=dp(6),
        )

        colJ = BoxLayout(orientation='vertical', size_hint=(0.44, 1), spacing=dp(2))
        self.lblNombreJ = Label(
            text='—', font_size=sf(9), color=COLOR_GUARDIANES, bold=True,
            size_hint=(1, None), height=sh(14), halign='left', valign='middle',
        )
        self.lblNombreJ.bind(size=self.lblNombreJ.setter('text_size'))
        self.barraJ = _BarraVida(color=COLOR_GUARDIANES, size_hint=(1, None), height=sh(16))
        colJ.add_widget(self.lblNombreJ)
        colJ.add_widget(self.barraJ)

        lblVS = Label(
            text='VS', font_size=sf(13), bold=True, color=GRIS,
            size_hint=(0.12, 1), halign='center', valign='middle',
        )
        lblVS.bind(size=lblVS.setter('text_size'))

        colE = BoxLayout(orientation='vertical', size_hint=(0.44, 1), spacing=dp(2))
        self.lblNombreE = Label(
            text='—', font_size=sf(9), color=COLOR_ANOMALIAS, bold=True,
            size_hint=(1, None), height=sh(14), halign='right', valign='middle',
        )
        self.lblNombreE.bind(size=self.lblNombreE.setter('text_size'))
        self.barraE = _BarraVida(color=COLOR_ANOMALIAS, size_hint=(1, None), height=sh(16))
        colE.add_widget(self.lblNombreE)
        colE.add_widget(self.barraE)

        filaVida.add_widget(colJ)
        filaVida.add_widget(lblVS)
        filaVida.add_widget(colE)

        # ── 2. SPRITES CON FONDO DE NODO ──────────────────────────────────────
        self.zonaSprites = FloatLayout(size_hint=(1, 0.38))

        self.imgFondo = Image(
            source='', allow_stretch=True, keep_ratio=False,
            size_hint=(1, 1), pos_hint={'x': 0, 'y': 0},
        )
        self.imgJugador = Image(
            source='', allow_stretch=True, keep_ratio=True,
            size_hint=(0.45, 1), pos_hint={'x': 0.02, 'y': 0},
        )
        self.imgEnemigo = Image(
            source='', allow_stretch=True, keep_ratio=True,
            size_hint=(0.45, 1), pos_hint={'x': 0.53, 'y': 0},
        )

        self.zonaSprites.add_widget(self.imgFondo)
        self.zonaSprites.add_widget(self.imgJugador)
        self.zonaSprites.add_widget(self.imgEnemigo)

        # ── 3. TURNO + HABILIDAD ESPECIAL ─────────────────────────────────────
        zonaInfo = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=sh(48),
            spacing=dp(2),
            padding=[dp(10), dp(4)],
        )
        with zonaInfo.canvas.before:
            Color(*PANEL_OSCURO)
            self._rectInfo = RoundedRectangle(
                pos=zonaInfo.pos, size=zonaInfo.size, radius=[dp(8)]
            )
        zonaInfo.bind(
            pos=lambda *a: setattr(self._rectInfo, 'pos', zonaInfo.pos),
            size=lambda *a: setattr(self._rectInfo, 'size', zonaInfo.size),
        )

        self.lblTurno = Label(
            text='TURNO 1', font_size=sf(12), bold=True, color=COLOR_GUARDIANES,
            size_hint=(1, None), height=sh(20), halign='center', valign='middle',
        )
        self.lblTurno.bind(size=self.lblTurno.setter('text_size'))

        self.lblHabilidad = Label(
            text='HABILIDAD ESPECIAL: —',
            font_size=sf(10), color=GRIS,
            size_hint=(1, None), height=sh(18),
            halign='center', valign='middle',
            opacity=0,
        )
        self.lblHabilidad.bind(size=self.lblHabilidad.setter('text_size'))

        zonaInfo.add_widget(self.lblTurno)
        zonaInfo.add_widget(self.lblHabilidad)

        # ── 4. LOG ────────────────────────────────────────────────────────────
        zonaLog = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            spacing=dp(2),
            padding=dp(6),
        )
        with zonaLog.canvas.before:
            Color(*PANEL_OSCURO)
            self._rectLog = RoundedRectangle(
                pos=zonaLog.pos, size=zonaLog.size, radius=[dp(8)]
            )
        zonaLog.bind(
            pos=lambda *a: setattr(self._rectLog, 'pos', zonaLog.pos),
            size=lambda *a: setattr(self._rectLog, 'size', zonaLog.size),
        )

        lblLogTitulo = Label(
            text='EVENTOS DE COMBATE',
            font_size=sf(9), bold=True, color=COLOR_GUARDIANES,
            size_hint=(1, None), height=sh(18), halign='center', valign='middle',
        )
        lblLogTitulo.bind(size=lblLogTitulo.setter('text_size'))

        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.contenidoLog = BoxLayout(
            orientation='vertical', size_hint=(1, None), spacing=dp(2),
        )
        self.contenidoLog.bind(minimum_height=self.contenidoLog.setter('height'))
        scroll.add_widget(self.contenidoLog)

        zonaLog.add_widget(lblLogTitulo)
        zonaLog.add_widget(scroll)

        # ── 5. BOTONES ────────────────────────────────────────────────────────
        filaBotones = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=sh(52),
            spacing=dp(10),
            padding=[dp(10), dp(6)],
        )
        with filaBotones.canvas.before:
            Color(*PANEL_OSCURO)
            self._rectBtn = RoundedRectangle(
                pos=filaBotones.pos, size=filaBotones.size,
                radius=[dp(16), dp(16), 0, 0],
            )
        filaBotones.bind(
            pos=lambda *a: setattr(self._rectBtn, 'pos', filaBotones.pos),
            size=lambda *a: setattr(self._rectBtn, 'size', filaBotones.size),
        )

        self.btnVolver = BotonRedondeado(
            text='MAPA', bg_color=PANEL_MEDIO, text_color=BLANCO,
            radius=8, size_hint=(1, 1), font_size=dp(12), bold=True,
        )
        self.btnVolver.bind(on_press=self._onVolver)

        self.btnCombate = BotonRedondeado(
            text='PELEAR', bg_color=COLOR_GUARDIANES, text_color=FONDO_PRINCIPAL,
            radius=8, size_hint=(1, 1), font_size=dp(12), bold=True,
        )
        self.btnCombate.bind(on_press=self._onPelear)

        filaBotones.add_widget(self.btnVolver)
        filaBotones.add_widget(self.btnCombate)

        raiz.add_widget(filaVida)
        raiz.add_widget(self.zonaSprites)
        raiz.add_widget(zonaInfo)
        raiz.add_widget(zonaLog)
        raiz.add_widget(filaBotones)
        self.add_widget(raiz)

    # ─────────────────────────────────────────────────────
    # CICLO DE VIDA
    # ─────────────────────────────────────────────────────

    def on_pre_enter(self, *args):
        self._reset()
        self._cargarDatos()

    # ─────────────────────────────────────────────────────
    # INIT / RESET
    # ─────────────────────────────────────────────────────

    def _reset(self):
        self.limpiarLog()
        self.barraJ.setVidaInstantaneo(1.0)
        self.barraE.setVidaInstantaneo(1.0)
        self.lblTurno.text        = 'TURNO 1'
        self.btnCombate.text      = 'PELEAR'
        self.btnCombate.disabled  = False
        self.lblHabilidad.opacity = 0
        self._en_combate  = False
        self._encuentro   = None
        self.vidaMaxEnemigo = 1   # se fijará en el primer turno_paso

    def _cargarDatos(self):
        if self.gm is None:
            return

        # ── Jugador ──────────────────────────────────────────────────────────
        info = self.gm.get_personaje_activo_info()
        if info:
            self.nombreJugador = info.get('nombre', '')
            self.lblNombreJ.text = self.nombreJugador

            # vida_max real desde BD (incluye bonuses de equipo)
            vida_db = self.gm.get_recursos() or {}
            vida_actual = vida_db.get('vida_actual', info.get('pv_base', 1))
            vida_max    = vida_db.get('vida_max',    info.get('pv_base', 1))
            self.vidaMaxJugador = max(1, vida_max)

            pct = vida_actual / self.vidaMaxJugador
            self.barraJ.setVidaInstantaneo(pct)

            if self.nombreJugador:
                self.imgJugador.source = obtenerRutaJugador(self.nombreJugador, ESTADO_IDLE)
                self.imgJugador.reload()

        # ── Enemigo ───────────────────────────────────────────────────────────
        nodo_id = getattr(self.gm, 'nodo_seleccionado', None)
        if nodo_id is not None:
            nodo = self.gm.get_nodo(nodo_id)
            if nodo and nodo.get('enemigo'):
                enemigo = nodo['enemigo']
                self.nombreEnemigo = enemigo.get('nombre', '')
                # vida_max del enemigo desde el nodo (referencia inicial)
                self.vidaMaxEnemigo = max(1, enemigo.get('pv', 1))
                self.lblNombreE.text = self.nombreEnemigo
                self.barraE.setVidaInstantaneo(1.0)
                if self.nombreEnemigo:
                    self.imgEnemigo.source = obtenerRutaEnemigo(
                        self.nombreEnemigo, ESTADO_IDLE
                    )
                    self.imgEnemigo.reload()

            # Fondo de nodo
            faccion = getattr(self.gm, 'faccion', None)
            if faccion:
                self.imgFondo.source = obtenerFondoNodo(nodo_id, faccion)
                self.imgFondo.reload()

    # ─────────────────────────────────────────────────────
    # BOTONES
    # ─────────────────────────────────────────────────────

    def _onVolver(self, *args):
        if self._en_combate:
            _PopupBloqueado().open()
            return
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current    = 'mapa'

    def _onPelear(self, *args):
        if self.gm is None:
            return

        nodo_id = getattr(self.gm, 'nodo_seleccionado', None)
        if nodo_id is None:
            self._log('⚠ No hay nodo seleccionado.')
            return

        # Modo REPETIR
        if self._encuentro is not None and self._encuentro.terminado:
            self._reset()
            self._cargarDatos()
            return

        # Primera pulsación: preparar combate
        if self._encuentro is None:
            resultado_init = self.gm.preparar_combate(nodo_id)
            if resultado_init is None:
                self._log('⚠ No se pudo iniciar el combate.')
                return

            jugador_obj = resultado_init.get('jugador')
            enemigo_obj = resultado_init.get('enemigo')
            if jugador_obj is None or enemigo_obj is None:
                self._log('⚠ Faltan datos de combate.')
                return

            self._encuentro = Encuentro()
            self._encuentro.preparar(jugador_obj, enemigo_obj)
            self._en_combate = True

            # Fijar vida_max del enemigo desde el objeto real de combate
            self.vidaMaxEnemigo = max(1, enemigo_obj.vida_max)

            self.limpiarLog()
            self._log(f'⚔️  {jugador_obj.nombre}  vs  {enemigo_obj.nombre}')
            self._log('─' * 38)

            from logic.Clases.Guerrero import Guerrero
            if isinstance(jugador_obj, Guerrero):
                self.lblHabilidad.opacity = 1
                self.lblHabilidad.text    = 'HABILIDAD ESPECIAL: Berserker inactivo'
                self.lblHabilidad.color   = GRIS

        # Ejecutar un turno
        r = self._encuentro.turno_paso()

        # Actualizar turno
        self.lblTurno.text = f'TURNO {r["turno"]}'

        # Barra jugador
        pct_j = r['vida_jugador'] / max(1, self.vidaMaxJugador)
        self.barraJ.animarHasta(pct_j)

        # Barra enemigo — usa vida_max_e del propio objeto de combate
        # para garantizar que el porcentaje siempre sea correcto
        pct_e = r['vida_enemigo'] / max(1, r['vida_max_e'])
        self.barraE.animarHasta(pct_e)

        # Habilidad especial
        if self.lblHabilidad.opacity > 0:
            if r['berserker']:
                self.lblHabilidad.text  = 'HABILIDAD ESPECIAL: ⚔️ BERSERKER ACTIVO'
                self.lblHabilidad.color = (1.0, 0.55, 0.0, 1)
            else:
                self.lblHabilidad.text  = 'HABILIDAD ESPECIAL: Berserker inactivo'
                self.lblHabilidad.color = GRIS

        # Log
        for linea in r['lineas']:
            if linea.strip():
                self._log(linea)

        # Fin del combate
        if r['terminado']:
            self._en_combate     = False
            self.btnCombate.text = 'REPETIR'

            if self.gm:
                self.gm.persistir_vida_tras_combate(r['vida_jugador'], r['vida_max_j'])

            if r['victoria']:
                self._log('🏆  ¡VICTORIA!')
                recompensas = self.gm.aplicar_recompensas_nodo(nodo_id) if self.gm else {}
                if recompensas:
                    self._log(f'💰 Recompensas: {recompensas}')
            else:
                self._log('💀  DERROTA')
                if self.nombreJugador:
                    self.imgJugador.source = obtenerRutaJugador(
                        self.nombreJugador, ESTADO_DERROTA
                    )
                    self.imgJugador.reload()

    # ─────────────────────────────────────────────────────
    # LOG
    # ─────────────────────────────────────────────────────

    def _log(self, texto):
        lbl = Label(
            text=texto, font_size=sf(10), color=BLANCO,
            size_hint=(1, None), height=sh(20),
            halign='left', valign='middle',
        )
        lbl.bind(size=lbl.setter('text_size'))
        self.contenidoLog.add_widget(lbl)
        Clock.schedule_once(
            lambda dt: setattr(self.contenidoLog.parent, 'scroll_y', 0), 0.05
        )

    def limpiarLog(self):
        self.contenidoLog.clear_widgets()

    # ─────────────────────────────────────────────────────
    # FONDO
    # ─────────────────────────────────────────────────────

    def _actualizarFondo(self, *args):
        self._bg.pos  = self.pos
        self._bg.size = self.size