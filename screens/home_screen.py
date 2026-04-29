from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp
from config import (
    PANEL_MEDIO, COLOR_ANOMALIAS, COLOR_GUARDIANES, BLANCO, COLOR_VIDA,
    FONDO_ANOMALIAS, FONDO_GUARDIANES, NOMBRE_ANOMALIA,
    LOGO_ANOMALIA, LOGO_GUARDIAN,
    ICONO_MONEDA, ICONO_GACHA, ICONO_INVENTARIO,
    ICONO_ATK, ICONO_DEF, ICONO_DES, ICONO_MAG, ICONO_POCION,
    FONDO_RUNA_ANOMALIA, FONDO_RUNA_GUARDIAN,
    PAPIRO_ANOMALIA, PAPIRO_GUARDIAN, ICONO_CAMPAÑA, FONDO_HOME,
    PLACEHOLDER, SPRITE_GUARDIAN
)


def _icono_label(icono, texto, font_size=dp(11), color=BLANCO):
    fila = BoxLayout(orientation='horizontal', spacing=dp(4), size_hint=(1, 1))
    fila.add_widget(Widget(size_hint=(1, 1)))
    fila.add_widget(Image(
        source=icono,
        size_hint=(None, None),
        size=(dp(32), dp(32)),
        allow_stretch=True,
        keep_ratio=True,
        mipmap=True,
        pos_hint={'center_y': 0.5}
    ))
    lbl = Label(text=texto, font_size=font_size, color=color, halign='left', valign='middle', size_hint=(None, 1), width=dp(30))
    lbl.bind(size=lbl.setter('text_size'))
    fila.add_widget(lbl)
    fila.add_widget(Widget(size_hint=(1, 1)))
    return fila


