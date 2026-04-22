import random
from logic.Clases.Enemigo import Enemigo


class EnemigoJefe(Enemigo):
    """
    Enemigo boss de nodos especiales. Hereda de Enemigo.

    contador_danio    : 4
    Mecánica de salvación: cuando va a quitar el ÚLTIMO contador al jugador,
        se lanza un número del 1 al 100. Si es > 70, el jugador no pierde ese
        contador. Solo ocurre una vez por combate.
    """

    CONTADOR_DANIO = 4
    UMBRAL_SALVACION = 70

    def __init__(self, nombre, atk, vida, defensa):
        super().__init__(
            nombre=nombre,
            atk=atk,
            vida=vida,
            defensa=defensa,
            contador_danio=self.CONTADOR_DANIO,
        )
        self._salvacion_usada = False

    def salvacion_disponible(self):
        """True si la salvación aún no se ha usado en este combate."""
        return not self._salvacion_usada

    def intentar_salvacion(self):
        """
        Lanza 1-100. Si > 70 y es la primera vez, el jugador se salva.
        Devuelve (lanzamiento, salvado).
        Marca la salvación como usada independientemente del resultado.
        """
        if self._salvacion_usada:
            return 0, False
        self._salvacion_usada = True
        lanzamiento = random.randint(1, 100)
        salvado = lanzamiento > self.UMBRAL_SALVACION
        return lanzamiento, salvado

    def resetear_salvacion(self):
        """Llamar al inicio de cada nuevo combate."""
        self._salvacion_usada = False