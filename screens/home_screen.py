from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp
from widgets.responsive import sw, sh, sf, sdp
from config import (
    PANEL_MEDIO, COLOR_ANOMALIAS, COLOR_GUARDIANES, BLANCO,
    COLOR_VIDA, COLOR_VIDA_MEDIA, COLOR_VIDA_BAJA, COLOR_STATS,
    FONDO_ANOMALIAS, FONDO_GUARDIANES, NOMBRE_ANOMALIA,
    LOGO_ANOMALIA, LOGO_GUARDIAN,
    MARCO_VIDA,
    ICONO_MONEDA, ICONO_GACHA, ICONO_INVENTARIO,
    ICONO_ATK, ICONO_DEF, ICONO_DES, ICONO_MAG, ICONO_POCION,
    FONDO_RUNA_ANOMALIA, FONDO_RUNA_GUARDIAN,
    PAPIRO_ANOMALIA, PAPIRO_GUARDIAN, ICONO_CAMPAÑA, FONDO_HOME,
    PLACEHOLDER, SPRITE_GUARDIAN
)


# ── Tamaño de la barra de vida (proporción del contenedor) ──────────────────
# 1.0 = ocupa todo. Valores menores = barra más pequeña, centrada.
# Si quieres la barra más fina, baja BARRA_VIDA_ALTO_PCT.
# Si quieres la barra más corta, baja BARRA_VIDA_ANCHO_PCT.
BARRA_VIDA_ANCHO_PCT = 0.85   # 85% del ancho del contenedor
BARRA_VIDA_ALTO_PCT  = 0.55   # 55% del alto del contenedor


def _stat_fila(icono_path, etiqueta_texto):
    """Fila [icono | "ETIQUETA: —"] para el panel de stats."""
    fila = BoxLayout(
        orientation='horizontal',
        size_hint=(1, 1),
        spacing=dp(6),
        padding=[dp(2), dp(1)]
    )
    fila.add_widget(Image(
        source=icono_path,
        size_hint=(None, 1),
        width=dp(22),
        allow_stretch=True,
        keep_ratio=True,
        mipmap=True,
        pos_hint={'center_y': 0.5}
    ))
    lbl = Label(
        text=f"{etiqueta_texto}: —",
        font_size=sf(11),
        bold=True,
        color=BLANCO,
        halign='left',
        valign='middle',
        size_hint=(1, 1)
    )
    lbl.bind(size=lbl.setter('text_size'))
    fila.add_widget(lbl)
    return fila, lbl


def _equipo_fila(icono_inicial, ancho_icono):
    """Fila [icono | (nombre arriba, stats debajo)] para runas y arma."""
    fila = BoxLayout(
        orientation='horizontal',
        size_hint=(1, 1),
        spacing=dp(4),
        padding=[dp(2), dp(2)]
    )
    icono = Image(
        source=icono_inicial,
        size_hint=(None, 1),
        width=ancho_icono,
        allow_stretch=True,
        keep_ratio=True,
        mipmap=True
    )
    info = BoxLayout(orientation='vertical', size_hint=(1, 1), spacing=dp(0))
    lbl_nombre = Label(
        text='—',
        font_size=sf(10),
        color=BLANCO,
        bold=True,
        halign='left',
        valign='bottom',
        size_hint=(1, 0.5)
    )
    lbl_nombre.bind(size=lbl_nombre.setter('text_size'))
    lbl_stats = Label(
        text='',
        font_size=sf(9),
        color=COLOR_STATS,
        bold=True,
        halign='left',
        valign='top',
        size_hint=(1, 0.5)
    )
    lbl_stats.bind(size=lbl_stats.setter('text_size'))
    info.add_widget(lbl_nombre)
    info.add_widget(lbl_stats)
    fila.add_widget(icono)
    fila.add_widget(info)
    return fila, icono, lbl_nombre, lbl_stats


