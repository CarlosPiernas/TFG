from logic.Clases.Jugador import Jugador


class Mago(Jugador):
    """
    DPS mágico de alto riesgo. Hereda de Jugador.

    Diferencias respecto al padre:
    contador_danio : 3
    ATK efectivo   : atk + magia  (la magia potencia el ataque)
    Pasiva         : la PRIMERA vez que va a perder un contador de daño,
                         también le quita 1 contador al enemigo.
                         Solo ocurre una vez por combate.
    destreza : 0 al inicio
    """

    CONTADOR_DANIO = 3

    def __init__(self, nombre, atk, vida, defensa, magia):
        super().__init__(
            nombre=nombre,
            atk=atk,
            vida=vida,
            defensa=defensa,
            destreza=0,
            magia=magia,
            contador_danio=self.CONTADOR_DANIO,
        )
        self._pasiva_usada = False

    @property
    def atk_efectivo(self):
        """ATK real del Mago: base + magia."""
        return self.atk + self.magia

    def resetear_pasiva(self):
        """Llamar al inicio de cada nuevo combate para reiniciar la pasiva."""
        self._pasiva_usada = False

    def intentar_pasiva(self):
        """
        Intenta activar la pasiva de contraataque.
        Devuelve True la primera vez (y marca como usada).
        Devuelve False si ya se usó.
        """
        if not self._pasiva_usada:
            self._pasiva_usada = True
            return True
        return False