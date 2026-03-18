# API Interna — Base de Datos

Este documento describe todas las funciones disponibles en la capa de datos.
Alex y Oscar deben usar únicamente estas funciones para acceder a la base de datos.
**Nunca llamar a `sqlite3` directamente fuera de la carpeta `database/`.**

---

## Importaciones
```python
from database.repositories.personaje_repo import PersonajeRepo
from database.repositories.arma_repo import ArmaRepo
from database.repositories.runa_repo import RunaRepo
from database.repositories.inventario_repo import InventarioRepo
from database.repositories.equipamiento_repo import EquipamientoRepo
from database.repositories.recursos_repo import RecursosRepo
from database.repositories.pity_repo import PityRepo
from database.repositories.mapa_repo import MapaRepo
```

---

## PersonajeRepo

| Método | Parámetros | Devuelve | Descripción |
|---|---|---|---|
| `get_catalogo()` | — | `list[dict]` | Todos los personajes del catálogo |
| `get_by_id(personaje_id)` | `personaje_id: int` | `dict \| None` | Un personaje por su id |
| `get_by_faccion(faccion)` | `faccion: str` | `list[dict]` | Personajes de una facción |
| `get_by_rareza(rareza)` | `rareza: str` | `list[dict]` | Personajes de una rareza |

**Valores válidos:**
- `faccion` = `'guardian'` | `'anomalia'`
- `rareza` = `'B'` | `'A'` | `'S'`

**Ejemplo:**
```python
repo = PersonajeRepo()
personaje = repo.get_by_id(1)
# {"id": 1, "nombre": "Guardian_Guerrero_B", "faccion": "guardian",
#  "clase": "guerrero", "rareza": "B", "atk_base": 80, "magia_base": 20,
#  "pv_base": 200, "destreza_base": 30, "sprite_id": None}
```

---

## ArmaRepo

| Método | Parámetros | Devuelve | Descripción |
|---|---|---|---|
| `get_catalogo()` | — | `list[dict]` | Todas las armas del catálogo |
| `get_by_id(arma_id)` | `arma_id: int` | `dict \| None` | Un arma por su id |
| `get_by_rareza(rareza)` | `rareza: str` | `list[dict]` | Armas de una rareza |
| `get_arma_de_personaje_s(personaje_id)` | `personaje_id: int` | `dict \| None` | Arma S vinculada a un personaje S |

**Valores válidos:**
- `rareza` = `'basica'` | `'S'`

---

## RunaRepo

| Método | Parámetros | Devuelve | Descripción |
|---|---|---|---|
| `get_catalogo()` | — | `list[dict]` | Todas las runas del catálogo |
| `get_by_id(runa_id)` | `runa_id: int` | `dict \| None` | Una runa por su id |
| `get_by_rareza(rareza)` | `rareza: str` | `list[dict]` | Runas de una rareza |

**Valores válidos:**
- `rareza` = `'generica'` | `'unica_S'`

---

## InventarioRepo

| Método | Parámetros | Devuelve | Descripción |
|---|---|---|---|
| `get_inventario()` | — | `list[dict]` | Todos los ítems del jugador |
| `get_inventario_by_tipo(tipo)` | `tipo: str` | `list[dict]` | Ítems del jugador filtrados por tipo |
| `add_item(tipo, catalogo_id)` | `tipo: str`, `catalogo_id: int` | `int` | Añade un ítem al inventario, devuelve su id |
| `existe_en_inventario(tipo, catalogo_id)` | `tipo: str`, `catalogo_id: int` | `bool` | True si el jugador ya tiene ese ítem |

**Valores válidos:**
- `tipo` = `'personaje'` | `'arma'` | `'runa'`

**Ejemplo:**
```python
repo = InventarioRepo()
nuevo_id = repo.add_item("personaje", 6)
# nuevo_id = 15 (id asignado por SQLite)
```

---

## EquipamientoRepo

| Método | Parámetros | Devuelve | Descripción |
|---|---|---|---|
| `get_equipo_de_personaje(personaje_inv_id)` | `personaje_inv_id: int` | `list[dict]` | Ítems equipados en un personaje |
| `equipar(personaje_inv_id, slot, item_inv_id)` | `int`, `str`, `int` | — | Equipa un ítem, reemplaza si ya había uno |
| `desequipar(personaje_inv_id, slot)` | `int`, `str` | — | Desequipa el ítem de un slot |
| `desequipar_todo(personaje_inv_id)` | `personaje_inv_id: int` | — | Desequipa todo el equipamiento |

**Valores válidos:**
- `slot` = `'arma'` | `'runa_1'` | `'runa_2'`

**Ejemplo:**
```python
repo = EquipamientoRepo()
repo.equipar(15, "arma", 3)
# Equipa el ítem con inventario id=3 en el slot 'arma' del personaje con inventario id=15
```

---

## RecursosRepo

| Método | Parámetros | Devuelve | Descripción |
|---|---|---|---|
| `get_recursos()` | — | `dict \| None` | Todos los recursos del jugador |
| `add_recurso(tipo, cantidad)` | `tipo: str`, `cantidad: int` | — | Suma o resta un recurso |
| `get_pociones()` | — | `dict \| None` | Pociones actuales y máximo |
| `set_ultima_regen(timestamp)` | `timestamp: str` | — | Guarda el timestamp de última regeneración |

**Valores válidos:**
- `tipo` = `'tickets_personaje'` | `'tickets_arma'` | `'moneda_premium'` | `'pociones'`
- Para restar usar cantidad negativa: `add_recurso("tickets_personaje", -1)`

---

## PityRepo

| Método | Parámetros | Devuelve | Descripción |
|---|---|---|---|
| `get_pity(banner)` | `banner: str` | `int` | Contador de pity actual |
| `set_pity(banner, valor)` | `banner: str`, `valor: int` | — | Guarda el contador de pity |
| `reset_pity(banner)` | `banner: str` | — | Resetea el contador a 0 |

**Valores válidos:**
- `banner` = `'personajes'` | `'armas'`

---

## MapaRepo

| Método | Parámetros | Devuelve | Descripción |
|---|---|---|---|
| `get_nodo(nodo_id)` | `nodo_id: int` | `dict \| None` | Estado de un nodo |
| `get_todos_nodos()` | — | `list[dict]` | Estado de todos los nodos |
| `completar_nodo(nodo_id, estrellas)` | `int`, `int` | — | Marca el nodo como completado y desbloquea el siguiente |
| `incrementar_intentos(nodo_id)` | `nodo_id: int` | — | Suma 1 al contador de intentos |

---

## Inicialización

Desde `main.py` al arrancar el juego (Carlos se encarga de integrarlo):
```python
from database.db_manager import initialize_db
from database.seed import run_seed

initialize_db()  # Crea las tablas si no existen
run_seed()       # Rellena el catálogo si está vacío
```