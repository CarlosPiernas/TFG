"""
poblar_firebase.py — Sube datos de enemigos a Firebase.

Ejecutar desde la raíz del proyecto:
    python firebase/poblar_firebase.py
"""

import sys, os, importlib
_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from firebase.firebase_client import FirebaseClient
ENEMIGOS = importlib.import_module("logic.Clases.stat").ENEMIGOS


def main():
    print("=" * 55)
    print("  POBLAR FIREBASE CON DATOS DE ENEMIGOS")
    print("=" * 55)

    datos = {}
    for nodo_id, d in ENEMIGOS.items():
        datos[nodo_id] = {
            "nombre": d["nombre"], "tipo": d["tipo"],
            "atk": d["atk"], "defensa": d["defensa"], "vida": d["vida"],
        }

    print(f"\n  Enemigos: {len(datos)}")
    for nid in sorted(datos):
        e = datos[nid]
        icon = "👑" if e["tipo"] == "jefe" else "👾"
        print(f"    Nodo {nid:>2}: {icon} {e['nombre']:<22} ATK:{e['atk']:>3} DEF:{e['defensa']:>3} VID:{e['vida']:>4}")

    fb = FirebaseClient()
    print(f"\n  Modo: {fb.modo}")

    if fb.modo == "firebase":
        fb.poblar_enemigos(datos)
        fb.set_config("pity_demo", 5)
        fb.set_config("pity_produccion", 90)
        print("  ✅ Datos subidos a Firebase.")
    else:
        print("  ⚠️  Firebase no disponible.")

    fb.poblar_json_local(datos)
    print("  ✅ JSON local actualizado.")

    kronos = fb.get_enemigo(5)
    if kronos:
        print(f"\n  Verificación nodo 5: {kronos['nombre']} ATK:{kronos['atk']} DEF:{kronos['defensa']} VID:{kronos['vida']}")

    print("\n" + "=" * 55)

if __name__ == "__main__":
    main()