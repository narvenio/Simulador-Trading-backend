import random

def simulate_price(base_price: float) -> float:
    variation = random.uniform(-0.05, +0.05)
    simulate_price = base_price * (1 + variation)
    return round(simulate_price, 2)
# devuelve el precio simulado con 2 decimales