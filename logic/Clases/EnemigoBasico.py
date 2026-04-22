from logic.Clases.Enemigo import Enemigo


class EnemigoBasico(Enemigo):
    """
    Enemigo estándar de nodos normales. Hereda de Enemigo.
    contador_danio : 3
    Sin mecánicas especiales; la lógica de combate la gestiona Encuentro.
    """

    CONTADOR_DANIO = 3

    def __init__(self, nombre, atk, vida, defensa):
        super().__init__(
            nombre=nombre,
            atk=atk,
            vida=vida,
            defensa=defensa,
            contador_danio=self.CONTADOR_DANIO,
        )