class PantallaPrincipal(Screen):
    def __init__(self, gm=None, **kwargs):
        super().__init__(**kwargs)
        self.gm = gm

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self._bg_rect = Rectangle(source=FONDO_HOME, pos=self.pos, size=self.size)
        self.bind(pos=self.actualizarFondo, size=self.actualizarFondo)

        raiz = BoxLayout(orientation='vertical', spacing=0)

        # ── BARRA SUPERIOR (10%) ──────────────────────────────────────────────
        barraTop = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.10),
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
            width=dp(70)
        )

        contenedorVida = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            padding=[0, dp(6)]
        )
        self.barraVida = Widget(size_hint=(1, 1))
        contenedorVida.add_widget(self.barraVida)
        self.barraVida.bind(pos=self._dibujarBarraVida, size=self._dibujarBarraVida)

        filaMonedas = BoxLayout(
            orientation='horizontal',
            size_hint=(None, 1),
            width=dp(55),
            spacing=dp(4)
        )
        self.etiquetaMonedas = Label(
            text='0',
            font_size=dp(13),
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

        # ── SPLASH ART (42%) ──────────────────────────────────────────────────
        self.imagenPersonaje = Image(
            source=SPRITE_GUARDIAN,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 0.42)
        )

        # ── PILA PAPIRO + RUNAS/ARMA (38%) ───────────────────────────────────
        filaCentral = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.38),
            spacing=dp(4),
            padding=[dp(10), dp(6)]
        )

        # ── Papiro ────────────────────────────────────────────────────────────
        papiro = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.35),
            padding=[dp(6), dp(4)],
            spacing=dp(4)
        )
        with papiro.canvas.before:
            Color(1, 1, 1, 1)
            self._papiroRect = Rectangle(
                source=PLACEHOLDER,
                pos=papiro.pos,
                size=papiro.size
            )
        papiro.bind(
            pos=lambda *a: setattr(self._papiroRect, 'pos', papiro.pos),
            size=lambda *a: setattr(self._papiroRect, 'size', papiro.size)
        )

        filasStats = BoxLayout(orientation='horizontal', size_hint=(1, 1), spacing=dp(4))
        self.lblAtk   = _icono_label(ICONO_ATK, '—')
        self.lblDef   = _icono_label(ICONO_DEF, '—')
        self.lblMagia = _icono_label(ICONO_MAG, '—')
        self.lblDes   = _icono_label(ICONO_DES, '—')
        filasStats.add_widget(self.lblAtk)
        filasStats.add_widget(self.lblDef)
        filasStats.add_widget(self.lblMagia)
        filasStats.add_widget(self.lblDes)

        self.lblPociones = Label(
            text='5/5',
            font_size=dp(11),
            color=BLANCO,
            halign='left',
            valign='middle',
            size_hint=(None, 1),
            width=dp(30)
        )
        self.lblPociones.bind(size=self.lblPociones.setter('text_size'))

        filaPociones = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(20),
            spacing=dp(4)
        )
        filaPociones.add_widget(Widget(size_hint=(1, 1)))
        filaPociones.add_widget(Image(
            source=ICONO_POCION,
            size_hint=(None, 1),
            width=dp(16),
            allow_stretch=True,
            keep_ratio=True,
            mipmap=True
        ))
        filaPociones.add_widget(self.lblPociones)
        filaPociones.add_widget(Widget(size_hint=(1, 1)))

        papiro.add_widget(Widget(size_hint=(1, 1)))
        papiro.add_widget(filasStats)
        papiro.add_widget(filaPociones)
        papiro.add_widget(Widget(size_hint=(1, 1)))

        # ── Bloque runas/arma ─────────────────────────────────────────────────
        bloqueRunas = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.65),
            padding=[dp(16), dp(10)],
            spacing=dp(8)
        )
        with bloqueRunas.canvas.before:
            Color(1, 1, 1, 1)
            self._fondoRunaRect = Rectangle(
                source=PLACEHOLDER,
                pos=bloqueRunas.pos,
                size=bloqueRunas.size
            )
        bloqueRunas.bind(
            pos=lambda *a: setattr(self._fondoRunaRect, 'pos', bloqueRunas.pos),
            size=lambda *a: setattr(self._fondoRunaRect, 'size', bloqueRunas.size)
        )

        # Lado izquierdo: runas
        ladoRunas = BoxLayout(orientation='vertical', size_hint=(0.55, 1), spacing=dp(6),
                              padding=[0, dp(8)])

        filaRuna1 = BoxLayout(orientation='horizontal', size_hint=(1, 1), spacing=dp(6))
        self.iconoRuna1 = Image(source=PLACEHOLDER, size_hint=(None, 1), width=dp(28), allow_stretch=True, keep_ratio=True, mipmap=True)
        bloqueRuna1 = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.lblNombreRuna1 = Label(text='—', font_size=dp(9), color=BLANCO, bold=True, halign='left', valign='middle', size_hint=(1, 1))
        self.lblNombreRuna1.bind(size=self.lblNombreRuna1.setter('text_size'))
        self.lblStatRuna1 = Label(text='', font_size=dp(8), color=COLOR_GUARDIANES, halign='left', valign='middle', size_hint=(1, 1))
        self.lblStatRuna1.bind(size=self.lblStatRuna1.setter('text_size'))
        bloqueRuna1.add_widget(self.lblNombreRuna1)
        bloqueRuna1.add_widget(self.lblStatRuna1)
        filaRuna1.add_widget(self.iconoRuna1)
        filaRuna1.add_widget(bloqueRuna1)

        filaRuna2 = BoxLayout(orientation='horizontal', size_hint=(1, 1), spacing=dp(6))
        self.iconoRuna2 = Image(source=PLACEHOLDER, size_hint=(None, 1), width=dp(28), allow_stretch=True, keep_ratio=True, mipmap=True)
        bloqueRuna2 = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.lblNombreRuna2 = Label(text='—', font_size=dp(9), color=BLANCO, bold=True, halign='left', valign='middle', size_hint=(1, 1))
        self.lblNombreRuna2.bind(size=self.lblNombreRuna2.setter('text_size'))
        self.lblStatRuna2 = Label(text='', font_size=dp(8), color=COLOR_GUARDIANES, halign='left', valign='middle', size_hint=(1, 1))
        self.lblStatRuna2.bind(size=self.lblStatRuna2.setter('text_size'))
        bloqueRuna2.add_widget(self.lblNombreRuna2)
        bloqueRuna2.add_widget(self.lblStatRuna2)
        filaRuna2.add_widget(self.iconoRuna2)
        filaRuna2.add_widget(bloqueRuna2)

        ladoRunas.add_widget(filaRuna1)
        ladoRunas.add_widget(filaRuna2)

        # Lado derecho: arma
        ladoArma = BoxLayout(orientation='vertical', size_hint=(0.45, 1), spacing=dp(4),
                             padding=[0, dp(8)])
        self.iconoArma = Image(source=PLACEHOLDER, size_hint=(1, 1), allow_stretch=True, keep_ratio=True, mipmap=True)
        self.lblNombreArma = Label(text='—', font_size=dp(9), color=BLANCO, bold=True, halign='center', valign='middle', size_hint=(1, None), height=dp(14))
        self.lblNombreArma.bind(size=self.lblNombreArma.setter('text_size'))
        self.lblStatArma = Label(text='', font_size=dp(8), color=COLOR_GUARDIANES, halign='center', valign='middle', size_hint=(1, None), height=dp(12))
        self.lblStatArma.bind(size=self.lblStatArma.setter('text_size'))
        ladoArma.add_widget(self.iconoArma)
        ladoArma.add_widget(self.lblNombreArma)
        ladoArma.add_widget(self.lblStatArma)

        bloqueRunas.add_widget(ladoRunas)
        bloqueRunas.add_widget(ladoArma)

        filaCentral.add_widget(papiro)
        filaCentral.add_widget(bloqueRunas)

        # ── BARRA NAVEGACIÓN (10%) ────────────────────────────────────────────
        barraNav = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.10),
            padding=[dp(8), dp(8)],
            spacing=dp(8)
        )
        with barraNav.canvas.before:
            Color(0, 0, 0, 0)
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
            width=dp(60),
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
            width=dp(60),
            border=(0, 0, 0, 0),
            mipmap=True
        )
        btnInventario.bind(on_press=lambda _: self.navegarA('inventario'))

        barraNav.add_widget(btnGacha)
        barraNav.add_widget(btnCampana)
        barraNav.add_widget(btnInventario)

        raiz.add_widget(barraTop)
        raiz.add_widget(self.imagenPersonaje)
        raiz.add_widget(filaCentral)
        raiz.add_widget(barraNav)
        self.add_widget(raiz)

        self._pociones_actuales = 5

    # ── Canvas helpers ────────────────────────────────────────────────────────

    def _dibujarBarraVida(self, *args):
        w = self.barraVida
        w.canvas.clear()
        with w.canvas:
            Color(0.2, 0.2, 0.2, 0.8)
            RoundedRectangle(pos=w.pos, size=w.size, radius=[dp(4)])
            Color(*COLOR_VIDA)
            RoundedRectangle(pos=w.pos, size=(w.width * 0.8, w.height), radius=[dp(4)])

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
            self._papiroRect.source    = PAPIRO_ANOMALIA
            self.logoFaccion.source    = LOGO_ANOMALIA
            self._fondoRunaRect.source = FONDO_RUNA_ANOMALIA
        else:
            self._papiroRect.source    = PAPIRO_GUARDIAN
            self.logoFaccion.source    = LOGO_GUARDIAN
            self._fondoRunaRect.source = FONDO_RUNA_GUARDIAN
        self.logoFaccion.reload()

        sprite = info.get('sprite_id', '') or PLACEHOLDER
        self.imagenPersonaje.source = sprite
        self.imagenPersonaje.reload()

        self.lblAtk.children[1].text   = str(info.get('atk_base', '—'))
        self.lblDef.children[1].text   = str(info.get('defensa_base', '—'))
        self.lblMagia.children[1].text = str(info.get('magia_base', '—'))
        self.lblDes.children[1].text   = str(info.get('destreza_base', '—'))

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

        recursos = self.gm.get_recursos()
        self._pociones_actuales = recursos.get('pociones', 5)
        self.lblPociones.text = f"{self._pociones_actuales}/5"

        monedas = recursos.get('monedas', 0)
        self.etiquetaMonedas.text = str(monedas)

    def cargarPersonaje(self, nombreFaccion, rutaSprite, colorAcento):
        self.imagenPersonaje.source = rutaSprite or PLACEHOLDER
        self.imagenPersonaje.reload()
        self._bg_rect.source = FONDO_HOME
        if nombreFaccion == NOMBRE_ANOMALIA:
            self._papiroRect.source    = PAPIRO_ANOMALIA
            self.logoFaccion.source    = LOGO_ANOMALIA
            self._fondoRunaRect.source = FONDO_RUNA_ANOMALIA
        else:
            self._papiroRect.source    = PAPIRO_GUARDIAN
            self.logoFaccion.source    = LOGO_GUARDIAN
            self._fondoRunaRect.source = FONDO_RUNA_GUARDIAN
        self.logoFaccion.reload()

    def navegarA(self, pantalla):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = pantalla

    def actualizarFondo(self, *args):
        self._bg_rect.pos  = self.pos
        self._bg_rect.size = self.size