import os
import csv
import logging
from datetime import datetime

import requests

# =========================
# Rutas y constantes básicas
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

DATA_FILE = os.path.join(DATA_DIR, "btc_prices.csv")
LOG_FILE = os.path.join(LOGS_DIR, "app.log")

# API pública de CoinGecko para obtener precio de BTC en USD
API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

# Asegurar que existan carpetas data/ y logs/
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# =========================
# Configuración de logging
# =========================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [collector] %(levelname)s: %(message)s",
)


# =========================
# Funciones principales
# =========================

def fetch_btc_price_usd() -> float:
    """
    Consulta la API y devuelve el precio de BTC en USD como float.
    Lanza excepción si algo sale mal.
    """
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        price = float(data["bitcoin"]["usd"])
        logging.info(f"Precio obtenido de la API: {price} USD")
        return price
    except Exception as e:
        logging.error(f"Error al obtener el precio de BTC: {e}")
        raise


def append_price_row(price: float) -> None:
    """
    Agrega una fila al CSV con timestamp UTC e importe en USD.
    Si el archivo no existe, escribe primero el encabezado.
    """
    file_exists = os.path.isfile(DATA_FILE)
    timestamp = datetime.utcnow().isoformat()

    with open(DATA_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "price_usd"])
        writer.writerow([timestamp, price])

    logging.info(f"Registro guardado: {timestamp}, {price} USD")


def main() -> None:
    """
    Orquesta el flujo de este módulo:
    - obtiene el precio,
    - lo guarda en el CSV
    - escribe log
    """
    try:
        price = fetch_btc_price_usd()
        append_price_row(price)
        print(f"Precio de BTC guardado correctamente: {price} USD")
    except Exception:
        # El detalle ya se guarda en logs; aquí solo avisamos en consola
        print("Error al obtener/guardar el precio de BTC. Revisa logs/app.log.")


if __name__ == "__main__":
    main()

