"""
Forja — Transmutación de runas.

Interfaz:
  - 2 huecos vacíos donde el jugador coloca runas de su inventario.
  - 1 hueco de resultado donde aparece la runa mixta resultante.
  - Botón "Transmutar": consume las 2 runas + 1 carga de transmutador,
    genera la runa mixta y la añade al inventario.

Combinaciones válidas:
  ATAQUE + DEFENSA  → ACERO     (+30 ATK, +20 DEF)
  ATAQUE + DESTREZA → CAZA      (+20 ATK, +25 DES)
  DESTREZA + DEFENSA → SOMBRA   (+30 DES, +15 DEF)
  MAGIA + DEFENSA   → ARCANA    (+30 MAG, +10 DEF)
  DESTREZA + MAGIA  → GUARDIAN  (+40 DEF pura)

Cualquier otra combinación → ROTA (-40 DEF).
"""

from logic.Clases.stat import (
    RECETAS_TRANSMUTADOR,
    RESULTADO_MEZCLA_INVALIDA,
    RUNAS_MIXTAS_MAP,
)
from logic.Almacenamiento.Mochila import CATALOGO_RUNAS


class Forja:
    """
    Sistema de transmutación de runas.
    Opera sobre una instancia de DatosJugador.
    """

    def __init__(self, datos_jugador):
        self.datos = datos_jugador

        # ── Slots de la forja ──
        self.slot_1 = None      # nombre de la runa colocada (ej: "ATAQUE")
        self.slot_2 = None      # nombre de la runa colocada (ej: "DEFENSA")
        self.resultado = None   # nombre de la runa resultante (ej: "ACERO")

    # ═══════════════════════════════════
    # COLOCAR RUNAS EN LOS SLOTS
    # ═══════════════════════════════════

    def colocar_runa(self, slot, nombre_runa):
        """
        Coloca una runa del inventario en el slot indicado (1 o 2).
        No la consume aún — solo la reserva visualmente.
        Devuelve {"ok", "mensaje"}.
        """
        if slot not in (1, 2):
            return {"ok": False, "mensaje": "El slot debe ser 1 o 2."}

        if self.datos.cantidad_runa(nombre_runa) <= 0:
            return {"ok": False, "mensaje": f"No tienes runa '{nombre_runa}' en el inventario."}

        # No permitir la misma runa en ambos slots (si solo tiene 1 unidad)
        otro_slot = self.slot_2 if slot == 1 else self.slot_1
        if otro_slot == nombre_runa and self.datos.cantidad_runa(nombre_runa) < 2:
            return {"ok": False, "mensaje": f"Solo tienes 1 '{nombre_runa}', no puedes ponerla en ambos slots."}

        if slot == 1:
            self.slot_1 = nombre_runa
        else:
            self.slot_2 = nombre_runa

        # Limpiar resultado previo
        self.resultado = None

        return {"ok": True, "mensaje": f"Runa '{nombre_runa}' colocada en slot {slot}."}

    def quitar_runa(self, slot):
        """Quita la runa del slot indicado (sin afectar el inventario)."""
        if slot == 1:
            self.slot_1 = None
        elif slot == 2:
            self.slot_2 = None
        self.resultado = None

    # ═══════════════════════════════════
    # PREVISUALIZAR RESULTADO
    # ═══════════════════════════════════

    def previsualizar(self):
        """
        Muestra qué runa resultaría de la combinación actual SIN consumir nada.
        Devuelve {"nombre", "stats", "es_valida"} o None si los slots no están llenos.
        """
        if self.slot_1 is None or self.slot_2 is None:
            return None

        clave = frozenset([self.slot_1, self.slot_2])
        nombre_resultado = RECETAS_TRANSMUTADOR.get(clave, RESULTADO_MEZCLA_INVALIDA)

        info = CATALOGO_RUNAS.get(nombre_resultado, {})
        return {
            "nombre":    nombre_resultado,
            "stats":     info.get("stats", {}),
            "es_valida": nombre_resultado != RESULTADO_MEZCLA_INVALIDA,
            "descripcion": info.get("descripcion", "Resultado desconocido."),
        }

    # ═══════════════════════════════════
    # TRANSMUTAR (BOTÓN)
    # ═══════════════════════════════════

    def transmutar(self):
        """
        Ejecuta la transmutación:
          1. Verifica que hay 2 runas en los slots.
          2. Verifica que hay al menos 1 transmutador.
          3. Consume las 2 runas del inventario.
          4. Consume 1 transmutador.
          5. Genera la runa resultante y la añade al inventario.
          6. Muestra el resultado en el slot de resultado.
        Devuelve {"ok", "mensaje", "resultado"}.
        """
        # ── Validaciones ──
        if self.slot_1 is None or self.slot_2 is None:
            return {
                "ok": False,
                "mensaje": "Debes colocar una runa en cada slot.",
                "resultado": None,
            }

        if self.slot_1 == self.slot_2:
            return {
                "ok": False,
                "mensaje": "No puedes combinar una runa consigo misma.",
                "resultado": None,
            }

        if self.datos.transmutadores <= 0:
            return {
                "ok": False,
                "mensaje": "No tienes cargas de transmutador.",
                "resultado": None,
            }

        if self.datos.cantidad_runa(self.slot_1) <= 0:
            return {
                "ok": False,
                "mensaje": f"Ya no tienes runa '{self.slot_1}' en el inventario.",
                "resultado": None,
            }

        if self.datos.cantidad_runa(self.slot_2) <= 0:
            return {
                "ok": False,
                "mensaje": f"Ya no tienes runa '{self.slot_2}' en el inventario.",
                "resultado": None,
            }

        # ── Consumir recursos ──
        self.datos.quitar_runa(self.slot_1)
        self.datos.quitar_runa(self.slot_2)
        self.datos.usar_transmutador()

        # ── Calcular resultado ──
        clave = frozenset([self.slot_1, self.slot_2])
        nombre_resultado = RECETAS_TRANSMUTADOR.get(clave, RESULTADO_MEZCLA_INVALIDA)

        # ── Añadir resultado al inventario ──
        self.datos.agregar_runa(nombre_resultado)

        # ── Actualizar slots ──
        runa1_usada = self.slot_1
        runa2_usada = self.slot_2
        self.slot_1 = None
        self.slot_2 = None
        self.resultado = nombre_resultado

        # ── Construir mensaje ──
        info = CATALOGO_RUNAS.get(nombre_resultado, {})
        stats_str = ", ".join(f"{k}: {v:+d}" for k, v in info.get("stats", {}).items())
        es_valida = nombre_resultado != RESULTADO_MEZCLA_INVALIDA

        if es_valida:
            mensaje = (f"Transmutación exitosa: {runa1_usada} + {runa2_usada} "
                       f"= RUNA_{nombre_resultado} ({stats_str})")
        else:
            mensaje = (f"Transmutación fallida: {runa1_usada} + {runa2_usada} "
                       f"= RUNA_ROTA ({stats_str}). ¡Combinación no válida!")

        return {
            "ok": True,
            "mensaje": mensaje,
            "resultado": {
                "nombre":    nombre_resultado,
                "stats":     info.get("stats", {}),
                "es_valida": es_valida,
                "descripcion": info.get("descripcion", ""),
            },
        }

    # ═══════════════════════════════════
    # LIMPIAR FORJA
    # ═══════════════════════════════════

    def limpiar(self):
        """Vacía todos los slots de la forja."""
        self.slot_1 = None
        self.slot_2 = None
        self.resultado = None

    # ═══════════════════════════════════
    # ESTADO ACTUAL
    # ═══════════════════════════════════

    def estado(self):
        """Devuelve el estado actual de la forja para la UI."""
        prev = self.previsualizar()
        return {
            "slot_1":          self.slot_1,
            "slot_2":          self.slot_2,
            "resultado":       self.resultado,
            "previsualizacion": prev,
            "transmutadores":  self.datos.transmutadores,
            "puede_transmutar": (self.slot_1 is not None
                                 and self.slot_2 is not None
                                 and self.slot_1 != self.slot_2
                                 and self.datos.transmutadores > 0),
        }

    # ═══════════════════════════════════
    # RUNAS DISPONIBLES PARA LA FORJA
    # ═══════════════════════════════════

    def runas_disponibles(self):
        """
        Devuelve las runas básicas que el jugador tiene disponibles para transmutar.
        Solo las básicas se pueden meter en la forja.
        """
        basicas = ["ATAQUE", "MAGIA", "DEFENSA", "DESTREZA"]
        resultado = []
        for nombre in basicas:
            cantidad = self.datos.cantidad_runa(nombre)
            if cantidad > 0:
                resultado.append({"nombre": nombre, "cantidad": cantidad})
        return resultado