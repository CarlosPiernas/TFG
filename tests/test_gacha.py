from database.repositories import recursos_repo
from logic.gacha import realizar_pull, realizar_multi_pull

# ── Colores para consola ──────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
GOLD   = "\033[93m"    # S
PURPLE = "\033[95m"    # A
WHITE  = "\033[97m"    # B
RED    = "\033[91m"    # error / fragmento
GREEN  = "\033[92m"    # nuevo
CYAN   = "\033[96m"    # info
GRAY   = "\033[90m"    # separadores

JUGADOR_ID = 1
FACCION    = "guardian"
BANNER     = "personajes"

def color_rareza(rareza: str) -> str:
    if rareza == "S": return GOLD
    if rareza == "A": return PURPLE
    return WHITE

def imprimir_resultado(i: int, r: dict):
    if "error" in r:
        print(f"  {RED}Pull {i:>2}: ✗ {r['error']}{RESET}")
        return

    rareza  = r.get("rareza", "?")
    nombre  = r.get("item", {}).get("nombre", "???")
    es_nuevo = r.get("es_nuevo", False)
    frag    = r.get("fragmento")
    pity    = r.get("pity_count", 0)
    col     = color_rareza(rareza)

    nuevo_txt = f"{GREEN}★ nuevo{RESET}" if es_nuevo else f"{RED}↩ fragmento {frag}{RESET}"
    pity_txt  = f"{GRAY}[pity: {pity}]{RESET}"

    print(f"  {col}{BOLD}Pull {i:>2}: [{rareza}]{RESET} {col}{nombre:<25}{RESET} {nuevo_txt} {pity_txt}")

def imprimir_separador(titulo: str):
    print(f"\n{CYAN}{'─'*55}{RESET}")
    print(f"{CYAN}{BOLD}  {titulo}{RESET}")
    print(f"{CYAN}{'─'*55}{RESET}")

def imprimir_recursos():
    r = recursos_repo.get_recursos()
    print(f"\n  {GRAY}Tickets personaje : {r['tickets_personaje']}")
    print(f"  Tickets arma      : {r['tickets_arma']}")
    print(f"  Fragmentos rojos  : {r['fragmentos_rojos']}")
    print(f"  Fragmentos azules : {r['fragmentos_azules']}{RESET}")

# ── Setup: añadir 300 tickets ─────────────────────────────────────────────────
imprimir_separador("Setup — añadiendo 300 tickets")
recursos_repo.add_recurso("tickets_personaje", 300)
recursos_repo.add_recurso("tickets_arma", 300)
print(f"  {GREEN}✓ 300 tickets de personaje añadidos{RESET}")
print(f"  {GREEN}✓ 300 tickets de arma añadidos{RESET}")
imprimir_recursos()

# ── Test 1: 5 pulls individuales personajes ───────────────────────────────────
imprimir_separador("Test 1 — 5 pulls individuales (personajes · guardian)")
for i in range(1, 6):
    r = realizar_pull(JUGADOR_ID, BANNER, FACCION)
    imprimir_resultado(i, r)

# ── Test 2: x10 personajes ────────────────────────────────────────────────────
imprimir_separador("Test 2 — Multi-pull x10 (personajes · guardian)")
resultados = realizar_multi_pull(JUGADOR_ID, BANNER, FACCION)
for i, r in enumerate(resultados, 1):
    imprimir_resultado(i, r)

rarezas = [r.get("rareza") for r in resultados if "rareza" in r]
print(f"\n  Resumen: {rarezas.count('S')}xS  {rarezas.count('A')}xA  {rarezas.count('B')}xB")

# ── Test 3: x10 armas ─────────────────────────────────────────────────────────
imprimir_separador("Test 3 — Multi-pull x10 (armas)")
resultados_armas = realizar_multi_pull(JUGADOR_ID, "armas", FACCION)
for i, r in enumerate(resultados_armas, 1):
    imprimir_resultado(i, r)

rarezas_a = [r.get("rareza") for r in resultados_armas if "rareza" in r]
print(f"\n  Resumen: {rarezas_a.count('S')}xS  {rarezas_a.count('A')}xA  {rarezas_a.count('B')}xB")

# ── Test 4: pull hasta duplicado ─────────────────────────────────────────────
imprimir_separador("Test 4 — Tirando hasta ver un duplicado")
for i in range(1, 20):
    r = realizar_pull(JUGADOR_ID, BANNER, FACCION)
    imprimir_resultado(i, r)
    if r.get("fragmento"):
        print(f"\n  {RED}Duplicado detectado en pull {i} — fragmento generado correctamente{RESET}")
        break

# ── Estado final ──────────────────────────────────────────────────────────────
imprimir_separador("Estado final de recursos")
imprimir_recursos()
print()