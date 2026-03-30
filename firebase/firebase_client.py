"""
firebase_client.py — Conexión con Firebase Realtime Database.

Responsable: M4 (Carlos)

Funcionalidad:
  - Inicializa la conexión con Firebase usando firebase-admin SDK.
  - Proporciona métodos CRUD para leer datos de enemigos por nodo.
  - Si Firebase no está disponible (sin credenciales, sin red, error),
    usa automáticamente el JSON local como fallback.

Uso:
    from firebase.firebase_client import FirebaseClient

    fb = FirebaseClient()
    enemigo = fb.get_enemigo(nodo_id=3)
    todos   = fb.get_todos_enemigos()
"""

import json
import os

# ── Rutas ──
_DIR_ACTUAL   = os.path.dirname(os.path.abspath(__file__))
_RUTA_CLAVE   = os.path.join(_DIR_ACTUAL, "clave-firebase.json")
_RUTA_JSON    = os.path.join(_DIR_ACTUAL, "..", "database", "enemigos.json")

# ── Intentar importar firebase_admin ──
try:
    import firebase_admin
    from firebase_admin import credentials, db as firebase_db
    _FIREBASE_DISPONIBLE = True
except ImportError:
    _FIREBASE_DISPONIBLE = False


class FirebaseClient:
    _DATABASE_URL = "https://tfgprueba-a5b90-default-rtdb.europe-west1.firebasedatabase.app"

    def __init__(self):
        self._datos_locales = None
        self._conectado = False
        self.modo = "local"
        self._intentar_conexion_firebase()
        if not self._conectado:
            self._cargar_json_local()

    def _intentar_conexion_firebase(self):
        if not _FIREBASE_DISPONIBLE:
            print("[Firebase] SDK firebase-admin no instalado. Usando JSON local.")
            return
        if not os.path.exists(_RUTA_CLAVE):
            print("[Firebase] No se encontró clave-firebase.json. Usando JSON local.")
            return
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(_RUTA_CLAVE)
                firebase_admin.initialize_app(cred, {"databaseURL": self._DATABASE_URL})
            ref = firebase_db.reference("/enemigos")
            datos = ref.get()
            if datos is not None:
                self._conectado = True
                self.modo = "firebase"
                print("[Firebase] Conexión establecida correctamente.")
            else:
                print("[Firebase] Conectado pero sin datos. Usando JSON local.")
        except Exception as e:
            print(f"[Firebase] Error al conectar: {e}. Usando JSON local.")

    def _cargar_json_local(self):
        try:
            with open(_RUTA_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._datos_locales = data.get("enemigos", {})
            print(f"[Firebase] JSON local cargado: {len(self._datos_locales)} enemigos.")
        except FileNotFoundError:
            print(f"[Firebase] ERROR: No se encontró {_RUTA_JSON}")
            self._datos_locales = {}
        except json.JSONDecodeError as e:
            print(f"[Firebase] ERROR: JSON malformado: {e}")
            self._datos_locales = {}

    def get_enemigo(self, nodo_id: int) -> dict | None:
        clave = f"nodo_{nodo_id}"
        if self._conectado:
            return self._get_enemigo_firebase(clave)
        return self._get_enemigo_local(clave)

    def _get_enemigo_firebase(self, clave: str) -> dict | None:
        try:
            ref = firebase_db.reference(f"/enemigos/{clave}")
            datos = ref.get()
            if datos is None:
                return None
            return self._normalizar_enemigo(datos)
        except Exception as e:
            print(f"[Firebase] Error al leer {clave}: {e}")
            return self._get_enemigo_local(clave)

    def _get_enemigo_local(self, clave: str) -> dict | None:
        datos = self._datos_locales.get(clave)
        if datos is None:
            return None
        return self._normalizar_enemigo(datos)

    def get_todos_enemigos(self) -> dict:
        if self._conectado:
            return self._get_todos_firebase()
        return self._get_todos_local()

    def _get_todos_firebase(self) -> dict:
        try:
            ref = firebase_db.reference("/enemigos")
            datos = ref.get()
            if datos is None:
                return {}
            resultado = {}
            for clave, valor in datos.items():
                try:
                    nodo_id = int(clave.replace("nodo_", ""))
                    resultado[nodo_id] = self._normalizar_enemigo(valor)
                except (ValueError, TypeError):
                    continue
            return resultado
        except Exception as e:
            print(f"[Firebase] Error al leer todos: {e}")
            return self._get_todos_local()

    def _get_todos_local(self) -> dict:
        resultado = {}
        for clave, valor in self._datos_locales.items():
            try:
                nodo_id = int(clave.replace("nodo_", ""))
                resultado[nodo_id] = self._normalizar_enemigo(valor)
            except (ValueError, TypeError):
                continue
        return resultado

    def set_enemigo(self, nodo_id: int, datos: dict) -> bool:
        if not self._conectado:
            return False
        try:
            ref = firebase_db.reference(f"/enemigos/nodo_{nodo_id}")
            ref.set(datos)
            return True
        except Exception as e:
            print(f"[Firebase] Error al escribir nodo_{nodo_id}: {e}")
            return False

    def poblar_enemigos(self, enemigos_dict: dict) -> bool:
        if not self._conectado:
            return False
        try:
            datos_firebase = {f"nodo_{k}": v for k, v in enemigos_dict.items()}
            firebase_db.reference("/enemigos").set(datos_firebase)
            print(f"[Firebase] {len(datos_firebase)} enemigos subidos.")
            return True
        except Exception as e:
            print(f"[Firebase] Error al poblar: {e}")
            return False

    def get_config(self, clave: str, default=None):
        if not self._conectado:
            return default
        try:
            valor = firebase_db.reference(f"/config/{clave}").get()
            return valor if valor is not None else default
        except Exception:
            return default

    def set_config(self, clave: str, valor) -> bool:
        if not self._conectado:
            return False
        try:
            firebase_db.reference(f"/config/{clave}").set(valor)
            return True
        except Exception:
            return False

    def _normalizar_enemigo(self, datos: dict) -> dict:
        return {
            "nombre":  str(datos.get("nombre", "Enemigo desconocido")),
            "tipo":    str(datos.get("tipo", "basico")),
            "atk":     int(datos.get("atk", 0)),
            "defensa": int(datos.get("defensa", datos.get("def", 0))),
            "vida":    int(datos.get("vida", datos.get("hp", 0))),
        }

    def poblar_json_local(self, enemigos_dict: dict):
        datos_json = {"enemigos": {f"nodo_{k}": v for k, v in enemigos_dict.items()}}
        with open(_RUTA_JSON, "w", encoding="utf-8") as f:
            json.dump(datos_json, f, indent=4, ensure_ascii=False)
        print(f"[Firebase] JSON local actualizado con {len(enemigos_dict)} enemigos.")

    def estado(self) -> dict:
        return {
            "modo": self.modo, "conectado": self._conectado,
            "sdk": _FIREBASE_DISPONIBLE, "clave": os.path.exists(_RUTA_CLAVE),
            "json_local": os.path.exists(_RUTA_JSON),
        }