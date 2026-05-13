from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.modalview import ModalView
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp
from widgets.responsive import sw, sh, sf, sdp
from config import (
    PANEL_OSCURO, PANEL_MEDIO,
    COLOR_ANOMALIAS, COLOR_GUARDIANES, BLANCO, GRIS, COLOR_STATS,
    CABECERA_INVENTARIO,
    BOTON_PERSONAJES, BOTON_ARMAS, BOTON_RUNAS, BOTON_OBJETOS,
    MARCO_BOTON, BOTON_FORJAR,
    FONDO_HOME, FONDO_RUNA_ANOMALIA, FONDO_RUNA_GUARDIAN,
    PLACEHOLDER, ICONO_POCION,
    SLOT_RUNA_VACIO,
    icono_arma, nombre_arma, lore_arma,
    icono_runa, nombre_runa, lore_runa,
    icono_personaje, nombre_personaje, lore_personaje,
)

# ── Textos de habilidad por clase ────────────────────────────────────────────
HABILIDAD_CLASE = {
    'guerrero': 'Al estar en aprietos el guerrero potencia su ataque entrando en estado Berserker.',
    'mago':     'Al recibir daño una vez por combate lanzara CounterSpell y dañara a su enemigo.',
    'asesino':  'Antes de golpear cada turno lanzara un dado e intentara realizar un golpe extra.',
}


# ── Image que se comporta como botón (click en el icono = seleccionar item) ─
class IconoClicable(ButtonBehavior, Image):
    pass


# ── Botón con marco decorativo PNG (reutilizado de forja_screen) ───────────
class BotonConMarco(FloatLayout):
    def __init__(self, texto='VOLVER', marco_path=MARCO_BOTON,
                 on_press_callback=None, **kwargs):
        super().__init__(**kwargs)

        self.imagenMarco = Image(
            source=marco_path,
            allow_stretch=True,
            keep_ratio=False,
            mipmap=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(1, 1)
        )
        self.add_widget(self.imagenMarco)

        self.boton = Button(
            text=texto,
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=BLANCO,
            font_size=dp(15),
            bold=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(1, 1)
        )
        if on_press_callback is not None:
            self.boton.bind(on_press=on_press_callback)
        self.add_widget(self.boton)


# ── Pestaña de categoría con PNG de fondo ──────────────────────────────────
class PestañaCategoria(FloatLayout):
    def __init__(self, marco_path, categoria, on_press_callback, **kwargs):
        super().__init__(**kwargs)
        self.categoria = categoria
        self._activa = False

        with self.canvas.before:
            Color(0, 0, 0, 0.55)
            self._fondoRect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
        self.bind(
            pos=lambda *a: setattr(self._fondoRect, 'pos', self.pos),
            size=lambda *a: setattr(self._fondoRect, 'size', self.size)
        )

        self.imagenMarco = Image(
            source=marco_path,
            allow_stretch=True,
            keep_ratio=True,
            mipmap=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(1, 1)
        )
        self.add_widget(self.imagenMarco)

        with self.canvas.after:
            Color(*COLOR_GUARDIANES)
            self._bordeLine = Line(
                rounded_rectangle=(0, 0, 0, 0, 0),
                width=1.6
            )
        self.bind(pos=self._actualizarBorde, size=self._actualizarBorde)

        self.boton = Button(
            background_normal='',
            background_color=(0, 0, 0, 0),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(1, 1)
        )
        self.boton.bind(on_press=lambda _: on_press_callback(categoria))
        self.add_widget(self.boton)

    def _actualizarBorde(self, *args):
        if self._activa:
            self._bordeLine.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(8))

    def set_activa(self, activa: bool):
        self._activa = activa
        if activa:
            self._bordeLine.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(8))
        else:
            self._bordeLine.rounded_rectangle = (0, 0, 0, 0, 0)
        self.imagenMarco.opacity = 1.0


