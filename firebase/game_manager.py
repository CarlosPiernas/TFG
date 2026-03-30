"""
game_manager.py — Módulo de integración central.

Responsable: M4 (Carlos)

Este módulo es el PEGAMENTO entre los tres sistemas:
  - M1 (database/) → Persistencia SQLite
  - M2 (logic/)    → Lógica de combate, clases, gacha
  - M3 (screens/)  → Interfaz Kivy

Uso desde las pantallas:
    from firebase.game_manager import GameManager

    gm = GameManager()
    gm.iniciar_juego(faccion="guardian")
    resultado = gm.tirar_gacha(banner="personajes")
    log = gm.iniciar_combate(nodo_id=3)
    personajes = gm.get_personajes_jugador()
"""

import sys, os, importlib

# Asegurar que la raíz del proyecto está en el path
_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# ── Imports de database (no conflictan) ──
from database.db_manager import initialize_db, get_connection
from database.seed import run_seed
from database.repositories import (
    personaje_repo, arma_repo, runa_repo,
    inventario_repo, recursos_repo, pity_repo,
)
from database.repositories.mapa_repo import MapaRepo
from database.repositories.equipamiento_repo import EquipamientoRepo

# ── Imports de logic con importlib (evita conflicto firebase-admin en Windows) ──
Guerrero  = importlib.import_module("logic.Clases.Guerrero").Guerrero
Mago      = importlib.import_module("logic.Clases.Mago").Mago
Asesino   = importlib.import_module("logic.Clases.Asesino").Asesino
Encuentro = importlib.import_module("logic.Combate.Encuentro").Encuentro

_gacha_mod          = importlib.import_module("logic.gacha")
realizar_pull       = _gacha_mod.realizar_pull
realizar_multi_pull = _gacha_mod.realizar_multi_pull

# ── Import de firebase (mismo paquete) ──
from firebase.enemy_loader import EnemyLoader


