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

    Uso:
        enc = Encuentro()
        log = enc.iniciar(jugador, enemigo)

    Devuelve un log (lista de strings) con todo lo ocurrido turno a turno.
    M3 lo usa para reproducir la animación.
    """

    def iniciar(self, jugador, enemigo):
        """
        Detecta el tipo de enemigo y lanza el combate correspondiente.
        Devuelve el log completo.
        """
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

    # ────────────────
    # COMBATE BÁSICO
    # ────────────────

    def _combate_basico(self, jugador, enemigo, log):
        """
        Bucle contra EnemigoBasico. Cada turno se evalúan dos comparaciones
        independientes — ambas pueden ocurrir en el mismo turno:

          ATK jugador > DEF enemigo → enemigo pierde 1 contador + vida
                                      jugador pierde 10 ATK y 10 DEF
          ATK enemigo > DEF jugador → jugador pierde 1 contador + vida
                                      enemigo pierde 10 ATK y 10 DEF
          Empate en algún lado      → ese lado pierde 1 contador
        """
        turno = 1

        while jugador.esta_vivo() and enemigo.esta_vivo():
            log.append(f"\n  TURNO {turno}")

            # Pasiva del Asesino: lanzamiento de suerte
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
                        self._aplicar_muerte_si_procede(enemigo, log)
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

            # ── Jugador golpea al enemigo ──
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
                self._aplicar_muerte_si_procede(enemigo, log)

            # ── Empate jugador ──
            elif empate_j:
                log.append(f"  ⚖️  EMPATE — {jugador.nombre} y {enemigo.nombre} igualan fuerzas.")
                if isinstance(jugador, Mago):
                    self._aplicar_pasiva_mago(jugador, enemigo, log)
                jugador.contador_danio -= 1
                enemigo.contador_danio -= 1
                self._aplicar_muerte_si_procede(jugador, log)
                self._aplicar_muerte_si_procede(enemigo, log)

            if not enemigo.esta_vivo() or not jugador.esta_vivo():
                log.append(f"  📊 {jugador.nombre}: contadores={jugador.contador_danio}  "
                           f"vida={jugador.vida}/{jugador.vida_max}")
                log.append(f"  📊 {enemigo.nombre}: contadores={enemigo.contador_danio}  "
                           f"vida={enemigo.vida}/{enemigo.vida_max}")
                break

            # ── Enemigo golpea al jugador ──
            if enemigo_golpea:
                vida_perdida_j = jugador.perder_vida_por_golpe()
                if isinstance(jugador, Mago):
                    self._aplicar_pasiva_mago(jugador, enemigo, log)
                jugador.contador_danio -= 1
                enemigo.atk = max(0, enemigo.atk - 10)
                enemigo.defensa = max(0, enemigo.defensa - 10)
                log.append(f"  ❌ {enemigo.nombre} golpea a {jugador.nombre}.")
                log.append(f"     {jugador.nombre} pierde {vida_perdida_j} de vida "
                           f"({jugador.vida}/{jugador.vida_max}) "
                           f"y 1 contador → [{jugador.contador_danio}].")
                log.append(f"     {enemigo.nombre} pierde 10 ATK y 10 DEF "
                           f"→ ATK:{enemigo.atk} DEF:{enemigo.defensa}.")
                self._aplicar_muerte_si_procede(jugador, log)

            # ── Empate enemigo ──
            elif empate_e and not jugador_golpea and not empate_j:
                log.append(f"  ⚖️  EMPATE — {enemigo.nombre} y {jugador.nombre} igualan fuerzas.")
                if isinstance(jugador, Mago):
                    self._aplicar_pasiva_mago(jugador, enemigo, log)
                jugador.contador_danio -= 1
                enemigo.contador_danio -= 1
                self._aplicar_muerte_si_procede(jugador, log)
                self._aplicar_muerte_si_procede(enemigo, log)

            log.append(f"  📊 {jugador.nombre}: contadores={jugador.contador_danio}  "
                       f"vida={jugador.vida}/{jugador.vida_max}")
            log.append(f"  📊 {enemigo.nombre}: contadores={enemigo.contador_danio}  "
                       f"vida={enemigo.vida}/{enemigo.vida_max}")
            turno += 1

    # ─────────────────────────────────────────────────────
    #  COMBATE JEFE
    # ─────────────────────────────────────────────────────

    def _combate_jefe(self, jugador, enemigo, log):
        """
        Bucle contra EnemigoJefe. Misma lógica de doble comparación independiente:

          ATK jugador > DEF jefe → jefe pierde 1 contador
                                   jugador pierde 20 ATK y 20 DEF
          ATK jefe > DEF jugador → jugador pierde 2 contadores + vida
                                   jefe pierde 20 ATK y 20 DEF
          Salvación              → si el jefe va a quitar el último contador,
                                   se lanza 1-100: si > 70 el jugador se salva.
        """
        turno = 1

        while jugador.esta_vivo() and enemigo.esta_vivo():
            log.append(f"\n  TURNO {turno}")

            # Pasiva del Asesino: lanzamiento de suerte
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
                        self._aplicar_muerte_si_procede(enemigo, log)
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

            # ── Jugador golpea al jefe ──
            if jugador_golpea:
                enemigo.contador_danio -= 1
                jugador.atk = max(0, jugador.atk - 20)
                jugador.defensa = max(0, jugador.defensa - 20)
                log.append(f"  ✅ {jugador.nombre} golpea al jefe {enemigo.nombre}.")
                log.append(f"     {enemigo.nombre} pierde 1 contador "
                           f"→ [{enemigo.contador_danio}].")
                log.append(f"     {jugador.nombre} pierde 20 ATK y 20 DEF "
                           f"→ ATK:{jugador.atk} DEF:{jugador.defensa}.")
                self._aplicar_muerte_si_procede(enemigo, log)

            # ── Empate jugador ──
            elif empate_j:
                log.append(f"  ⚖️  EMPATE — {jugador.nombre} y {enemigo.nombre} igualan fuerzas.")
                if isinstance(jugador, Mago):
                    self._aplicar_pasiva_mago(jugador, enemigo, log)
                jugador.contador_danio -= 1
                enemigo.contador_danio -= 1
                self._aplicar_muerte_si_procede(jugador, log)
                self._aplicar_muerte_si_procede(enemigo, log)

            if not enemigo.esta_vivo() or not jugador.esta_vivo():
                log.append(f"  🎫 {jugador.nombre}: contadores={jugador.contador_danio}  "
                           f"vida={jugador.vida}/{jugador.vida_max}")
                log.append(f"  🎫 {enemigo.nombre}: contadores={enemigo.contador_danio}  "
                           f"vida={enemigo.vida}/{enemigo.vida_max}")
                break

            # ── Jefe golpea al jugador ──
            if jefe_golpea:
                log.append(f"  ❌ {enemigo.nombre} ataca a {jugador.nombre}.")
                contadores_a_perder = 2

                # ¿Va a quitar el último contador?
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
                    self._aplicar_pasiva_mago(jugador, enemigo, log)

                vida_perdida_j = jugador.perder_vida_por_golpe()
                jugador.contador_danio = max(0, jugador.contador_danio - contadores_a_perder)
                enemigo.atk = max(0, enemigo.atk - 20)
                enemigo.defensa = max(0, enemigo.defensa - 20)
                log.append(f"     {jugador.nombre} pierde {vida_perdida_j} de vida "
                           f"({jugador.vida}/{jugador.vida_max}) "
                           f"y {contadores_a_perder} contadores → [{jugador.contador_danio}].")
                log.append(f"     {enemigo.nombre} pierde 20 ATK y 20 DEF "
                           f"→ ATK:{enemigo.atk} DEF:{enemigo.defensa}.")
                self._aplicar_muerte_si_procede(jugador, log)

            # ── Empate jefe ──
            elif empate_e and not jugador_golpea and not empate_j:
                log.append(f"  ⚖️  EMPATE — {enemigo.nombre} y {jugador.nombre} igualan fuerzas.")
                if isinstance(jugador, Mago):
                    self._aplicar_pasiva_mago(jugador, enemigo, log)
                jugador.contador_danio -= 1
                enemigo.contador_danio -= 1
                self._aplicar_muerte_si_procede(jugador, log)
                self._aplicar_muerte_si_procede(enemigo, log)

            log.append(f"  🎫 {jugador.nombre}: contadores={jugador.contador_danio}  "
                       f"vida={jugador.vida}/{jugador.vida_max}")
            log.append(f"  🎫 {enemigo.nombre}: contadores={enemigo.contador_danio}  "
                       f"vida={enemigo.vida}/{enemigo.vida_max}")
            turno += 1

    # ─────────────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────────────

    def _preparar_combate(self, jugador, enemigo):
        """Resetea estados de pasivas al inicio de cada combate."""
        if isinstance(jugador, Mago):
            jugador.resetear_pasiva()
        if isinstance(enemigo, EnemigoJefe):
            enemigo.resetear_salvacion()

    def _aplicar_muerte_si_procede(self, entidad, log):
        """Si el contador llega a 0, la vida también cae a 0."""
        if entidad.contador_danio <= 0 and entidad.vida > 0:
            entidad.vida = 0
            log.append(f" 👻 {entidad.nombre} pierde toda la vida restante → 0.")

    def _aplicar_pasiva_mago(self, mago, enemigo, log):
        """Activa la pasiva del Mago (solo la primera vez por combate)."""
        if mago.intentar_pasiva():
            enemigo.contador_danio = max(0, enemigo.contador_danio - 1)
            log.append(f" 🔥  PASIVA MAGO — {mago.nombre} contraataca: "
                       f"{enemigo.nombre} pierde 1 contador extra "
                       f"→ [{enemigo.contador_danio}].")
            self._aplicar_muerte_si_procede(enemigo, log)


def imprimir_log(log):
    for linea in log:
        print(linea)