class PantallaInventario(Screen):
    def __init__(self, gm=None, **kwargs):
        super().__init__(**kwargs)
        self.gm = gm

        self.categoriaActual = 'personajes'
        self.itemSeleccionado = None

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self._bg_rect = Rectangle(source=FONDO_HOME, pos=self.pos, size=self.size)
        self.bind(pos=self._actualizarFondo, size=self._actualizarFondo)

        with self.canvas.before:
            Color(0, 0, 0, 0.45)
            self._overlay = Rectangle(pos=self.pos, size=self.size)
        self.bind(
            pos=lambda *a: setattr(self._overlay, 'pos', self.pos),
            size=lambda *a: setattr(self._overlay, 'size', self.size)
        )

        raiz = BoxLayout(orientation='vertical', spacing=0)

        cabecera = Image(
            source=CABECERA_INVENTARIO,
            allow_stretch=True,
            keep_ratio=False,
            mipmap=True,
            size_hint=(1, 0.15)
        )

        filaPestañas = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.10),
            padding=[dp(6), dp(4)],
            spacing=dp(4)
        )

        self.pestañas = {}
        for nombre, png in [
            ('personajes', BOTON_PERSONAJES),
            ('armas',      BOTON_ARMAS),
            ('runas',      BOTON_RUNAS),
            ('objetos',    BOTON_OBJETOS),
        ]:
            pestaña = PestañaCategoria(png, nombre, self.cambiarCategoria, size_hint=(0.25, 1))
            filaPestañas.add_widget(pestaña)
            self.pestañas[nombre] = pestaña

        contenedorScroll = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.15),
            padding=[dp(8), dp(4)]
        )
        with contenedorScroll.canvas.before:
            Color(0, 0, 0, 0.55)
            self._scrRect = Rectangle(pos=contenedorScroll.pos, size=contenedorScroll.size)
        contenedorScroll.bind(
            pos=lambda *a: setattr(self._scrRect, 'pos', contenedorScroll.pos),
            size=lambda *a: setattr(self._scrRect, 'size', contenedorScroll.size)
        )

        scrollItems = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=True,
            do_scroll_y=False,
            bar_width=dp(4)
        )
        self.filaItems = BoxLayout(
            orientation='horizontal',
            size_hint=(None, 1),
            spacing=dp(8),
            padding=[dp(6), dp(2)]
        )
        self.filaItems.bind(minimum_width=self.filaItems.setter('width'))
        scrollItems.add_widget(self.filaItems)
        contenedorScroll.add_widget(scrollItems)

        zonaDetalle = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.30),
            padding=[dp(8), dp(4)],
            spacing=dp(8)
        )

        self.previewBox = BoxLayout(
            orientation='vertical',
            size_hint=(0.45, 1),
            padding=[dp(4), dp(4)]
        )
        with self.previewBox.canvas.before:
            Color(0, 0, 0, 0.5)
            self._prevRect = RoundedRectangle(
                pos=self.previewBox.pos,
                size=self.previewBox.size,
                radius=[dp(8)]
            )
        self.previewBox.bind(
            pos=lambda *a: setattr(self._prevRect, 'pos', self.previewBox.pos),
            size=lambda *a: setattr(self._prevRect, 'size', self.previewBox.size)
        )
        self.imagenPreview = Image(
            source='',
            fit_mode='contain',
            mipmap=True,
            size_hint=(1, 1),
            opacity=0
        )
        self.previewBox.add_widget(self.imagenPreview)

        columnaStats = BoxLayout(
            orientation='vertical',
            size_hint=(0.55, 1),
            spacing=dp(6)
        )

        cajaStats = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.65),
            padding=[dp(10), dp(6)]
        )
        with cajaStats.canvas.before:
            Color(0, 0, 0, 0.5)
            self._stRect = RoundedRectangle(
                pos=cajaStats.pos, size=cajaStats.size, radius=[dp(8)]
            )
        cajaStats.bind(
            pos=lambda *a: setattr(self._stRect, 'pos', cajaStats.pos),
            size=lambda *a: setattr(self._stRect, 'size', cajaStats.size)
        )
        self.lblStats = Label(
            text='Selecciona un item',
            font_size=sf(12),
            color=BLANCO,
            bold=True,
            halign='left',
            valign='top',
            size_hint=(1, 1)
        )
        self.lblStats.bind(size=self.lblStats.setter('text_size'))
        cajaStats.add_widget(self.lblStats)
        columnaStats.add_widget(cajaStats)

        self.botonEquipar = BotonConMarco(
            texto='EQUIPAR',
            marco_path=MARCO_BOTON,
            on_press_callback=self.confirmarSeleccion,
            size_hint=(1, 0.35)
        )
        columnaStats.add_widget(self.botonEquipar)

        zonaDetalle.add_widget(self.previewBox)
        zonaDetalle.add_widget(columnaStats)

        panelExplicativo = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.18),
            padding=[dp(12), dp(8)]
        )
        with panelExplicativo.canvas.before:
            Color(0, 0, 0, 0.6)
            self._panelRect = RoundedRectangle(
                pos=panelExplicativo.pos,
                size=panelExplicativo.size,
                radius=[dp(8)]
            )
        panelExplicativo.bind(
            pos=lambda *a: setattr(self._panelRect, 'pos', panelExplicativo.pos),
            size=lambda *a: setattr(self._panelRect, 'size', panelExplicativo.size)
        )
        self.lblDescripcion = Label(
            text='Selecciona un item para ver su descripción.',
            font_size=sf(11),
            color=BLANCO,
            italic=True,
            halign='left',
            valign='top',
            size_hint=(1, 1)
        )
        self.lblDescripcion.bind(size=self.lblDescripcion.setter('text_size'))
        panelExplicativo.add_widget(self.lblDescripcion)

        botonera = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.12),
            padding=[dp(20), dp(8)],
            spacing=dp(20)
        )
        with botonera.canvas.before:
            Color(0, 0, 0, 0.55)
            self._botRect = Rectangle(pos=botonera.pos, size=botonera.size)
        botonera.bind(
            pos=lambda *a: setattr(self._botRect, 'pos', botonera.pos),
            size=lambda *a: setattr(self._botRect, 'size', botonera.size)
        )

        botonVolver = BotonConMarco(
            texto='VOLVER',
            marco_path=MARCO_BOTON,
            on_press_callback=self.volverAHome,
            size_hint=(0.5, 1)
        )
        botonForja = BotonConMarco(
            texto='FORJA',
            marco_path=MARCO_BOTON,
            on_press_callback=self.irAForja,
            size_hint=(0.5, 1)
        )
        botonera.add_widget(botonVolver)
        botonera.add_widget(botonForja)

        raiz.add_widget(cabecera)
        raiz.add_widget(filaPestañas)
        raiz.add_widget(contenedorScroll)
        raiz.add_widget(zonaDetalle)
        raiz.add_widget(panelExplicativo)
        raiz.add_widget(botonera)
        self.add_widget(raiz)

    # ── Eventos del ciclo de vida ────────────────────────────────────────

    def on_pre_enter(self, *args):
        self.cambiarCategoria(self.categoriaActual)

    def cambiarCategoria(self, categoria: str):
        self.categoriaActual = categoria
        self.itemSeleccionado = None

        for nombre, pestaña in self.pestañas.items():
            pestaña.set_activa(nombre == categoria)

        self.imagenPreview.source = ''
        self.imagenPreview.opacity = 0
        self.lblStats.text = 'Selecciona un item'
        self.lblDescripcion.text = 'Selecciona un item para ver su descripción.'

        self._cargarItems(categoria)

    def _cargarItems(self, categoria: str):
        self.filaItems.clear_widgets()
        if self.gm is None:
            return

        items = self._obtenerItems(categoria)

        if not items:
            lbl = Label(
                text=f'No tienes {categoria} disponibles',
                font_size=dp(11),
                color=GRIS,
                size_hint=(None, 1),
                width=dp(200)
            )
            self.filaItems.add_widget(lbl)
            return

        for item in items:
            tarjeta = self._crearTarjeta(item, categoria)
            self.filaItems.add_widget(tarjeta)

    def _obtenerItems(self, categoria: str):
        if categoria == 'personajes':
            items = self.gm.get_personajes_jugador()
            for it in items:
                nombre_db = it.get('nombre', '')
                it['icono']          = icono_personaje(nombre_db)
                it['nombre_display'] = nombre_personaje(nombre_db)
                it['descripcion']    = lore_personaje(nombre_db)
            return items

        elif categoria == 'armas':
            items = self.gm.get_armas_jugador()
            for it in items:
                nombre_db = it.get('nombre', '')
                it['icono']          = icono_arma(nombre_db)
                it['nombre_display'] = nombre_arma(nombre_db)
                it['descripcion']    = lore_arma(nombre_db)
            return items

        elif categoria == 'runas':
            items = self.gm.get_runas_jugador()
            for it in items:
                nombre_db = it.get('nombre', '')
                it['icono']          = icono_runa(nombre_db)
                it['nombre_display'] = nombre_runa(nombre_db)
                it['descripcion']    = lore_runa(nombre_db)
            return items

        elif categoria == 'objetos':
            return self._obtenerObjetosVirtuales()

        return []

    def _obtenerObjetosVirtuales(self):
        recursos = self.gm.get_recursos() or {}
        objetos = []
        if recursos.get('pociones', 0) > 0:
            objetos.append({
                'nombre':        'Poción',
                'nombre_display': 'Poción',
                'cantidad':      recursos.get('pociones', 0),
                'tipo_objeto':   'pocion',
                'usable':        True,
                'descripcion':   'Frasco de líquido carmesí. Restaura toda tu vida al instante. Úsalo entre nodos para llegar al jefe en plena forma.',
                'icono':         'assets/logos/Logo_Pocion.png',
                'inv_id':        None,
            })
        if recursos.get('transmutadores', 0) > 0:
            objetos.append({
                'nombre':        'Transmutador',
                'nombre_display': 'Transmutador',
                'cantidad':      recursos.get('transmutadores', 0),
                'tipo_objeto':   'transmutador',
                'usable':        False,
                'descripcion':   'Catalizador arcano. Permite combinar dos runas básicas en la Forja para obtener una runa mixta.',
                'icono':         'assets/logos/CargaTransmutacion.png',
                'inv_id':        None,
            })
        if recursos.get('fragmentos_rojos', 0) > 0:
            objetos.append({
                'nombre':        'Fragmento Rojo',
                'nombre_display': 'Fragmento Rojo',
                'cantidad':      recursos.get('fragmentos_rojos', 0),
                'tipo_objeto':   'fragmento_rojo',
                'usable':        False,
                'descripcion':   'Fragmento rojizo de un alma rota. Acumula 50 para invocar a un personaje sin gastar tickets.',
                'icono':         'assets/logos/Fragmento_Rojo.png',
                'inv_id':        None,
            })
        if recursos.get('fragmentos_azules', 0) > 0:
            objetos.append({
                'nombre':        'Fragmento Azul',
                'nombre_display': 'Fragmento Azul',
                'cantidad':      recursos.get('fragmentos_azules', 0),
                'tipo_objeto':   'fragmento_azul',
                'usable':        False,
                'descripcion':   'Esquirla azul de metal arcano. Acumula 50 para forjar un arma sin gastar tickets.',
                'icono':         'assets/logos/Fragmento_Azul.png',
                'inv_id':        None,
            })
        return objetos

    def _crearTarjeta(self, item: dict, categoria: str):
        contenedor = BoxLayout(
            orientation='vertical',
            size_hint=(None, 1),
            width=sw(110),
            padding=[dp(4), dp(4)]
        )

        nombre_display = item.get('nombre_display') or item.get('nombre', '?')
        if categoria == 'objetos':
            etiqueta = f"{nombre_display} x{item.get('cantidad', 0)}"
        else:
            etiqueta = nombre_display

        icono = item.get('icono')

        if icono:
            img = IconoClicable(
                source=icono,
                allow_stretch=True,
                keep_ratio=True,
                mipmap=True,
                size_hint=(1, 0.65),
            )
            img.bind(on_press=lambda _, it=item: self.seleccionarItem(it))
            contenedor.add_widget(img)

            btn = Button(
                text=etiqueta,
                background_color=(0.08, 0.08, 0.15, 0.95),
                background_normal='',
                color=(0.9, 0.75, 0.3, 1),
                font_size=dp(10),
                bold=True,
                size_hint=(1, 0.35),
            )
            btn.bind(on_press=lambda _, it=item: self.seleccionarItem(it))
            contenedor.add_widget(btn)
        else:
            btn = Button(
                text=etiqueta,
                background_color=(0.08, 0.08, 0.15, 0.95),
                background_normal='',
                color=(0.9, 0.75, 0.3, 1),
                font_size=dp(10),
                bold=True,
                size_hint=(1, 1),
            )
            btn.bind(on_press=lambda _, it=item: self.seleccionarItem(it))
            contenedor.add_widget(btn)

        return contenedor

    def seleccionarItem(self, item: dict):
        self.itemSeleccionado = item

        if self.categoriaActual == 'personajes':
            from database.repositories.personaje_repo import get_sprite_path
            ruta_imagen = get_sprite_path(
                item.get('faccion', ''),
                item.get('clase', ''),
                item.get('rareza', ''),
                'inventario'
            )
        else:
            ruta_imagen = item.get('icono') or PLACEHOLDER

        self.imagenPreview.source  = ruta_imagen
        self.imagenPreview.opacity = 1
        self.imagenPreview.reload()

        self.lblStats.text = self._formatearStats(item)

        descripcion = item.get('descripcion')
        if not descripcion:
            descripcion = self._descripcionGenerica(item)
        self.lblDescripcion.text = descripcion

    def _formatearStats(self, item: dict) -> str:
        nombre_display = item.get('nombre_display') or item.get('nombre', '?')

        if self.categoriaActual == 'personajes':
            clase = item.get('clase', '').lower()
            habilidad = HABILIDAD_CLASE.get(clase, '')
            texto = (
                f"{nombre_display}\n"
                f"Clase: {item.get('clase', '?').capitalize()}\n"
                f"Rareza: {item.get('rareza', '?')}\n\n"
                f"ATK: {item.get('atk_base', 0)}\n"
                f"DEF: {item.get('defensa_base', 0)}\n"
                f"MAG: {item.get('magia_base', 0)}\n"
                f"DES: {item.get('destreza_base', 0)}\n"
                f"PV:  {item.get('pv_base', 0)}"
            )
            if habilidad:
                texto += f"\n\n{habilidad}"
            return texto

        elif self.categoriaActual == 'armas':
            return (
                f"{nombre_display}\n"
                f"Rareza: {item.get('rareza', '?')}\n\n"
                f"+ATK: {item.get('bonus_atk', 0)}\n"
                f"+DEF: {item.get('bonus_def', 0)}\n"
                f"+MAG: {item.get('bonus_magia', 0)}\n"
                f"+DES: {item.get('bonus_destreza', 0)}"
            )
        elif self.categoriaActual == 'runas':
            return (
                f"{nombre_display}\n"
                f"Rareza: {item.get('rareza', '?')}\n\n"
                f"+ATK: {item.get('bonus_atk', 0)}\n"
                f"+DEF: {item.get('bonus_def', 0)}\n"
                f"+MAG: {item.get('bonus_magia', 0)}\n"
                f"+DES: {item.get('bonus_destreza', 0)}"
            )
        elif self.categoriaActual == 'objetos':
            return (
                f"{nombre_display}\n"
                f"Cantidad: {item.get('cantidad', 0)}\n\n"
                f"Tipo: Consumible"
            )
        return ''

    def _descripcionGenerica(self, item: dict) -> str:
        if self.categoriaActual == 'personajes':
            return f"Combatiente de la facción {item.get('faccion', '?').capitalize()}."
        elif self.categoriaActual == 'armas':
            return f"Arma de rareza {item.get('rareza', '?')}. Equipa para mejorar tus stats en combate."
        elif self.categoriaActual == 'runas':
            return f"Runa de rareza {item.get('rareza', '?')}. Aplica sus efectos al equiparla."
        return ''

    def confirmarSeleccion(self, instance):
        if self.gm is None or self.itemSeleccionado is None:
            self._mostrarPopup('Sin selección', 'Elige un item antes de equipar.', (0.7, 0.3, 0.1, 1))
            return

        if self.categoriaActual == 'objetos':
            self._usarObjeto(self.itemSeleccionado)
            return

        inv_id = self.itemSeleccionado.get('inv_id')
        if inv_id is None:
            return

        if self.categoriaActual == 'personajes':
            self.gm.cambiar_personaje_activo(inv_id)
            nombre_display = self.itemSeleccionado.get('nombre_display') or self.itemSeleccionado.get('nombre', '?')
            self._mostrarPopup('Personaje activo',
                               f"{nombre_display} es ahora tu personaje activo.",
                               (0.2, 0.8, 0.3, 1))

        elif self.categoriaActual == 'armas':
            resultado = self.gm.equipar_arma(inv_id)
            color = (0.2, 0.8, 0.3, 1) if resultado.get('ok') else (0.7, 0.1, 0.1, 1)
            self._mostrarPopup('Arma', resultado.get('mensaje', ''), color)

        elif self.categoriaActual == 'runas':
            self._popupSlotRuna(inv_id)

        self._cargarItems(self.categoriaActual)

    def _popupSlotRuna(self, inv_id: int):
        """Pregunta al jugador en qué slot equipar la runa.
        Cada opción muestra la imagen SLOT_RUNA_VACIO con el texto encima."""
        modal = ModalView(size_hint=(0.7, 0.42), background_color=(0, 0, 0, 0))

        cont = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(12))
        with cont.canvas.before:
            Color(0.05, 0.05, 0.1, 0.97)
            rect = RoundedRectangle(pos=cont.pos, size=cont.size, radius=[dp(16)])
        cont.bind(
            pos=lambda *a: setattr(rect, 'pos', cont.pos),
            size=lambda *a: setattr(rect, 'size', cont.size)
        )

        lbl = Label(
            text='¿En qué slot quieres equipar la runa?',
            font_size=dp(14), bold=True, color=BLANCO,
            size_hint=(1, None), height=dp(30),
            halign='center', valign='middle'
        )
        lbl.bind(size=lbl.setter('text_size'))
        cont.add_widget(lbl)

        botones = BoxLayout(orientation='horizontal', size_hint=(1, 1), spacing=dp(16))

        def _hacer_slot_btn(texto_slot):
            fl = FloatLayout(size_hint=(1, 1))
            img = Image(
                source=SLOT_RUNA_VACIO,
                allow_stretch=True,
                keep_ratio=True,
                mipmap=True,
                size_hint=(1, 1),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
            )
            lbl_slot = Label(
                text=texto_slot,
                font_size=dp(13), bold=True, color=BLANCO,
                size_hint=(1, 1),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                halign='center', valign='middle',
            )
            lbl_slot.bind(size=lbl_slot.setter('text_size'))
            btn = Button(
                background_normal='',
                background_color=(0, 0, 0, 0),
                size_hint=(1, 1),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
            )
            fl.add_widget(img)
            fl.add_widget(lbl_slot)
            fl.add_widget(btn)
            return fl, btn

        fl1, btn1 = _hacer_slot_btn('SLOT 1')
        fl2, btn2 = _hacer_slot_btn('SLOT 2')

        def _equipar(slot):
            res = self.gm.equipar_runa(inv_id, slot)
            modal.dismiss()
            color = (0.2, 0.8, 0.3, 1) if res.get('ok') else (0.7, 0.1, 0.1, 1)
            self._mostrarPopup('Runa', res.get('mensaje', ''), color)
            self._cargarItems(self.categoriaActual)

        btn1.bind(on_press=lambda _: _equipar(1))
        btn2.bind(on_press=lambda _: _equipar(2))

        botones.add_widget(fl1)
        botones.add_widget(fl2)
        cont.add_widget(botones)
        modal.add_widget(cont)
        modal.open()

    def _usarObjeto(self, objeto: dict):
        tipo = objeto.get('tipo_objeto', '')

        if tipo == 'pocion':
            ok = self.gm.usar_pocion()
            if ok:
                self._mostrarPopup('Poción usada',
                                   'Has restaurado tu vida al máximo.',
                                   (0.2, 0.8, 0.3, 1))
                self._cargarItems('objetos')
            else:
                self._mostrarPopup('Sin pociones',
                                   'No tienes pociones disponibles.',
                                   (0.7, 0.1, 0.1, 1))

        elif tipo == 'transmutador':
            self._mostrarPopup('Transmutador',
                               'Usa este objeto en la Forja para combinar runas.',
                               (0.7, 0.5, 0.1, 1))

        elif tipo in ('fragmento_rojo', 'fragmento_azul'):
            self._mostrarPopup('Fragmento',
                               'Usa este objeto en la Tienda al acumular suficientes.',
                               (0.7, 0.5, 0.1, 1))
        else:
            self._mostrarPopup('Objeto', 'Este objeto no tiene uso directo.', (0.7, 0.3, 0.1, 1))

    def _mostrarPopup(self, titulo, mensaje, color_titulo):
        modal = ModalView(size_hint=(0.8, 0.4), auto_dismiss=True, background_color=(0, 0, 0, 0))

        cont = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(12))
        with cont.canvas.before:
            Color(0.05, 0.05, 0.1, 0.97)
            rect = RoundedRectangle(pos=cont.pos, size=cont.size, radius=[dp(16)])
        cont.bind(
            pos=lambda *a: setattr(rect, 'pos', cont.pos),
            size=lambda *a: setattr(rect, 'size', cont.size)
        )

        lbl_titulo = Label(
            text=titulo, font_size=dp(18), bold=True, color=color_titulo,
            size_hint=(1, None), height=dp(36), halign='center', valign='middle'
        )
        lbl_titulo.bind(size=lbl_titulo.setter('text_size'))

        lbl_msg = Label(
            text=mensaje, font_size=dp(12), color=BLANCO,
            size_hint=(1, 1), halign='center', valign='middle'
        )
        lbl_msg.bind(size=lbl_msg.setter('text_size'))

        btn = Button(
            text='OK', background_normal='',
            background_color=COLOR_GUARDIANES, color=BLANCO,
            font_size=dp(13), bold=True,
            size_hint=(1, None), height=dp(40)
        )
        btn.bind(on_press=lambda _: modal.dismiss())

        cont.add_widget(lbl_titulo)
        cont.add_widget(lbl_msg)
        cont.add_widget(btn)
        modal.add_widget(cont)
        modal.open()

    def _actualizarFondo(self, *args):
        self._bg_rect.pos  = self.pos
        self._bg_rect.size = self.size

    def volverAHome(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'principal'

    def irAForja(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'forja'