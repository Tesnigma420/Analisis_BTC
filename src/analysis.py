import os
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# Rutas del proyecto
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "btc_prices.csv")
OUTPUT_PLOT = os.path.join(BASE_DIR, "data", "btc_chart.png")


def load_data():
    """
    Carga el histórico de precios de BTC desde el CSV.
    """
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(
            "No existe btc_prices.csv. Ejecuta primero collector.py para generar datos."
        )

    df = pd.read_csv(DATA_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def basic_stats(df):
    """
    Calcula estadísticas simples sobre el precio.
    """
    return {
        "promedio": df["price_usd"].mean(),
        "maximo": df["price_usd"].max(),
        "minimo": df["price_usd"].min(),
        "registros": len(df),
    }


def plot_data(df):
    """
    Genera una gráfica simple del precio de BTC en el tiempo.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(df["timestamp"], df["price_usd"], marker="o")
    plt.title("Precio histórico de BTC")
    plt.xlabel("Tiempo")
    plt.ylabel("Precio (USD)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT)
    plt.close()


def main():
    df = load_data()

    stats = basic_stats(df)
    print("Estadísticas básicas BTC:")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    plot_data(df)
    print(f"Gráfica guardada en: {OUTPUT_PLOT}")


if __name__ == "__main__":
    main()
