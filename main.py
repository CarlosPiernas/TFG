from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from screens.faction_screen   import PantallaSeleccion
from screens.home_screen      import PantallaPrincipal
from screens.inventory_screen import PantallaInventario
from screens.gacha_screen     import PantallaGacha
from screens.map_screen       import PantallaMapa
from screens.combat_screen    import PantallaCombate
from screens.forja_screen     import PantallaForja
from firebase.game_manager    import GameManager

Window.size = (400, 800)


class JuegoApp(App):
    def build(self):
        self.gm = GameManager()  # instancia única para toda la app

        sm = ScreenManager()
        sm.add_widget(PantallaSeleccion(name='seleccion',  gm=self.gm))
        sm.add_widget(PantallaPrincipal(name='principal',  gm=self.gm))
        sm.add_widget(PantallaInventario(name='inventario', gm=self.gm))
        sm.add_widget(PantallaGacha(name='gacha',          gm=self.gm))
        sm.add_widget(PantallaMapa(name='mapa',            gm=self.gm))
        sm.add_widget(PantallaForja(name='forja',          gm=self.gm))
        sm.add_widget(PantallaCombate(name='combate',      gm=self.gm))

        return sm


if __name__ == '__main__':
    JuegoApp().run()