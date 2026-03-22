import random
from logic.Clases.Jugador import Jugador


class Asesino(Jugador):
    """
    DPS impredecible basado en la suerte. Hereda de Jugador.

    Diferencias respecto al padre:
      contador_danio : 3
      magia          : 0
      ATK efectivo   : atk + destreza // 2  (la destreza potencia el ataque)
        Ej: atk=110, destreza=51 → ATK efectivo = 110 + 25 = 135
      Pasiva de suerte: antes de su turno lanza un número aleatorio
        entre 0 y su destreza. Si saca >= 40 (con destreza > 40),
        el enemigo pierde 1 contador extra.
        Con destreza 50 (base) → ~21% | destreza 75 → ~48% | destreza 100 => ~61%
    """

    CONTADOR_DANIO = 3

    def __init__(self, nombre, atk, vida, defensa, destreza):
        super().__init__(
            nombre=nombre,
            atk=atk,
            vida=vida,
            defensa=defensa,
            destreza=destreza,
            magia=0,
            contador_danio=self.CONTADOR_DANIO,
        )

    @property
    def atk_efectivo(self):
        """ATK real del Asesino: base + destreza // 2 (redondeado hacia abajo)."""
        return self.atk + self.destreza // 2

    def lanzar_suerte(self):
        """
        Lanza un número aleatorio entre 0 y destreza (inclusive).
        La suerte se activa si el resultado >= 40 (con destreza > 40).

        Con destreza 50 (base): rango 0-50,  activa si >=40 => ~21%.
        Con destreza 75:        rango 0-75,  activa si >=40 => ~48%.
        Con destreza 100:       rango 0-100, activa si >=40 => ~61%.
        """
        if self.destreza <= 0:
            return 0, False
        resultado = random.randint(0, self.destreza)
        tuvo_suerte = resultado >= 40 if self.destreza > 40 else resultado > 40
        return resultado, tuvo_suerte