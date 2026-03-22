import random


class Jugador:
    """
    Clase padre de todos los personajes jugables.

    Stats compartidos:
        atk            — Daño base. Se compara con la defensa del enemigo.
        vida           — Puntos de vida. Se reduce al recibir golpes.
        defensa        — Se compara con el ataque del enemigo.
        destreza       — Usada activamente por el Asesino; presente en todos.
        magia          — Sube el ATK del Mago. En Guerrero y Asesino es 0.
        contador_danio — Golpes que puede aguantar antes de ser derrotado.
    """

    def __init__(self, nombre, atk, vida, defensa, destreza, magia, contador_danio):
        self.nombre = nombre
        self.atk = atk
        self.vida = vida
        self.vida_max = vida
        self.defensa = defensa
        self.destreza = destreza
        self.magia = magia
        self.contador_danio = contador_danio
        self.runa_1 = None #slot de runa 1 (vacio al inicio)
        self.runa_2 = None #slot de runa 2 (vacio al inicio)
        self.arma = None #slot de arma (vacio al inicio)

    _STAT_MAP = {
        "atk": "atk",
        "defensa": "defensa",
        "magia": "magia",
        "destreza": "destreza",
        "vida": "vida",
    }
    def esta_vivo(self):
        return self.contador_danio > 0
#======================== Sección armas =======================================
    def equip_arma(self, arma: dict):
        """
        Equipa un arma en el slot único de arma.
        Si ya había un arma equipada, la desequipa primero.
        Las armas S solo pueden equiparlas su clase específica
        (detectado por la clave '_clase' en el diccionario).

        Ejemplo:
            from Clases.stat import ARMA_MANDOBLE, ARMA_S_GUERRERO
            guerrero.equip_arma(ARMA_MANDOBLE)    # básica, cualquier clase
            guerrero.equip_arma(ARMA_S_GUERRERO)  # S, solo Guerrero
        """
        #Validar restricción de clase en armas S
        clase_requerida = arma.get("_clase")
        if clase_requerida is not None:
            if self.__class__.__name__ != clase_requerida:
                raise ValueError(
                    f"El arma es exclusiva de la clase {clase_requerida}. "
                    f"{self.__class__.__name__} no puede equiparla."
                )

        #Desequipa el arma actual si la hay
        if self.arma is not None:
            self._aplicar_arma(self.arma, signo=-1)

        #Equipa la nueva
        self._aplicar_arma(arma, signo=+1)
        self.arma = arma

    def desequip_arma(self):
        """
        Desequipa el arma actual restando sus bonus.
        Si no hay arma equipada no hace nada.
        """
        if self.arma is None:
            return
        self._aplicar_arma(self.arma, signo=-1)
        self.arma = None

    def _aplicar_arma(self, arma, signo):
        """Suma o resta los stats de un arma ignorando la clave '_clase'."""
        for clave, valor in arma.items():
            if clave == "_clase":
                continue
            if clave not in self._STAT_MAP:
                raise ValueError(f"Stat desconocido en arma: '{clave}'")
            attr = self._STAT_MAP[clave]
            setattr(self, attr, getattr(self, attr) + signo * valor)
            if attr == "vida":
                self.vida_max += signo * valor
# ========================= Fin sección armas ========================================
# =========================== Sección runas ===========================================
    def _aplicar_runa(self, runa, signo):
        """Suma (signo=+1) o resta (signo=-1) los bonus de una runa."""
        for clave, valor in runa.items():
            if clave not in self._STAT_MAP:
                raise ValueError(f"Stat desconocido en runa: '{clave}'")
            attr = self._STAT_MAP[clave]
            setattr(self, attr, getattr(self, attr) + signo * valor)
            if attr == "vida":
                self.vida_max += signo * valor

    def equip_runa(self, runa: dict, slot: int):
        """
        Equipa una runa en el slot indicado (1 o 2).
        Si el slot ya tenía una runa, la desequipa primero (restando sus bonus).
        Una misma runa no puede estar en los dos slots a la vez.

        Ejemplo:
            from Clases.stat import RUNA_ATAQUE, RUNA_DEFENSA
            guerrero.equip_runa(RUNA_ATAQUE,  slot=1)
            guerrero.equip_runa(RUNA_DEFENSA, slot=2)
            guerrero.equip_runa(RUNA_MAGIA,   slot=1) #sustituye RUNA_ATAQUE
        """
        if slot not in (1, 2):
            raise ValueError("El slot debe ser 1 o 2.")

        otro_slot = self.runa_2 if slot == 1 else self.runa_1

        if otro_slot is not None and otro_slot == runa:
            raise ValueError("Esa runa ya está equipada en el otro slot.")

        #Desequipa la runa actual del slot si la hay
        actual = self.runa_1 if slot == 1 else self.runa_2
        if actual is not None:
            self._aplicar_runa(actual, signo=-1)

        #Equipa la nueva runa
        self._aplicar_runa(runa, signo=+1)

        if slot == 1:
            self.runa_1 = runa
        else:
            self.runa_2 = runa

    def desequip_runa(self, slot: int):
        """
        Desequipa la runa del slot indicado (1 o 2), restando sus bonus.
        Si el slot está vacío no hace nada.
        """
        if slot not in (1, 2):
            raise ValueError("El slot debe ser 1 o 2.")

        actual = self.runa_1 if slot == 1 else self.runa_2
        if actual is None:
            return

        self._aplicar_runa(actual, signo=-1)

        if slot == 1:
            self.runa_1 = None
        else:
            self.runa_2 = None
# =================== Fin sección runas ==================================
    def perder_vida_por_golpe(self):
        """
        Pérdida de vida por defecto: entre el 20% y el 40% de vida_max.
        El Guerrero sobreescribe este método (25% fijo).
        Devuelve la cantidad perdida.
        """
        porcentaje = random.uniform(0.20, 0.40)
        perdida = round(self.vida_max * porcentaje)
        self.vida = max(0, self.vida - perdida)
        return perdida

    def __str__(self):
        return (f"{self.nombre} ({self.__class__.__name__}) | "
                f"ATK:{self.atk}  VID:{self.vida}/{self.vida_max}  "
                f"DEF:{self.defensa}  DES:{self.destreza}  MAG:{self.magia}  "
                f"[Contadores: {self.contador_danio}]")