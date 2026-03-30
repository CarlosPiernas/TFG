# Anomalías vs Guardianes del Espacio Tiempo

RPG gacha mobile desarrollado con **Kivy (Python)** como Trabajo de Final de Grado.

## Descripción

El jugador elige entre dos facciones (Anomalías o Guardianes), obtiene personajes y armas mediante un sistema gacha, equipa su personaje activo y combate enemigos en un mapa de nodos progresivo. El combate es automático (auto-battle) con animaciones estilo Darkest Dungeon.

- **12 personajes** (6 por facción, rarezas B / A / S)
- **7 armas** (3 básicas + 4 únicas S)
- **10 runas** (4 básicas + 5 mixtas + 1 rota)
- **10 nodos de mapa** con 2 jefes (KRONOS y KRONOS DEFINITIVO)
- **Sistema gacha** con pity system y banners separados (personajes / armas)
- **Sistema de combate** 1v1 con 3 clases (Guerrero, Mago, Asesino) cada una con pasiva única

## Requisitos

- Python 3.10+
- pip

## Ejecución

### Aplicación Kivy (interfaz gráfica)

```bash
python main.py
```

### Demo de consola (prueba todos los sistemas)

```bash
python demo.py
```

La demo permite probar gacha, combate, inventario, mapa y cambio de personaje desde la terminal sin necesidad de Kivy.

### Tests

```bash
# Test de integración completo (Firebase + BD + Gacha + Combate + Mapa)
python tests/test_integracion.py

# Test del sistema gacha
python tests/test_gacha.py

# Test del sistema de combate
python tests/Pruebas.py

# Test del sistema de almacenamiento
python tests/Pruebaalmacenamiento.py
```

## Estructura del proyecto

```
TFG/
├── main.py                  # Punto de entrada Kivy
├── demo.py                  # Demo interactiva de consola
├── config.py                # Colores, rutas de sprites, constantes UI
├── requirements.txt         # Dependencias Python
│
├── database/                # M1 — Persistencia SQLite
│   ├── db_manager.py        #   Conexión y creación de tablas
│   ├── seed.py              #   Datos iniciales (12 personajes, 7 armas, 10 runas)
│   ├── enemigos.json        #   Fallback local de stats de enemigos
│   └── repositories/        #   Patrón Repository para cada tabla
│       ├── personaje_repo.py
│       ├── arma_repo.py
│       ├── runa_repo.py
│       ├── inventario_repo.py
│       ├── equipamiento_repo.py
│       ├── recursos_repo.py
│       ├── pity_repo.py
│       └── mapa_repo.py
│
├── logic/                   # M2 — Lógica de juego
│   ├── gacha.py             #   Sistema gacha (simple + genshin mode)
│   ├── Clases/              #   Jerarquía de personajes y enemigos
│   │   ├── Jugador.py       #     Clase padre (equipo de armas y runas)
│   │   ├── Guerrero.py      #     Tanque físico — pasiva Berserker
│   │   ├── Mago.py          #     DPS mágico — pasiva contraataque
│   │   ├── Asesino.py       #     DPS variable — pasiva suerte
│   │   ├── Enemigo.py       #     Clase padre de enemigos
│   │   ├── EnemigoBasico.py #     Enemigo estándar (3 contadores)
│   │   ├── EnemigoJefe.py   #     Jefe con salvación (4 contadores)
│   │   └── stat.py          #     Todos los valores numéricos del juego
│   ├── Combate/
│   │   └── Encuentro.py     #   Motor de combate turno a turno
│   └── Almacenamiento/
│       ├── DatosJugador.py  #   Estado del jugador en memoria
│       ├── Mochila.py       #   Interfaz de inventario
│       └── Forja.py         #   Transmutación de runas
│
├── firebase/                # M4 — Integración y Firebase
│   ├── firebase_client.py   #   Conexión Firebase + fallback JSON local
│   ├── enemy_loader.py      #   Fábrica de enemigos desde Firebase/JSON
│   ├── game_manager.py      #   Integración central (conecta M1 + M2 + M3)
│   └── poblar_firebase.py   #   Script para subir datos a Firebase
│
├── screens/                 # M3 — Interfaz Kivy
│   ├── faction_screen.py    #   Selección de facción
│   ├── home_screen.py       #   Pantalla principal
│   ├── inventory_screen.py  #   Inventario de personajes/armas/runas
│   ├── gacha_screen.py      #   Banner de tiradas (en construcción)
│   ├── map_screen.py        #   Mapa de nodos (en construcción)
│   └── combat_screen.py     #   Pantalla de combate (en construcción)
│
├── widgets/                 # Componentes UI reutilizables
│   └── componentes.py       #   PanelRedondeado, BotonRedondeado
│
├── tests/                   # Tests
│   ├── test_integracion.py  #   Test end-to-end de todos los sistemas
│   ├── test_gacha.py        #   Test del sistema gacha
│   ├── Pruebas.py           #   Test del sistema de combate
│   └── Pruebaalmacenamiento.py  # Test de Mochila y Forja
│
└── data/
    └── game.db              # Base de datos SQLite (se genera automáticamente)
```

## Firebase

El proyecto usa Firebase Realtime Database para almacenar los stats de los enemigos por nodo. Esto permite ajustar la dificultad sin recompilar la aplicación.

### Configuración

1. Obtener el archivo de credenciales desde la consola de Firebase
2. Guardarlo como `firebase/clave-firebase.json`
3. Instalar el SDK: `pip install firebase-admin` (introducido en requirements.txt)

### Poblar Firebase con datos

```bash
python firebase/poblar_firebase.py
```

### Fallback automático

Si Firebase no está disponible (sin credenciales, sin red, sin SDK), el juego usa automáticamente el archivo `database/enemigos.json` como fuente de datos local. El juego funciona igual en ambos modos.

## Demo para el tribunal

La versión de demostración tiene el pity configurado a **5 tiradas** (en vez de 90 en producción) para poder mostrar el flujo completo en ~10 minutos:

1. Seleccionar facción
2. Tirar gacha hasta obtener personaje S (garantizado en 5 tiradas)
3. Equipar personaje S
4. Combatir en nodos progresivos
5. Mostrar recompensas y progreso del mapa

```bash
python demo.py
```

## Equipo

| Miembro | Rol | Módulos |
|---------|-----|---------|
| Driss (M1) | Base de Datos & Backend | `database/` + `logic/gacha.py` |
| Alex (M2) | Lógica de Juego | `logic/Clases/` + `logic/Combate/` + `logic/Almacenamiento/` |
| Oscar (M3) | Interfaz & Arte | `screens/` + `widgets/` |
| Carlos (M4) | Integración, QA & Firebase | `firebase/` + `tests/test_integracion.py` + `demo.py` |