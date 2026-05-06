from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.clock import Clock

from config import (
    FONDO_MAPA1_GUARDIANES, FONDO_MAPA2_GUARDIANES,
    FONDO_MAPA1_ANOMALIAS,  FONDO_MAPA2_ANOMALIAS,
    PORTAL_GUARDIANES, PORTAL_ANOMALIAS,
    FLECHA_ARRIBA, FLECHA_ABAJO,
    BOTON_VOLVER, BLANCO
)

POSICIONES_MAPA1 = [
    (0.5,  0.12),
    (0.25, 0.28),
    (0.65, 0.45),
    (0.35, 0.62),
    (0.5,  0.82),
]

POSICIONES_MAPA2 = [
    (0.5,  0.12),
    (0.3,  0.28),
    (0.65, 0.44),
    (0.35, 0.62),
    (0.5,  0.82),
]


class _NodoWidget(FloatLayout):
    def __init__(self, nodo_id, completado, icono_enemigo, icono_completado,
                 gm, navegarCombate, **kwargs):
        super().__init__(**kwargs)
        self.nodo_id          = nodo_id
        self.completado       = completado
        self.icono_enemigo    = icono_enemigo
        self.icono_completado = icono_completado
        self.gm               = gm
        self.navegarCombate   = navegarCombate

        self.img = Image(
            source=icono_completado if completado else icono_enemigo,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0},
            mipmap=True
        )
        self.add_widget(self.img)

        self.btnTouch = Button(
            background_normal='',
            background_color=(0, 0, 0, 0),
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        self.btnTouch.bind(on_press=self._pulsar)
        self.add_widget(self.btnTouch)

    def actualizar(self, completado):
        self.completado  = completado
        self.img.source  = self.icono_completado if completado else self.icono_enemigo
        self.img.reload()

    def _pulsar(self, *args):
        if not self.completado:
            self.gm.nodo_seleccionado = self.nodo_id
            self.navegarCombate()


class PantallaMapa(Screen):
    def __init__(self, gm=None, **kwargs):
        super().__init__(**kwargs)
        self.gm       = gm
        self._pagina  = 0   # 0 = nodos 1-5 | 1 = nodos 6-10
        self._nodos   = []

        self.raiz = FloatLayout()

        # ── FONDO ─────────────────────────────────────────────────────────────
        self.imgFondo = Image(
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0},
            mipmap=True
        )
        self.raiz.add_widget(self.imgFondo)

        # ── NODOS — se construyen vacíos, se rellenan en on_pre_enter ─────────
        self._contenedorNodos = FloatLayout(size_hint=(1, 1))
        self.raiz.add_widget(self._contenedorNodos)

        # ── FLECHA ARRIBA ─────────────────────────────────────────────────────
        self.btnArriba = Button(
            background_normal=FLECHA_ARRIBA,
            background_down=FLECHA_ARRIBA,
            background_color=(1, 1, 1, 1),
            border=(0, 0, 0, 0),
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={'right': 0.95, 'top': 0.97},
            mipmap=True,
            opacity=0
        )
        self.btnArriba.bind(on_press=lambda _: self._cambiarPagina(1))
        self.raiz.add_widget(self.btnArriba)

        # ── FLECHA ABAJO ──────────────────────────────────────────────────────
        self.btnAbajo = Button(
            background_normal=FLECHA_ABAJO,
            background_down=FLECHA_ABAJO,
            background_color=(1, 1, 1, 1),
            border=(0, 0, 0, 0),
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={'right': 0.95, 'y': 0.03},
            mipmap=True,
            opacity=0
        )
        self.btnAbajo.bind(on_press=lambda _: self._cambiarPagina(0))
        self.raiz.add_widget(self.btnAbajo)

        # ── BOTÓN VOLVER ──────────────────────────────────────────────────────
        btnVolver = Button(
            text='VOLVER',
            background_normal=BOTON_VOLVER,
            background_down=BOTON_VOLVER,
            background_color=(1, 1, 1, 1),
            color=BLANCO,
            bold=True,
            font_size=dp(13),
            border=(0, 0, 0, 0),
            size_hint=(None, None),
            size=(dp(120), dp(44)),
            pos_hint={'x': 0.04, 'y': 0.02},
            mipmap=True
        )
        btnVolver.bind(on_press=lambda _: self._volver())
        self.raiz.add_widget(btnVolver)

        self.add_widget(self.raiz)

    # ── Ciclo de vida ─────────────────────────────────────────────────────────

    def on_pre_enter(self, *args):
        self._pagina = 0
        self._construir_pagina()

    # ── Construcción de página ────────────────────────────────────────────────

    def _construir_pagina(self):
        # Determinar facción
        faccion = self.gm.faccion if self.gm else 'guardian'

        # Fondo según página y facción
        if faccion == 'anomalia':
            fondo = FONDO_MAPA2_ANOMALIAS if self._pagina == 1 else FONDO_MAPA1_ANOMALIAS
            icono_enemigo    = PORTAL_GUARDIANES  # anomalías ven portales guardianes
            icono_completado = PORTAL_ANOMALIAS   # al completar se convierte en anomalía
        else:
            fondo = FONDO_MAPA2_GUARDIANES if self._pagina == 1 else FONDO_MAPA1_GUARDIANES
            icono_enemigo    = PORTAL_ANOMALIAS   # guardianes ven portales anomalías
            icono_completado = PORTAL_GUARDIANES  # al completar se convierte en guardián

        self.imgFondo.source = fondo
        self.imgFondo.reload()

        # Limpiar nodos anteriores
        self._contenedorNodos.clear_widgets()
        self._nodos = []

        # Obtener estado de la BD
        nodos_bd = self.gm.get_mapa() if self.gm else []
        offset   = self._pagina * 5  # 0-4 para página 0, 5-9 para página 1
        posiciones = POSICIONES_MAPA2 if self._pagina == 1 else POSICIONES_MAPA1

        for i, (px, py) in enumerate(posiciones):
            nodo_idx = offset + i
            if nodo_idx >= len(nodos_bd):
                break

            nodo_data  = nodos_bd[nodo_idx]
            estado     = nodo_data.get('estado', 'bloqueado')
            completado = estado == 'completado'
            nodo_id    = nodo_data.get('nodo_id', nodo_idx + 1)
            disponible = estado == 'disponible'

            tam = dp(65) if i == 4 else dp(55)  # jefe más grande

            nodo = _NodoWidget(
                nodo_id=nodo_id,
                completado=completado,
                icono_enemigo=icono_enemigo,
                icono_completado=icono_completado,
                gm=self.gm,
                navegarCombate=self._ir_combate,
                size_hint=(None, None),
                size=(tam, tam),
                pos_hint={'center_x': px, 'center_y': py},
                opacity=1.0 if (completado or disponible) else 0.45
            )
            self._contenedorNodos.add_widget(nodo)
            self._nodos.append(nodo)

        # Mostrar flechas según página
        self._actualizar_flechas()

    def _actualizar_flechas(self):
        # Flecha arriba: visible en página 0 si el nodo 5 está completado
        nodos_bd   = self.gm.get_mapa() if self.gm else []
        nodo5_done = len(nodos_bd) > 4 and nodos_bd[4].get('estado') == 'completado'
        nodo10_idx = 9

        if self._pagina == 0:
            self.btnArriba.opacity  = 1 if nodo5_done else 0
            self.btnAbajo.opacity   = 0
        else:
            self.btnArriba.opacity  = 0
            self.btnAbajo.opacity   = 1

    # ── Cambio de página con animación ───────────────────────────────────────

    def _cambiarPagina(self, nueva_pagina):
        if nueva_pagina == self._pagina:
            return

        direccion = 'up' if nueva_pagina == 1 else 'down'

        # Fade out
        anim = Animation(opacity=0, duration=0.3, t='in_out_quad')
        anim.bind(on_complete=lambda *_: self._aplicar_pagina(nueva_pagina))
        anim.start(self._contenedorNodos)
        anim.start(self.imgFondo)

    def _aplicar_pagina(self, nueva_pagina):
        self._pagina = nueva_pagina
        self._construir_pagina()
        # Fade in
        self._contenedorNodos.opacity = 0
        self.imgFondo.opacity         = 0
        Animation(opacity=1, duration=0.3, t='in_out_quad').start(self._contenedorNodos)
        Animation(opacity=1, duration=0.3, t='in_out_quad').start(self.imgFondo)

    # ── Navegación ────────────────────────────────────────────────────────────

    def _ir_combate(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current    = 'combate'

    def _volver(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current    = 'principal'