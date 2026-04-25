from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
 
from screens.faction_screen   import PantallaSeleccion
from screens.home_screen      import PantallaPrincipal
from screens.inventory_screen import PantallaInventario
from screens.gacha_screen     import PantallaGacha
from screens.map_screen       import PantallaMapa
from screens.combat_screen    import PantallaCombate
from screens.forja_screen import PantallaForja
 
Window.size = (400, 800)
 
 
class JuegoApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PantallaSeleccion(name='seleccion'))
        sm.add_widget(PantallaPrincipal(name='principal'))
        sm.add_widget(PantallaInventario(name='inventario'))
        sm.add_widget(PantallaGacha(name='gacha'))
        sm.add_widget(PantallaMapa(name='mapa'))
        sm.add_widget(PantallaForja(name='forja'))
        sm.add_widget(PantallaCombate(name='combate'))
 
        return sm
 
 
if __name__ == '__main__':
    JuegoApp().run()