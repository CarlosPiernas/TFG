import random


class Enemigo:
    """
    Clase padre de todos los enemigos.

    Stats:
        atk            — Ataque. Se compara con la defensa del jugador.
        vida           — Puntos de vida. Se reduce al recibir golpes.
        defensa        — Se compara con el ataque del jugador.
        contador_danio — Golpes que puede aguantar. Lo define cada subclase.
    """

    def __init__(self, nombre, atk, vida, defensa, contador_danio):
        self.nombre = nombre
        self.atk = atk
        self.vida = vida
        self.vida_max = vida
        self.defensa = defensa
        self.contador_danio = contador_danio

    def esta_vivo(self):
        return self.contador_danio > 0

    def perder_vida_por_golpe(self):
        """
        Pierde entre el 20% y el 40% de vida_max al recibir un golpe.
        Devuelve la cantidad perdida.
        """
        porcentaje = random.uniform(0.20, 0.40)
        perdida = round(self.vida_max * porcentaje)
        self.vida = max(0, self.vida - perdida)
        return perdida

    def __str__(self):
        return (f"{self.nombre} ({self.__class__.__name__}) | "
                f"ATK:{self.atk}  VID:{self.vida}/{self.vida_max}  "
                f"DEF:{self.defensa}  [Contadores: {self.contador_danio}]")