class GameManager:
    MAX_TURNOS = 50

    def __init__(self):
        initialize_db()
        run_seed()
        self._mapa_repo = MapaRepo()
        self._equip_repo = EquipamientoRepo()
        self._enemy_loader = EnemyLoader()
        self._encuentro = Encuentro()
        self.faccion = None
        self.personaje_activo_id = None
        self.jugador_id = 1
        print("[GameManager] Inicializado correctamente.")

    # ═══════════════════════════════════
    # INICIO DEL JUEGO
    # ═══════════════════════════════════

    def iniciar_juego(self, faccion: str):
        self.faccion = faccion.lower()
        personajes = personaje_repo.get_by_faccion(self.faccion)

        # Buscar personaje B Guerrero, o cualquier B
        personaje_b = None
        for p in personajes:
            if p["rareza"] == "B" and p["clase"] == "guerrero":
                personaje_b = p
                break
        if personaje_b is None:
            for p in personajes:
                if p["rareza"] == "B":
                    personaje_b = p
                    break
        if personaje_b is None:
            print(f"[GameManager] ERROR: No hay personaje B para '{faccion}'")
            return

        inventario_repo.agregar_item(self.jugador_id, personaje_b["id"], "personaje")
        inv = inventario_repo.get_inventario_by_tipo("personaje")
        for item in inv:
            if item["catalogo_id"] == personaje_b["id"]:
                self.personaje_activo_id = item["id"]
                break

        print(f"[GameManager] Facción: {self.faccion}. "
              f"Personaje inicial: {personaje_b['nombre']} (ID inv: {self.personaje_activo_id})")

    # ═══════════════════════════════════
    # PERSONAJE ACTIVO
    # ═══════════════════════════════════

    def get_personaje_activo_info(self) -> dict | None:
        if self.personaje_activo_id is None:
            return None
        inv = inventario_repo.get_inventario()
        catalogo_id = None
        for item in inv:
            if item["id"] == self.personaje_activo_id and item["tipo"] == "personaje":
                catalogo_id = item["catalogo_id"]
                break
        if catalogo_id is None:
            return None
        datos = personaje_repo.get_by_id(catalogo_id)
        if datos is None:
            return None
        equipo = self._equip_repo.get_equipo_de_personaje(self.personaje_activo_id)
        datos["equipo"] = equipo
        datos["inv_id"] = self.personaje_activo_id
        return datos

    def cambiar_personaje_activo(self, inv_id: int):
        self.personaje_activo_id = inv_id

    # ═══════════════════════════════════
    # INVENTARIO
    # ═══════════════════════════════════

    def get_personajes_jugador(self) -> list[dict]:
        inv_personajes = inventario_repo.get_inventario_by_tipo("personaje")
        resultado = []
        for item in inv_personajes:
            datos = personaje_repo.get_by_id(item["catalogo_id"])
            if datos:
                datos["inv_id"] = item["id"]
                resultado.append(datos)
        return resultado

    def get_armas_jugador(self) -> list[dict]:
        inv_armas = inventario_repo.get_inventario_by_tipo("arma")
        resultado = []
        for item in inv_armas:
            datos = arma_repo.get_by_id(item["catalogo_id"])
            if datos:
                datos["inv_id"] = item["id"]
                resultado.append(datos)
        return resultado

    def get_runas_jugador(self) -> list[dict]:
        inv_runas = inventario_repo.get_inventario_by_tipo("runa")
        resultado = []
        for item in inv_runas:
            datos = runa_repo.get_by_id(item["catalogo_id"])
            if datos:
                datos["inv_id"] = item["id"]
                resultado.append(datos)
        return resultado

    def get_recursos(self) -> dict:
        return recursos_repo.get_recursos() or {}

    # ═══════════════════════════════════
    # EQUIPAMIENTO
    # ═══════════════════════════════════

    def equipar_arma(self, arma_inv_id: int):
        if self.personaje_activo_id is None:
            return {"ok": False, "mensaje": "No hay personaje activo."}
        self._equip_repo.equipar(self.personaje_activo_id, "arma", arma_inv_id)
        return {"ok": True, "mensaje": "Arma equipada."}

    def equipar_runa(self, runa_inv_id: int, slot: int):
        if self.personaje_activo_id is None:
            return {"ok": False, "mensaje": "No hay personaje activo."}
        self._equip_repo.equipar(self.personaje_activo_id, f"runa_{slot}", runa_inv_id)
        return {"ok": True, "mensaje": f"Runa equipada en slot {slot}."}

    def desequipar(self, slot: str):
        if self.personaje_activo_id is None:
            return
        self._equip_repo.desequipar(self.personaje_activo_id, slot)

    # ═══════════════════════════════════
    # GACHA
    # ═══════════════════════════════════

    def tirar_gacha(self, banner: str) -> dict:
        if self.faccion is None:
            return {"error": "faccion_no_seleccionada"}
        return realizar_pull(self.jugador_id, banner, self.faccion)

    def tirar_gacha_x10(self, banner: str) -> list[dict]:
        if self.faccion is None:
            return [{"error": "faccion_no_seleccionada"}]
        return realizar_multi_pull(self.jugador_id, banner, self.faccion)

    # ═══════════════════════════════════
    # MAPA
    # ═══════════════════════════════════

    def get_mapa(self) -> list[dict]:
        nodos = self._mapa_repo.get_todos_nodos()
        resultado = []
        for nodo in nodos:
            nodo_dict = dict(nodo)
            enemigo_info = self._enemy_loader.get_info_nodo(nodo["nodo_id"])
            if enemigo_info:
                nodo_dict["enemigo"] = enemigo_info
            resultado.append(nodo_dict)
        return resultado

    def get_nodo(self, nodo_id: int) -> dict | None:
        nodo = self._mapa_repo.get_nodo(nodo_id)
        if nodo is None:
            return None
        nodo_dict = dict(nodo)
        enemigo_info = self._enemy_loader.get_info_nodo(nodo_id)
        if enemigo_info:
            nodo_dict["enemigo"] = enemigo_info
        return nodo_dict

    # ═══════════════════════════════════
    # COMBATE
    # ═══════════════════════════════════

    def iniciar_combate(self, nodo_id: int) -> dict:
        nodo = self._mapa_repo.get_nodo(nodo_id)
        if nodo is None:
            return {"victoria": False, "log": ["Nodo no encontrado."], "recompensas": None}
        if nodo["estado"] == "bloqueado":
            return {"victoria": False, "log": ["Nodo bloqueado."], "recompensas": None}

        enemigo = self._enemy_loader.crear_enemigo(nodo_id)
        if enemigo is None:
            return {"victoria": False, "log": ["No se pudo cargar el enemigo."], "recompensas": None}

        jugador = self._crear_jugador_para_combate()
        if jugador is None:
            return {"victoria": False, "log": ["No hay personaje activo."], "recompensas": None}

        log = self._encuentro.iniciar(jugador, enemigo)

        # Protección BUG-03: si ambos siguen vivos, desempatar por PV
        if jugador.esta_vivo() and enemigo.esta_vivo():
            log.append("⏰ LÍMITE DE TURNOS alcanzado.")
            if jugador.vida >= enemigo.vida:
                log.append(f"🏆 VICTORIA por PV — {jugador.nombre}: {jugador.vida} vs {enemigo.nombre}: {enemigo.vida}")
                victoria = True
            else:
                log.append(f"💀 DERROTA por PV — {jugador.nombre}: {jugador.vida} vs {enemigo.nombre}: {enemigo.vida}")
                victoria = False
        else:
            victoria = jugador.esta_vivo()

        recompensas = None
        if victoria:
            recompensas = self._dar_recompensas(nodo_id)
            self._mapa_repo.completar_nodo(nodo_id, estrellas=1)

        return {"victoria": victoria, "log": log, "recompensas": recompensas}

    def _crear_jugador_para_combate(self):
        info = self.get_personaje_activo_info()
        if info is None:
            return None

        clase   = info["clase"].lower()
        nombre  = info["nombre"]
        atk     = info["atk_base"]
        vida    = info["pv_base"]
        defensa = info.get("defensa_base", 0)

        if clase == "guerrero":
            jugador = Guerrero(nombre=nombre, atk=atk, vida=vida, defensa=defensa)
        elif clase == "mago":
            jugador = Mago(nombre=nombre, atk=atk, vida=vida, defensa=defensa, magia=info.get("magia_base", 0))
        elif clase == "asesino":
            jugador = Asesino(nombre=nombre, atk=atk, vida=vida, defensa=defensa, destreza=info.get("destreza_base", 0))
        else:
            jugador = Guerrero(nombre=nombre, atk=atk, vida=vida, defensa=defensa)

        # Aplicar bonuses de equipo
        equipo = self._equip_repo.get_equipo_de_personaje(self.personaje_activo_id)
        for slot in equipo:
            inv_items = inventario_repo.get_inventario()
            for inv_item in inv_items:
                if inv_item["id"] == slot["item_inv_id"]:
                    if inv_item["tipo"] == "arma":
                        arma_data = arma_repo.get_by_id(inv_item["catalogo_id"])
                        if arma_data:
                            jugador.atk += arma_data.get("bonus_atk", 0)
                            jugador.defensa += arma_data.get("bonus_def", 0)
                            jugador.magia += arma_data.get("bonus_magia", 0)
                            jugador.destreza += arma_data.get("bonus_destreza", 0)
                            bv = arma_data.get("bonus_pv", 0)
                            jugador.vida += bv
                            jugador.vida_max += bv
                    elif inv_item["tipo"] == "runa":
                        runa_data = runa_repo.get_by_id(inv_item["catalogo_id"])
                        if runa_data:
                            jugador.atk += runa_data.get("bonus_atk", 0)
                            jugador.defensa += runa_data.get("bonus_def", 0)
                            jugador.magia += runa_data.get("bonus_magia", 0)
                            jugador.destreza += runa_data.get("bonus_destreza", 0)
                            bv = runa_data.get("bonus_pv", 0)
                            jugador.vida += bv
                            jugador.vida_max += bv
                    break
        return jugador

    def _dar_recompensas(self, nodo_id: int) -> dict:
        import random
        _stat = importlib.import_module("logic.Clases.stat")
        MONEDAS_POR_NODO = _stat.MONEDAS_POR_NODO
        NODOS_TICKET_GRATIS = _stat.NODOS_TICKET_GRATIS

        monedas = MONEDAS_POR_NODO.get(nodo_id, 50)
        try:
            recursos_repo.add_recurso("monedas", monedas)
        except Exception:
            recursos_repo.add_recurso("moneda_premium", monedas)
        recompensas = {"monedas": monedas}

        if nodo_id in NODOS_TICKET_GRATIS:
            tipo_ticket = NODOS_TICKET_GRATIS[nodo_id]
            if tipo_ticket == "aleatorio":
                tipo_ticket = random.choice(["personaje", "arma"])
            if tipo_ticket == "personaje":
                recursos_repo.add_recurso("tickets_personaje", 1)
                recompensas["ticket_personaje"] = 1
            else:
                recursos_repo.add_recurso("tickets_arma", 1)
                recompensas["ticket_arma"] = 1
        return recompensas

    # ═══════════════════════════════════
    # POCIONES
    # ═══════════════════════════════════

    def usar_pocion(self) -> bool:
        pociones = recursos_repo.get_pociones()
        if pociones and pociones["pociones"] > 0:
            recursos_repo.add_recurso("pociones", -1)
            return True
        return False

    # ═══════════════════════════════════
    # ESTADO / DEBUG
    # ═══════════════════════════════════

    def estado_completo(self) -> dict:
        return {
            "faccion": self.faccion,
            "personaje_activo": self.get_personaje_activo_info(),
            "recursos": self.get_recursos(),
            "personajes": len(self.get_personajes_jugador()),
            "armas": len(self.get_armas_jugador()),
            "mapa": self.get_mapa(),
            "firebase": self._enemy_loader.estado(),
        }