class PantallaPrincipal(Screen):
    def __init__(self, gm=None, **kwargs):
        super().__init__(**kwargs)
        self.gm = gm

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self._bg_rect = Rectangle(source=FONDO_HOME, pos=self.pos, size=self.size)
        self.bind(pos=self.actualizarFondo, size=self.actualizarFondo)

        raiz = BoxLayout(orientation='vertical', spacing=0)

        # ── BARRA SUPERIOR (14%) ──────────────────────────────────────────────
        # Subida de 10% a 14% para dar más altura al marco decorativo de la
        # barra de vida. El extra se compensa reduciendo el splash del personaje.
        barraTop = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.14),
            padding=[dp(8), dp(8), dp(16), dp(8)],
            spacing=dp(8)
        )
        with barraTop.canvas.before:
            Color(0, 0, 0, 0.55)
            self._headerRect = Rectangle(pos=barraTop.pos, size=barraTop.size)
        barraTop.bind(
            pos=lambda *a: setattr(self._headerRect, 'pos', barraTop.pos),
            size=lambda *a: setattr(self._headerRect, 'size', barraTop.size)
        )

        self.logoFaccion = Image(
            source=PLACEHOLDER,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(None, 1),
            width=dp(60)
        )

        # ── Barra de vida con marco decorativo superpuesto ───────────────────
        # Capas (de fondo a frente):
        #   1. canvas.before: fondo gris + relleno de color (ocupan todo)
        #   2. self.marcoVida (Image): marco decorativo común
        #   3. self.lblVida (Label): texto "X / Y" centrado
        contenedorVida = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            padding=[0, dp(2)]
        )
        self.barraVida = FloatLayout(size_hint=(1, 1))

        # Capa 2 — marco decorativo (más grande que el contenedor para envolver la barra)
        self.marcoVida = Image(
            source=MARCO_VIDA,
            allow_stretch=True,
            keep_ratio=False,
            mipmap=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(1.15, 1.6)
        )
        self.barraVida.add_widget(self.marcoVida)

        # Capa 3 — texto de vida ("X / Y") centrado
        self.lblVida = Label(
            text='—',
            font_size=sf(12),
            bold=True,
            color=BLANCO,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(None, None)
        )
        self.lblVida.bind(texture_size=lambda lbl, ts: setattr(lbl, 'size', ts))
        self.barraVida.add_widget(self.lblVida)

        contenedorVida.add_widget(self.barraVida)
        self.barraVida.bind(pos=self._dibujarBarraVida, size=self._dibujarBarraVida)

        filaMonedas = BoxLayout(
            orientation='horizontal',
            size_hint=(None, 1),
            width=dp(60),
            spacing=dp(4)
        )
        self.etiquetaMonedas = Label(
            text='0',
            font_size=sf(13),
            bold=True,
            color=COLOR_GUARDIANES,
            size_hint=(1, 1),
            halign='right',
            valign='middle'
        )
        self.etiquetaMonedas.bind(size=self.etiquetaMonedas.setter('text_size'))
        filaMonedas.add_widget(self.etiquetaMonedas)
        filaMonedas.add_widget(Image(
            source=ICONO_MONEDA,
            size_hint=(None, 1),
            width=dp(22),
            allow_stretch=True,
            keep_ratio=True,
            mipmap=True
        ))

        barraTop.add_widget(self.logoFaccion)
        barraTop.add_widget(contenedorVida)
        barraTop.add_widget(filaMonedas)

        # ── SPLASH ART (38%) ──────────────────────────────────────────────────
        # fit_mode='cover': la imagen mantiene proporción y rellena todo el área
        # recortando lo que sobre por los bordes (estilo splash art de gacha).
        self.imagenPersonaje = Image(
            source=SPRITE_GUARDIAN,
            fit_mode='cover',
            mipmap=True,
            size_hint=(1, 0.38)
        )

        # ── PANEL CENTRAL UNIFICADO (30%) ─────────────────────────────────────
        # Reemplaza al antiguo papiro + bloque runas. Un único panel con:
        #   - Mitad izquierda (50%): 5 stats apiladas (icono + etiqueta)
        #   - Mitad derecha (50%): runas (50%) + arma (50%)
        panelCentral = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.30),
            padding=[dp(10), dp(8)],
            spacing=dp(8)
        )
        with panelCentral.canvas.before:
            Color(1, 1, 1, 1)
            self._fondoRunaRect = Rectangle(
                source=PLACEHOLDER,
                pos=panelCentral.pos,
                size=panelCentral.size
            )
        panelCentral.bind(
            pos=lambda *a: setattr(self._fondoRunaRect, 'pos', panelCentral.pos),
            size=lambda *a: setattr(self._fondoRunaRect, 'size', panelCentral.size)
        )

        # ── Mitad izquierda: estadísticas (5 filas) ──────────────────────────
        ladoStats = BoxLayout(
            orientation='vertical',
            size_hint=(0.5, 1),
            spacing=dp(2),
            padding=[dp(4), dp(2)]
        )

        filaAtk, self.lblAtk      = _stat_fila(ICONO_ATK, 'ATAQUE')
        filaDef, self.lblDef      = _stat_fila(ICONO_DEF, 'DEFENSA')
        filaMag, self.lblMagia    = _stat_fila(ICONO_MAG, 'MAGIA')
        filaDes, self.lblDes      = _stat_fila(ICONO_DES, 'DESTREZA')
        filaPoc, self.lblPociones = _stat_fila(ICONO_POCION, 'POCIONES')

        ladoStats.add_widget(filaAtk)
        ladoStats.add_widget(filaDef)
        ladoStats.add_widget(filaMag)
        ladoStats.add_widget(filaDes)
        ladoStats.add_widget(filaPoc)

        # ── Mitad derecha: equipo (runas arriba, arma abajo) ─────────────────
        ladoEquipo = BoxLayout(
            orientation='vertical',
            size_hint=(0.5, 1),
            spacing=dp(4),
            padding=[dp(2), dp(2)]
        )

        bloqueRunas = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.5),
            spacing=dp(2)
        )
        filaRuna1, self.iconoRuna1, self.lblNombreRuna1, self.lblStatRuna1 = \
            _equipo_fila(PLACEHOLDER, dp(32))
        filaRuna2, self.iconoRuna2, self.lblNombreRuna2, self.lblStatRuna2 = \
            _equipo_fila(PLACEHOLDER, dp(32))
        bloqueRunas.add_widget(filaRuna1)
        bloqueRunas.add_widget(filaRuna2)

        bloqueArma = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.5),
            spacing=dp(0)
        )
        filaArma, self.iconoArma, self.lblNombreArma, self.lblStatArma = \
            _equipo_fila(PLACEHOLDER, dp(36))
        bloqueArma.add_widget(filaArma)

        ladoEquipo.add_widget(bloqueRunas)
        ladoEquipo.add_widget(bloqueArma)

        panelCentral.add_widget(ladoStats)
        panelCentral.add_widget(ladoEquipo)

        # ── BARRA NAVEGACIÓN (18%) ────────────────────────────────────────────
        barraNav = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.18),
            padding=[dp(8), dp(8)],
            spacing=dp(8)
        )
        with barraNav.canvas.before:
            Color(0, 0, 0, 0.55)
            self._navRect = Rectangle(pos=barraNav.pos, size=barraNav.size)
        barraNav.bind(
            pos=lambda *a: setattr(self._navRect, 'pos', barraNav.pos),
            size=lambda *a: setattr(self._navRect, 'size', barraNav.size)
        )

        btnGacha = Button(
            background_normal=ICONO_GACHA,
            background_down=ICONO_GACHA,
            background_color=(1, 1, 1, 1),
            size_hint=(None, 1),
            width=dp(80),
            border=(0, 0, 0, 0),
            mipmap=True
        )
        btnGacha.bind(on_press=lambda _: self.navegarA('gacha'))

        btnCampana = Button(
            background_normal=ICONO_CAMPAÑA,
            background_down=ICONO_CAMPAÑA,
            background_color=(1, 1, 1, 1),
            size_hint=(1, 1),
            border=(0, 0, 0, 0),
            mipmap=True
        )
        btnCampana.bind(on_press=lambda _: self.navegarA('mapa'))

        btnInventario = Button(
            background_normal=ICONO_INVENTARIO,
            background_down=ICONO_INVENTARIO,
            background_color=(1, 1, 1, 1),
            size_hint=(None, 1),
            width=dp(80),
            border=(0, 0, 0, 0),
            mipmap=True
        )
        btnInventario.bind(on_press=lambda _: self.navegarA('inventario'))

        barraNav.add_widget(btnGacha)
        barraNav.add_widget(btnCampana)
        barraNav.add_widget(btnInventario)

        raiz.add_widget(barraTop)
        raiz.add_widget(self.imagenPersonaje)
        raiz.add_widget(panelCentral)
        raiz.add_widget(barraNav)
        self.add_widget(raiz)

        self._pociones_actuales = 5
        self._porcentaje_vida = 1.0

    # ── Canvas helpers ────────────────────────────────────────────────────────

    def _dibujarBarraVida(self, *args):
        w = self.barraVida
        pct = max(0.0, min(1.0, self._porcentaje_vida))

        if pct > 0.6:
            color_barra = COLOR_VIDA
        elif pct > 0.3:
            color_barra = COLOR_VIDA_MEDIA
        else:
            color_barra = COLOR_VIDA_BAJA

        # Calcular tamaño y posición de la barra (centrada en el contenedor)
        barra_w = w.width  * BARRA_VIDA_ANCHO_PCT
        barra_h = w.height * BARRA_VIDA_ALTO_PCT
        barra_x = w.x + (w.width  - barra_w) / 2
        barra_y = w.y + (w.height - barra_h) / 2

        w.canvas.before.clear()
        with w.canvas.before:
            # Fondo oscuro
            Color(0.2, 0.2, 0.2, 0.8)
            RoundedRectangle(pos=(barra_x, barra_y), size=(barra_w, barra_h), radius=[dp(4)])
            # Relleno proporcional al porcentaje
            Color(*color_barra)
            RoundedRectangle(pos=(barra_x, barra_y), size=(barra_w * pct, barra_h), radius=[dp(4)])

    # ── Datos ─────────────────────────────────────────────────────────────────

    def on_pre_enter(self, *args):
        self.refrescarDatos()

    def refrescarDatos(self):
        if self.gm is None:
            return
        info = self.gm.get_personaje_activo_info()
        if info is None:
            return

        faccion = self.gm.faccion or ''
        self._bg_rect.source = FONDO_HOME
        if faccion == 'anomalia':
            self.logoFaccion.source    = LOGO_ANOMALIA
            self._fondoRunaRect.source = FONDO_RUNA_ANOMALIA
        else:
            self.logoFaccion.source    = LOGO_GUARDIAN
            self._fondoRunaRect.source = FONDO_RUNA_GUARDIAN
        self.logoFaccion.reload()

        from database.repositories.personaje_repo import get_sprite_path
        sprite = get_sprite_path(
            info.get('faccion', ''),
            info.get('clase', ''),
            info.get('rareza', ''),
            'splash'  # home muestra el splash art
        )
        self.imagenPersonaje.source = sprite
        self.imagenPersonaje.reload()

        # Stats con etiqueta + valor
        self.lblAtk.text   = f"ATAQUE: {info.get('atk_base', '—')}"
        self.lblDef.text   = f"DEFENSA: {info.get('defensa_base', '—')}"
        self.lblMagia.text = f"MAGIA: {info.get('magia_base', '—')}"
        self.lblDes.text   = f"DESTREZA: {info.get('destreza_base', '—')}"

        # Equipo
        from database.repositories import inventario_repo, arma_repo, runa_repo
        equipo     = info.get('equipo', [])
        inv_por_id = {item['id']: item for item in inventario_repo.get_inventario()}

        self.lblNombreArma.text  = '—'
        self.lblStatArma.text    = ''
        self.lblNombreRuna1.text = '—'
        self.lblStatRuna1.text   = ''
        self.lblNombreRuna2.text = '—'
        self.lblStatRuna2.text   = ''

        for slot_info in equipo:
            slot        = slot_info.get('slot', '')
            item_inv_id = slot_info.get('item_inv_id')
            inv_item    = inv_por_id.get(item_inv_id)
            if inv_item is None:
                continue

            if slot == 'arma':
                datos = arma_repo.get_by_id(inv_item['catalogo_id'])
                if datos:
                    self.lblNombreArma.text = datos.get('nombre', '—')
                    self.lblStatArma.text   = f"+{datos.get('bonus_atk',0)}ATK  +{datos.get('bonus_def',0)}DEF"
            elif slot == 'runa_1':
                datos = runa_repo.get_by_id(inv_item['catalogo_id'])
                if datos:
                    self.lblNombreRuna1.text = datos.get('nombre', '—')
                    self.lblStatRuna1.text   = f"+{datos.get('bonus_atk',0)}ATK +{datos.get('bonus_magia',0)}MAG +{datos.get('bonus_def',0)}DEF"
            elif slot == 'runa_2':
                datos = runa_repo.get_by_id(inv_item['catalogo_id'])
                if datos:
                    self.lblNombreRuna2.text = datos.get('nombre', '—')
                    self.lblStatRuna2.text   = f"+{datos.get('bonus_atk',0)}ATK +{datos.get('bonus_magia',0)}MAG +{datos.get('bonus_def',0)}DEF"

        # Pociones (formato "POCIONES: X/5") y monedas
        recursos = self.gm.get_recursos()
        self._pociones_actuales = recursos.get('pociones', 5)
        self.lblPociones.text   = f"POCIONES: {self._pociones_actuales}/5"

        monedas = recursos.get('monedas', 0)
        self.etiquetaMonedas.text = str(monedas)

        # Vida del jugador (barra dinámica)
        vida_actual = recursos.get('vida_actual', 0) or 0
        vida_max    = recursos.get('vida_max', 0)    or 0
        if vida_max <= 0:
            vida_max    = info.get('pv_base', 1) or 1
            vida_actual = vida_max

        self._porcentaje_vida = vida_actual / vida_max if vida_max > 0 else 0.0
        self.lblVida.text = f"{vida_actual} / {vida_max}"
        self._dibujarBarraVida()

    def cargarPersonaje(self, nombreFaccion, rutaSprite, colorAcento):
        self.imagenPersonaje.source = rutaSprite or PLACEHOLDER
        self.imagenPersonaje.reload()
        self._bg_rect.source = FONDO_HOME
        if nombreFaccion == NOMBRE_ANOMALIA:
            self.logoFaccion.source    = LOGO_ANOMALIA
            self._fondoRunaRect.source = FONDO_RUNA_ANOMALIA
        else:
            self.logoFaccion.source    = LOGO_GUARDIAN
            self._fondoRunaRect.source = FONDO_RUNA_GUARDIAN
        self.logoFaccion.reload()

    def navegarA(self, pantalla):
        if pantalla == 'gacha':
            self.manager.transition = SlideTransition(direction='right')
        else:
            self.manager.transition = SlideTransition(direction='left')
        self.manager.current = pantalla

    def actualizarFondo(self, *args):
        self._bg_rect.pos  = self.pos
        self._bg_rect.size = self.size