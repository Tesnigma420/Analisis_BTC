import logging
import os

from collector import main as collector_main
from analysis import main as analysis_main
from notifier import send_report

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, "app.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [run] %(levelname)s: %(message)s",
)


def main():
    logging.info("===== Ejecución BTC Sentinel iniciada =====")
    try:
        # 1. Recolectar nuevo dato
        collector_main()

        # 2. Analizar datos y generar gráfica
        stats, plot_path = analysis_main()

        # 3. Enviar reporte a Telegram
        send_report(stats, plot_path)

        logging.info("Ejecución completada correctamente.")
        print("BTC Sentinel ejecutado correctamente. Revisa tu Telegram.")
    except Exception as e:
        logging.error(f"Error en ejecución principal: {e}")
        print("Error en BTC Sentinel. Revisa logs/app.log.")


if __name__ == "__main__":
    main()
