import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("Datos/clave-firebase.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://tfgprueba-a5b90-default-rtdb.europe-west1.firebasedatabase.app/'})

def get_stats(id_nodo):
    try:
        ref = db.reference(f'enemigos/nivel{id_nodo}')
        stats = ref.get()

        if stats:
            nombre = stats.get('nombre')
            print (f"Datos cargados para {nombre}")
            return stats
        else:
            print ("No hay datos")
            return None
    except Exception as e:
        print(e)
        return None

stats_combate = get_stats(1)
print(stats_combate)
