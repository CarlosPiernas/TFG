"""
enemy_loader.py — Carga de enemigos para el sistema de combate.

Responsable: M4 (Carlos)

Uso:
    from firebase.enemy_loader import EnemyLoader

    loader = EnemyLoader()
    enemigo = loader.crear_enemigo(nodo_id=3)   # EnemigoBasico
    jefe    = loader.crear_enemigo(nodo_id=5)   # EnemigoJefe
"""

import sys, os, importlib

# Asegurar que la raíz del proyecto está en el path
_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# Importar FirebaseClient (mismo paquete, no da conflicto)
from firebase.firebase_client import FirebaseClient

# Importar clases de M2 con importlib para evitar conflicto
# con el paquete firebase-admin en Windows
_EnemigoBasico = importlib.import_module("logic.Clases.EnemigoBasico").EnemigoBasico
_EnemigoJefe   = importlib.import_module("logic.Clases.EnemigoJefe").EnemigoJefe


class EnemyLoader:
    """
    Fábrica de enemigos. Lee datos de Firebase (o JSON local)
    y devuelve instancias de las clases de M2.
    """

    def __init__(self, firebase_client=None):
        self._fb = firebase_client if firebase_client is not None else FirebaseClient()

    def crear_enemigo(self, nodo_id: int):
        """
        Crea EnemigoBasico o EnemigoJefe según el tipo del nodo.
        Retorna None si el nodo no existe.
        """
        datos = self._fb.get_enemigo(nodo_id)
        if datos is None:
            print(f"[EnemyLoader] No hay datos para nodo {nodo_id}.")
            return None

        if datos["tipo"] == "jefe":
            return _EnemigoJefe(
                nombre=datos["nombre"], atk=datos["atk"],
                vida=datos["vida"], defensa=datos["defensa"],
            )
        else:
            return _EnemigoBasico(
                nombre=datos["nombre"], atk=datos["atk"],
                vida=datos["vida"], defensa=datos["defensa"],
            )

    def crear_todos_enemigos(self) -> dict:
        datos_todos = self._fb.get_todos_enemigos()
        return {nid: self.crear_enemigo(nid) for nid in datos_todos if self.crear_enemigo(nid)}

    def get_info_nodo(self, nodo_id: int) -> dict | None:
        return self._fb.get_enemigo(nodo_id)

    def listar_nodos(self) -> list[dict]:
        datos_todos = self._fb.get_todos_enemigos()
        resultado = []
        for nodo_id in sorted(datos_todos.keys()):
            info = datos_todos[nodo_id].copy()
            info["nodo_id"] = nodo_id
            resultado.append(info)
        return resultado

    def estado(self) -> dict:
        fb_estado = self._fb.estado()
        todos = self._fb.get_todos_enemigos()
        return {**fb_estado, "enemigos_disponibles": len(todos), "nodos": sorted(todos.keys())}