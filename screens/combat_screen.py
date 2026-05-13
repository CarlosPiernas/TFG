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
)
from widgets.componentes import BotonRedondeado
from widgets.responsive import sw, sh, sf, sdp

from logic.Combate.Encuentro import Encuentro
from logic.Clases.Guerrero import Guerrero
from logic.Clases.Mago import Mago
from logic.Clases.Asesino import Asesino

COLOR_LOG           = (0, 0, 0, 1)
COLOR_BERSERKER_ON  = (1.0, 0.55, 0.0, 1)
COLOR_COUNTER_OK    = (0.3, 0.85, 1.0, 1)
COLOR_COUNTER_USADO = (0.5, 0.5,  0.5, 1)
COLOR_DADO_SUERTE   = (1.0, 0.85, 0.0, 1)
COLOR_DADO_FALLO    = (0.7, 0.7,  0.7, 1)


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
        if self.collide_point(*touch.pos) and self._callback:
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

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self._bg = Rectangle(source=FONDO_HOME, pos=self.pos, size=self.size)
        self.bind(pos=self._actualizarFondo, size=self._actualizarFondo)

        raiz = BoxLayout(orientation='vertical', padding=dp(8), spacing=dp(5))

        # ── Fila de vida ─────────────────────────────────────────────────────
        filaVida = BoxLayout(orientation='horizontal', size_hint=(1, None), height=sh(88), spacing=dp(6))

        colJ = BoxLayout(orientation='vertical', size_hint=(0.42, 1), spacing=dp(2))
        # FIX nº2: font_size reducido de sf(19) a sf(13)
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
        # FIX nº2: font_size reducido de sf(19) a sf(13)
        self.lblNombreE = Label(text='', font_size=sf(13), color=COLOR_ANOMALIAS, bold=True,
                                size_hint=(1, None), height=sh(30), halign='right', valign='middle')
        self.lblNombreE.bind(size=self.lblNombreE.setter('text_size'))
        self.barraE = _BarraVida(color=COLOR_ANOMALIAS, size_hint=(1, None), height=sh(32))
        colE.add_widget(self.lblNombreE)
        colE.add_widget(self.barraE)

        filaVida.add_widget(colJ)
        filaVida.add_widget(lblVS)
        filaVida.add_widget(colE)

        # ── Zona sprites ─────────────────────────────────────────────────────
        self.zonaSprites = FloatLayout(size_hint=(1, 0.43))
        self.imgFondo = Image(source='', allow_stretch=True, keep_ratio=False,
                              size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        self.imgJugador = Image(source='', allow_stretch=True, keep_ratio=True,
                                size_hint=(0.60, 1.2), pos_hint={'x': -0.02, 'y': -0.05})
        self.imgEnemigo = Image(source='', allow_stretch=True, keep_ratio=True,
                                size_hint=(0.60, 1.2), pos_hint={'x': 0.42, 'y': -0.05})
        self.zonaSprites.add_widget(self.imgFondo)
        self.zonaSprites.add_widget(self.imgJugador)
        self.zonaSprites.add_widget(self.imgEnemigo)

        # ── Zona info turno/habilidad ─────────────────────────────────────────
        zonaInfo = BoxLayout(orientation='vertical', size_hint=(1, None), height=sh(72),
                             spacing=dp(2), padding=[dp(10), dp(4)])
        with zonaInfo.canvas.before:
            Color(0, 0, 0, 0.65)
            self._rectInfo = RoundedRectangle(pos=zonaInfo.pos, size=zonaInfo.size, radius=[dp(8)])
        zonaInfo.bind(
            pos=lambda *a: setattr(self._rectInfo, 'pos', zonaInfo.pos),
            size=lambda *a: setattr(self._rectInfo, 'size', zonaInfo.size),
        )
        self.lblTurno = Label(text='TURNO 1', font_size=sf(15), bold=True, color=COLOR_GUARDIANES,
                              size_hint=(1, None), height=sh(26), halign='center', valign='middle')
        self.lblTurno.bind(size=self.lblTurno.setter('text_size'))
        self.lblHabilidad = Label(text='', font_size=sf(12), bold=True, color=GRIS,
                                  size_hint=(1, None), height=sh(22),
                                  halign='center', valign='middle', opacity=0)
        self.lblHabilidad.bind(size=self.lblHabilidad.setter('text_size'))
        zonaInfo.add_widget(self.lblTurno)
        zonaInfo.add_widget(self.lblHabilidad)

        # ── Zona log ──────────────────────────────────────────────────────────
        zonaLog = BoxLayout(orientation='vertical', size_hint=(1, 0.5),
                            padding=[dp(12), dp(8)], spacing=dp(4))
        with zonaLog.canvas.before:
            Color(0, 0, 0, 0.65)
            self._rectLog = RoundedRectangle(pos=zonaLog.pos, size=zonaLog.size, radius=[dp(8)])
        zonaLog.bind(
            pos=lambda *a: setattr(self._rectLog, 'pos', zonaLog.pos),
            size=lambda *a: setattr(self._rectLog, 'size', zonaLog.size),
        )
        lblLogTitulo = Label(text='EVENTOS DE COMBATE', font_size=sf(13), bold=True,
                             color=COLOR_GUARDIANES, size_hint=(1, None), height=sh(24),
                             halign='center', valign='middle')
        lblLogTitulo.bind(size=lblLogTitulo.setter('text_size'))
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.contenidoLog = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=dp(2))
        self.contenidoLog.bind(minimum_height=self.contenidoLog.setter('height'))
        scroll.add_widget(self.contenidoLog)
        zonaLog.add_widget(lblLogTitulo)
        zonaLog.add_widget(scroll)

        # ── Botones ───────────────────────────────────────────────────────────
        filaBotones = BoxLayout(orientation='horizontal', size_hint=(1, None), height=sh(90),
                                spacing=dp(10), padding=[dp(8), dp(6)])
        self.btnVolver = _BotonImagen(
            texto='VOLVER', ruta_img=BOTON_VOLVER_COMBATE, color_texto=BLANCO,
            font_size=dp(16), on_press=self._onVolver, size_hint=(1, 1))
        self.btnCombate = _BotonImagen(
            texto='', ruta_img=BOTON_PELEAR_COMBATE, color_texto=BLANCO,
            font_size=dp(18), on_press=self._onPelear, size_hint=(1, 1))
        filaBotones.add_widget(self.btnVolver)
        filaBotones.add_widget(self.btnCombate)

        raiz.add_widget(filaVida)
        raiz.add_widget(self.zonaSprites)
        raiz.add_widget(zonaInfo)
        raiz.add_widget(zonaLog)
        raiz.add_widget(filaBotones)
        self.add_widget(raiz)

    def on_pre_enter(self, *args):
        self._reset()
        self._cargarDatos()

    def _reset(self):
        self._cancelarTimerSprite()
        self._cancelarTimerSpriteE()
        self.limpiarLog()
        self.barraJ.setVidaInstantaneo(1.0)
        self.barraE.setVidaInstantaneo(1.0)
        self.lblTurno.text        = 'TURNO 1'
        self.btnCombate.text      = ''
        self.btnCombate.disabled  = False
        self.lblHabilidad.opacity = 0
        self.lblHabilidad.text    = ''
        self._en_combate    = False
        self._encuentro     = None
        self.vidaMaxEnemigo = 1
        self._counter_usado = False
        self.spriteEnemigo  = ''

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

                # Determinar sprite del enemigo según nodo y facción del jugador
                faccion = getattr(self.gm, 'faccion', None) or ''
                self.spriteEnemigo = obtenerSpriteEnemigo(nodo_id, faccion)

                # FIX nº3: nombre display a partir del sprite
                # 'anomalia_guerrero_b' → 'Anomalia_Guerrero_B' → 'Cascarón Errante'
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

    # ── Sprites del jugador ───────────────────────────────────────────────────

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

    # ── Sprites del enemigo ───────────────────────────────────────────────────

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

    # ── Panel habilidad ───────────────────────────────────────────────────────

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
            if self._counter_usado:
                self.lblHabilidad.text  = 'Counter: YA USADO'
                self.lblHabilidad.color = COLOR_COUNTER_USADO
            else:
                self.lblHabilidad.text  = 'Counter: DISPONIBLE'
                self.lblHabilidad.color = COLOR_COUNTER_OK
        elif isinstance(jugador_obj, Asesino):
            resultado = r['dado_resultado']
            destreza  = jugador_obj.destreza
            if r['dado']:
                self.lblHabilidad.text  = f'Tirada: {resultado}/{destreza}  SUERTE!'
                self.lblHabilidad.color = COLOR_DADO_SUERTE
            else:
                self.lblHabilidad.text  = f'Tirada: {resultado}/{destreza}'
                self.lblHabilidad.color = COLOR_DADO_FALLO

    # ── Botones ───────────────────────────────────────────────────────────────

    def _onVolver(self, *args):
        if self._en_combate:
            _PopupBloqueado().open()
            return
        self._cancelarTimerSprite()
        self._cancelarTimerSpriteE()
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current    = 'mapa'

    def _onPelear(self, *args):
        if self.gm is None:
            return
        nodo_id = getattr(self.gm, 'nodo_seleccionado', None)
        if nodo_id is None:
            self._log('No hay nodo seleccionado.')
            return

        if self._encuentro is not None and self._encuentro.terminado:
            self._reset()
            self._cargarDatos()
            return

        if self._encuentro is None:
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
                    if intentos == 1:
                        prob_sorpresa = 0.10
                    elif intentos == 2:
                        prob_sorpresa = 0.20
                    elif intentos >= 3:
                        prob_sorpresa = 0.30
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

        vida_j_antes = self._encuentro.jugador.vida
        vida_e_antes = self._encuentro.enemigo.vida

        r = self._encuentro.turno_paso()

        self.lblTurno.text = f'TURNO {r["turno"]}'
        self.barraJ.animarHasta(r['vida_jugador'] / max(1, self.vidaMaxJugador))
        self.barraE.animarHasta(r['vida_enemigo'] / max(1, r['vida_max_e']))

        jugador_obj = self._encuentro.jugador
        if self.lblHabilidad.opacity > 0:
            self._actualizarHabilidad(jugador_obj, r)

        nombre_display = nombre_personaje(self.nombreJugador) or self.nombreJugador
        for linea in r['lineas']:
            if linea.strip():
                self._log(linea.replace(self.nombreJugador, nombre_display))
        self._logSeparador()

        self._resolverSpritePostTurno(vida_j_antes, vida_e_antes, r)
        self._resolverSpriteEnemigoPostTurno(vida_j_antes, vida_e_antes, r)

        if r['terminado']:
            self._en_combate     = False
            self.btnCombate.text = ''
            if self.gm:
                self.gm.persistir_vida_tras_combate(r['vida_jugador'], r['vida_max_j'])
            if r['victoria']:
                recompensas = self.gm.aplicar_recompensas_nodo(nodo_id) if self.gm else {}
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

    # ── Log ───────────────────────────────────────────────────────────────────

    def _log(self, texto):
        lbl = Label(
            text=texto, font_size=sf(13), bold=True, color=BLANCO,
            size_hint=(1, None), height=sh(22), halign='left', valign='middle',
        )
        lbl.bind(size=lbl.setter('text_size'))
        self.contenidoLog.add_widget(lbl)
        Clock.schedule_once(
            lambda dt: setattr(self.contenidoLog.parent, 'scroll_y', 0), 0.05)

    def limpiarLog(self):
        self.contenidoLog.clear_widgets()

    def _logSeparador(self):
        lbl = Label(text='', size_hint=(1, None), height=sh(8))
        self.contenidoLog.add_widget(lbl)

    def _actualizarFondo(self, *args):
        self._bg.pos  = self.pos
        self._bg.size = self.size