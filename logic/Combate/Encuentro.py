from logic.Clases.Jugador import Jugador
from logic.Clases.Mago import Mago
from logic.Clases.Asesino import Asesino
from logic.Clases.Guerrero import Guerrero
from logic.Clases.Enemigo import Enemigo
from logic.Clases.EnemigoBasico import EnemigoBasico
from logic.Clases.EnemigoJefe import EnemigoJefe


class Encuentro:
    """
    Gestiona un combate 1vs1 entre un Jugador y un Enemigo.

    Modo completo (tests / M2):
        enc = Encuentro()
        log = enc.iniciar(jugador, enemigo)

    Modo paso a paso (pantalla de combate):
        enc = Encuentro()
        enc.preparar(jugador, enemigo)
        while not enc.terminado:
            r = enc.turno_paso()
            # r['lineas']       → líneas de log simplificadas para la UI
            # r['terminado']    → bool
            # r['victoria']     → bool
            # r['turno']        → int
            # r['vida_jugador'] → int
            # r['vida_max_j']   → int
            # r['vida_enemigo'] → int
            # r['vida_max_e']   → int
            # r['berserker']    → bool
    """

    # ─────────────────────────────────────────────────────
    # MODO PASO A PASO
    # ─────────────────────────────────────────────────────

    def preparar(self, jugador, enemigo):
        self.jugador   = jugador
        self.enemigo   = enemigo
        self.turno     = 1
        self.terminado = False
        self.victoria  = False
        self._preparar_combate(jugador, enemigo)

    def turno_paso(self):
        lineas = []

        if self.terminado:
            return self._estado(lineas)

        jugador = self.jugador
        enemigo = self.enemigo
        es_jefe = isinstance(enemigo, EnemigoJefe)

        lineas.append(f"— Turno {self.turno} —")

        # ── Pasiva Asesino ──────────────────────────────────────────────────
        if isinstance(jugador, Asesino):
            resultado, suerte = jugador.lanzar_suerte()
            if suerte:
                lineas.append(f"🎲 {jugador.nombre} activa su SUERTE")
                if enemigo.esta_vivo():
                    enemigo.contador_danio = max(0, enemigo.contador_danio - 1)
                    self._aplicar_muerte_si_procede(enemigo)

        if not self._vivo(enemigo):
            self._cerrar_combate(lineas)
            return self._estado(lineas)

        atk_jugador = jugador.atk_efectivo if isinstance(jugador, (Mago, Asesino, Guerrero)) else jugador.atk

        jugador_golpea = atk_jugador > enemigo.defensa
        enemigo_golpea = enemigo.atk > jugador.defensa
        empate_j       = atk_jugador == enemigo.defensa
        empate_e       = enemigo.atk == jugador.defensa

        degrade = 20 if es_jefe else 10

        # ── Jugador golpea al enemigo ────────────────────────────────────────
        if jugador_golpea:
            enemigo.perder_vida_por_golpe()
            enemigo.contador_danio -= 1
            jugador.atk     = max(0, jugador.atk    - degrade)
            jugador.defensa = max(0, jugador.defensa - degrade)
            lineas.append(f"⚔️ {jugador.nombre} ¡ATACA!")
            self._aplicar_muerte_si_procede(enemigo)

        elif empate_j:
            if isinstance(jugador, Mago):
                self._aplicar_pasiva_mago(jugador, enemigo, lineas)
            jugador.contador_danio -= 1
            enemigo.contador_danio -= 1
            lineas.append(f"⚖️ Empate de fuerzas")
            self._aplicar_muerte_si_procede(jugador)
            self._aplicar_muerte_si_procede(enemigo)

        # Si alguien murió tras el ataque del jugador, cerramos
        if not self._vivo(enemigo) or not self._vivo(jugador):
            self._cerrar_combate(lineas)
            return self._estado(lineas)

        # ── Enemigo / Jefe golpea al jugador ────────────────────────────────
        if enemigo_golpea:
            if es_jefe:
                contadores_a_perder = 2
                if jugador.contador_danio <= contadores_a_perder and enemigo.salvacion_disponible():
                    lanzamiento, salvado = enemigo.intentar_salvacion()
                    if salvado:
                        lineas.append(f"✨ ¡{jugador.nombre} se salva del golpe definitivo!")
                        enemigo.atk     = max(0, enemigo.atk    - degrade)
                        enemigo.defensa = max(0, enemigo.defensa - degrade)
                        self.turno += 1
                        return self._estado(lineas)

                if isinstance(jugador, Mago):
                    self._aplicar_pasiva_mago(jugador, enemigo, lineas)

                jugador.perder_vida_por_golpe()
                jugador.contador_danio = max(0, jugador.contador_danio - contadores_a_perder)
                enemigo.atk     = max(0, enemigo.atk    - degrade)
                enemigo.defensa = max(0, enemigo.defensa - degrade)
                lineas.append(f"💥 {jugador.nombre} ¡Recibe un golpe!")
                self._aplicar_muerte_si_procede(jugador)

            else:
                if isinstance(jugador, Mago):
                    self._aplicar_pasiva_mago(jugador, enemigo, lineas)

                jugador.perder_vida_por_golpe()
                jugador.contador_danio -= 1
                enemigo.atk     = max(0, enemigo.atk    - degrade)
                enemigo.defensa = max(0, enemigo.defensa - degrade)
                lineas.append(f"💥 {jugador.nombre} ¡Recibe un golpe!")
                self._aplicar_muerte_si_procede(jugador)

        elif empate_e and not jugador_golpea and not empate_j:
            if isinstance(jugador, Mago):
                self._aplicar_pasiva_mago(jugador, enemigo, lineas)
            jugador.contador_danio -= 1
            enemigo.contador_danio -= 1
            lineas.append(f"⚖️ Empate de fuerzas")
            self._aplicar_muerte_si_procede(jugador)
            self._aplicar_muerte_si_procede(enemigo)

        # Comprobar fin tras ataque del enemigo
        if not self._vivo(jugador) or not self._vivo(enemigo):
            self._cerrar_combate(lineas)
        else:
            self.turno += 1

        return self._estado(lineas)

    # ─────────────────────────────────────────────────────
    # HELPERS MODO PASO A PASO
    # ─────────────────────────────────────────────────────

    def _vivo(self, entidad) -> bool:
        """
        Una entidad está viva si tiene vida > 0 Y contadores > 0.
        Si cualquiera de los dos llega a 0, está muerta.
        """
        return entidad.vida > 0 and entidad.contador_danio > 0

    def _aplicar_muerte_si_procede(self, entidad):
        """
        Si los contadores llegan a 0 → vida a 0.
        Si la vida llega a 0 → contadores a 0.
        Así ambas condiciones se sincronizan y _vivo() devuelve False.
        """
        if entidad.contador_danio <= 0:
            entidad.vida = 0
        if entidad.vida <= 0:
            entidad.contador_danio = 0

    def _cerrar_combate(self, lineas):
        self.terminado = True
        self.victoria  = self._vivo(self.jugador)
        if self.victoria:
            lineas.append(f"🏆 ¡VICTORIA!")
        else:
            lineas.append(f"💀 DERROTA")

    def _estado(self, lineas):
        berserker = (
            isinstance(self.jugador, Guerrero) and self.jugador.berserker_activo
            if hasattr(self, 'jugador') else False
        )
        jugador = self.jugador if hasattr(self, 'jugador') else None
        enemigo = self.enemigo if hasattr(self, 'enemigo') else None
        return {
            'lineas'       : lineas,
            'terminado'    : self.terminado,
            'victoria'     : self.victoria,
            'turno'        : self.turno,
            'vida_jugador' : jugador.vida     if jugador else 0,
            'vida_max_j'   : jugador.vida_max if jugador else 1,
            'vida_enemigo' : enemigo.vida     if enemigo else 0,
            'vida_max_e'   : enemigo.vida_max if enemigo else 1,
            'berserker'    : berserker,
        }

    def _aplicar_pasiva_mago(self, mago, enemigo, lineas):
        if mago.intentar_pasiva():
            enemigo.contador_danio = max(0, enemigo.contador_danio - 1)
            lineas.append(f"🔥 Pasiva del Mago — {enemigo.nombre} pierde 1 contador extra")
            self._aplicar_muerte_si_procede(enemigo)

    # ─────────────────────────────────────────────────────
    # MODO COMPLETO (para tests, sin cambios)
    # ─────────────────────────────────────────────────────

    def iniciar(self, jugador, enemigo):
        self._preparar_combate(jugador, enemigo)
        log = []
        log.append(f"⚔️  INICIO DEL COMBATE: {jugador.nombre} vs {enemigo.nombre}")
        log.append(str(jugador))
        log.append(str(enemigo))
        log.append("─" * 55)
        if isinstance(enemigo, EnemigoJefe):
            self._combate_jefe(jugador, enemigo, log)
        else:
            self._combate_basico(jugador, enemigo, log)
        log.append("─" * 55)
        if jugador.esta_vivo():
            log.append(f"🏆  VICTORIA — {jugador.nombre} ha derrotado a {enemigo.nombre}.")
        else:
            log.append(f"💀  DERROTA  — {jugador.nombre} ha sido derrotado por {enemigo.nombre}.")
        return log

    def _combate_basico(self, jugador, enemigo, log):
        turno = 1
        while jugador.esta_vivo() and enemigo.esta_vivo():
            log.append(f"\n  TURNO {turno}")
            if isinstance(jugador, Asesino):
                resultado, suerte = jugador.lanzar_suerte()
                if suerte:
                    log.append(f"  🎲 {jugador.nombre} saca {resultado} "
                               f"(rango 0-{jugador.destreza}, necesita >40) — "
                               f"\"¡Voy a tener suerte!\"")
                    if enemigo.esta_vivo():
                        enemigo.contador_danio = max(0, enemigo.contador_danio - 1)
                        log.append(f"  ⚡ SUERTE — {enemigo.nombre} pierde 1 contador extra "
                                   f"→ [{enemigo.contador_danio}].")
                        self._aplicar_muerte_completo(enemigo, log)
                else:
                    log.append(f"  🎲 {jugador.nombre} lanza suerte: {resultado} "
                               f"(rango 0-{jugador.destreza}, necesita >40)")
            if not enemigo.esta_vivo():
                break
            atk_jugador = jugador.atk_efectivo if isinstance(jugador, (Mago, Asesino, Guerrero)) else jugador.atk
            if isinstance(jugador, Guerrero) and jugador.berserker_activo:
                log.append(f"  💪 ¡BERSERKER! {jugador.nombre} tiene 1 contador — ATK sube a {atk_jugador}.")
            log.append(f"  ATK jugador: {atk_jugador}  |  DEF enemigo: {enemigo.defensa}")
            log.append(f"  ATK enemigo: {enemigo.atk}  |  DEF jugador: {jugador.defensa}")
            jugador_golpea = atk_jugador > enemigo.defensa
            enemigo_golpea = enemigo.atk > jugador.defensa
            empate_j = atk_jugador == enemigo.defensa
            empate_e = enemigo.atk == jugador.defensa
            if jugador_golpea:
                vida_perdida = enemigo.perder_vida_por_golpe()
                enemigo.contador_danio -= 1
                jugador.atk = max(0, jugador.atk - 10)
                jugador.defensa = max(0, jugador.defensa - 10)
                log.append(f"  ✅ {jugador.nombre} golpea a {enemigo.nombre}.")
                log.append(f"     {enemigo.nombre} pierde {vida_perdida} de vida "
                           f"({enemigo.vida}/{enemigo.vida_max}) "
                           f"y 1 contador → [{enemigo.contador_danio}].")
                log.append(f"     {jugador.nombre} pierde 10 ATK y 10 DEF "
                           f"→ ATK:{jugador.atk} DEF:{jugador.defensa}.")
                self._aplicar_muerte_completo(enemigo, log)
            elif empate_j:
                log.append(f"  ⚖️  EMPATE — {jugador.nombre} y {enemigo.nombre} igualan fuerzas.")
                if isinstance(jugador, Mago):
                    self._aplicar_pasiva_mago_completo(jugador, enemigo, log)
                jugador.contador_danio -= 1
                enemigo.contador_danio -= 1
                self._aplicar_muerte_completo(jugador, log)
                self._aplicar_muerte_completo(enemigo, log)
            if not enemigo.esta_vivo() or not jugador.esta_vivo():
                log.append(f"  📊 {jugador.nombre}: contadores={jugador.contador_danio}  "
                           f"vida={jugador.vida}/{jugador.vida_max}")
                log.append(f"  📊 {enemigo.nombre}: contadores={enemigo.contador_danio}  "
                           f"vida={enemigo.vida}/{enemigo.vida_max}")
                break
            if enemigo_golpea:
                vida_perdida_j = jugador.perder_vida_por_golpe()
                if isinstance(jugador, Mago):
                    self._aplicar_pasiva_mago_completo(jugador, enemigo, log)
                jugador.contador_danio -= 1
                enemigo.atk = max(0, enemigo.atk - 10)
                enemigo.defensa = max(0, enemigo.defensa - 10)
                log.append(f"  ❌ {enemigo.nombre} golpea a {jugador.nombre}.")
                log.append(f"     {jugador.nombre} pierde {vida_perdida_j} de vida "
                           f"({jugador.vida}/{jugador.vida_max}) "
                           f"y 1 contador → [{jugador.contador_danio}].")
                log.append(f"     {enemigo.nombre} pierde 10 ATK y 10 DEF "
                           f"→ ATK:{enemigo.atk} DEF:{enemigo.defensa}.")
                self._aplicar_muerte_completo(jugador, log)
            elif empate_e and not jugador_golpea and not empate_j:
                log.append(f"  ⚖️  EMPATE — {enemigo.nombre} y {jugador.nombre} igualan fuerzas.")
                if isinstance(jugador, Mago):
                    self._aplicar_pasiva_mago_completo(jugador, enemigo, log)
                jugador.contador_danio -= 1
                enemigo.contador_danio -= 1
                self._aplicar_muerte_completo(jugador, log)
                self._aplicar_muerte_completo(enemigo, log)
            log.append(f"  📊 {jugador.nombre}: contadores={jugador.contador_danio}  "
                       f"vida={jugador.vida}/{jugador.vida_max}")
            log.append(f"  📊 {enemigo.nombre}: contadores={enemigo.contador_danio}  "
                       f"vida={enemigo.vida}/{enemigo.vida_max}")
            turno += 1

    def _combate_jefe(self, jugador, enemigo, log):
        turno = 1
        while jugador.esta_vivo() and enemigo.esta_vivo():
            log.append(f"\n  TURNO {turno}")
            if isinstance(jugador, Asesino):
                resultado, suerte = jugador.lanzar_suerte()
                if suerte:
                    log.append(f"  🎲 {jugador.nombre} saca {resultado} "
                               f"(rango 0-{jugador.destreza}, necesita >=40) — "
                               f"\"¡Voy a tener suerte!\"")
                    if enemigo.esta_vivo():
                        enemigo.contador_danio = max(0, enemigo.contador_danio - 1)
                        log.append(f"  ⚡ SUERTE — {enemigo.nombre} pierde 1 contador extra "
                                   f"→ [{enemigo.contador_danio}].")
                        self._aplicar_muerte_completo(enemigo, log)
                else:
                    log.append(f"  🎲 {jugador.nombre} lanza suerte: {resultado} "
                               f"(rango 0-{jugador.destreza}, necesita >=40)")
            if not enemigo.esta_vivo():
                break
            atk_jugador = jugador.atk_efectivo if isinstance(jugador, (Mago, Asesino, Guerrero)) else jugador.atk
            if isinstance(jugador, Guerrero) and jugador.berserker_activo:
                log.append(f"  💪 ¡BERSERKER! {jugador.nombre} tiene 1 contador — ATK sube a {atk_jugador}.")
            log.append(f"  ATK jugador: {atk_jugador}  |  DEF jefe: {enemigo.defensa}")
            log.append(f"  ATK jefe: {enemigo.atk}      |  DEF jugador: {jugador.defensa}")
            jugador_golpea = atk_jugador > enemigo.defensa
            jefe_golpea    = enemigo.atk > jugador.defensa
            empate_j       = atk_jugador == enemigo.defensa
            empate_e       = enemigo.atk == jugador.defensa
            if jugador_golpea:
                enemigo.contador_danio -= 1
                jugador.atk = max(0, jugador.atk - 20)
                jugador.defensa = max(0, jugador.defensa - 20)
                log.append(f"  ✅ {jugador.nombre} golpea al jefe {enemigo.nombre}.")
                log.append(f"     {enemigo.nombre} pierde 1 contador → [{enemigo.contador_danio}].")
                log.append(f"     {jugador.nombre} pierde 20 ATK y 20 DEF "
                           f"→ ATK:{jugador.atk} DEF:{jugador.defensa}.")
                self._aplicar_muerte_completo(enemigo, log)
            elif empate_j:
                log.append(f"  ⚖️  EMPATE — {jugador.nombre} y {enemigo.nombre} igualan fuerzas.")
                if isinstance(jugador, Mago):
                    self._aplicar_pasiva_mago_completo(jugador, enemigo, log)
                jugador.contador_danio -= 1
                enemigo.contador_danio -= 1
                self._aplicar_muerte_completo(jugador, log)
                self._aplicar_muerte_completo(enemigo, log)
            if not enemigo.esta_vivo() or not jugador.esta_vivo():
                log.append(f"  🎫 {jugador.nombre}: contadores={jugador.contador_danio}  "
                           f"vida={jugador.vida}/{jugador.vida_max}")
                log.append(f"  🎫 {enemigo.nombre}: contadores={enemigo.contador_danio}  "
                           f"vida={enemigo.vida}/{enemigo.vida_max}")
                break
            if jefe_golpea:
                log.append(f"  ❌ {enemigo.nombre} ataca a {jugador.nombre}.")
                contadores_a_perder = 2
                if jugador.contador_danio <= contadores_a_perder and enemigo.salvacion_disponible():
                    lanzamiento, salvado = enemigo.intentar_salvacion()
                    log.append(f"  😨 ¡MOMENTO CRÍTICO! Lanzamiento de salvación: {lanzamiento}/100")
                    if salvado:
                        log.append(f"  ✨ ¡{jugador.nombre} se SALVA del golpe definitivo! (>{enemigo.UMBRAL_SALVACION})")
                        enemigo.atk = max(0, enemigo.atk - 20)
                        enemigo.defensa = max(0, enemigo.defensa - 20)
                        log.append(f"     {enemigo.nombre} pierde 20 ATK y 20 DEF "
                                   f"→ ATK:{enemigo.atk} DEF:{enemigo.defensa}.")
                        log.append(f"  🎫 {jugador.nombre}: contadores={jugador.contador_danio}  "
                                   f"vida={jugador.vida}/{jugador.vida_max}")
                        log.append(f"  🎫 {enemigo.nombre}: contadores={enemigo.contador_danio}  "
                                   f"vida={enemigo.vida}/{enemigo.vida_max}")
                        turno += 1
                        continue
                if isinstance(jugador, Mago):
                    self._aplicar_pasiva_mago_completo(jugador, enemigo, log)
                vida_perdida_j = jugador.perder_vida_por_golpe()
                jugador.contador_danio = max(0, jugador.contador_danio - contadores_a_perder)
                enemigo.atk = max(0, enemigo.atk - 20)
                enemigo.defensa = max(0, enemigo.defensa - 20)
                log.append(f"     {jugador.nombre} pierde {vida_perdida_j} de vida "
                           f"({jugador.vida}/{jugador.vida_max}) "
                           f"y {contadores_a_perder} contadores → [{jugador.contador_danio}].")
                log.append(f"     {enemigo.nombre} pierde 20 ATK y 20 DEF "
                           f"→ ATK:{enemigo.atk} DEF:{enemigo.defensa}.")
                self._aplicar_muerte_completo(jugador, log)
            elif empate_e and not jugador_golpea and not empate_j:
                log.append(f"  ⚖️  EMPATE — {enemigo.nombre} y {jugador.nombre} igualan fuerzas.")
                if isinstance(jugador, Mago):
                    self._aplicar_pasiva_mago_completo(jugador, enemigo, log)
                jugador.contador_danio -= 1
                enemigo.contador_danio -= 1
                self._aplicar_muerte_completo(jugador, log)
                self._aplicar_muerte_completo(enemigo, log)
            log.append(f"  🎫 {jugador.nombre}: contadores={jugador.contador_danio}  "
                       f"vida={jugador.vida}/{jugador.vida_max}")
            log.append(f"  🎫 {enemigo.nombre}: contadores={enemigo.contador_danio}  "
                       f"vida={enemigo.vida}/{enemigo.vida_max}")
            turno += 1

    # ─────────────────────────────────────────────────────
    # HELPERS COMPARTIDOS
    # ─────────────────────────────────────────────────────

    def _preparar_combate(self, jugador, enemigo):
        if isinstance(jugador, Mago):
            jugador.resetear_pasiva()
        if isinstance(enemigo, EnemigoJefe):
            enemigo.resetear_salvacion()

    def _aplicar_muerte_completo(self, entidad, log):
        """Versión con log para el modo iniciar()."""
        if entidad.contador_danio <= 0 and entidad.vida > 0:
            entidad.vida = 0
            log.append(f" 👻 {entidad.nombre} pierde toda la vida restante → 0.")
        if entidad.vida <= 0 and entidad.contador_danio > 0:
            entidad.contador_danio = 0

    def _aplicar_pasiva_mago_completo(self, mago, enemigo, log):
        if mago.intentar_pasiva():
            enemigo.contador_danio = max(0, enemigo.contador_danio - 1)
            log.append(f" 🔥  PASIVA MAGO — {mago.nombre} contraataca: "
                       f"{enemigo.nombre} pierde 1 contador extra "
                       f"→ [{enemigo.contador_danio}].")
            self._aplicar_muerte_completo(enemigo, log)


def imprimir_log(log):
    for linea in log:
        print(linea)