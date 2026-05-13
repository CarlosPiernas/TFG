from logic.Clases.Jugador import Jugador


class Guerrero(Jugador):
    """
    Tanque físico. Hereda de Jugador.

    Diferencias respecto al padre:
    contador_danio : 5  (el más resistente)
    Pierde SIEMPRE el 20% de vida_max al recibir un golpe (no aleatorio)
    magia    : 0
    destreza : 0
    Berserker: cuando le quedan 2 o menos contadores, su ATK efectivo sube +50.
    """

    CONTADOR_DANIO  = 5
    BONUS_BERSERKER = 50

    def __init__(self, nombre, atk, vida, defensa):
        super().__init__(
            nombre=nombre,
            atk=atk,
            vida=vida,
            defensa=defensa,
            destreza=0,
            magia=0,
            contador_danio=self.CONTADOR_DANIO,
        )

    @property
    def atk_efectivo(self):
        """ATK real del Guerrero: base normal, o base +50 si quedan 2 o menos contadores."""
        if self.contador_danio <= 2:
            return self.atk + self.BONUS_BERSERKER
        return self.atk

    @property
    def berserker_activo(self):
        """True cuando el modo berserker está activo (2 o menos contadores)."""
        return self.contador_danio <= 2

    def perder_vida_por_golpe(self):
        """El Guerrero siempre pierde exactamente el 20% de vida_max."""
        perdida = round(self.vida_max * 0.20)
        self.vida = max(0, self.vida - perdida)
        return perdida