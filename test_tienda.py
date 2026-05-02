# test_tienda.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import initialize_db
from database.seed import run_seed
from database.repositories import recursos_repo
from database.repositories.tienda_repo import (
    comprar_pocion, comprar_ticket_personaje, comprar_ticket_arma,
    comprar_transmutador, get_recursos_tienda, puede_comprar
)

initialize_db()
run_seed()

# Dar monedas para probar
recursos_repo.add_recurso('monedas', 1000)

print("=== RECURSOS ANTES ===")
print(get_recursos_tienda())
print(puede_comprar())

print("\n=== COMPRANDO ===")
print(comprar_pocion())
print(comprar_ticket_personaje())
print(comprar_ticket_arma())
print(comprar_transmutador())

print("\n=== RECURSOS DESPUÉS ===")
print(get_recursos_tienda())