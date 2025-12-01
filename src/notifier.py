import os
import logging
from typing import Dict

import requests

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, "app.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [notifier] %(levelname)s: %(message)s",
)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def _check_config():
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise RuntimeError(
            "Faltan variables de entorno TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID."
        )


def send_report(stats: Dict[str, float], image_path: str) -> None:
    """
    Envía a Telegram un mensaje con estadísticas y la imagen de la gráfica.
    """
    _check_config()

    text = (
        "📈 *Reporte BTC Sentinel*\n\n"
        f"Promedio: `{stats['promedio']:.2f}` USD\n"
        f"Máximo: `{stats['maximo']:.2f}` USD\n"
        f"Mínimo: `{stats['minimo']:.2f}` USD\n"
        f"Registros: `{stats['registros']}`"
    )

    try:
        # Enviar mensaje de texto
        resp_msg = requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text,
                "parse_mode": "Markdown",
            },
            timeout=10,
        )
        resp_msg.raise_for_status()
        logging.info("Mensaje de texto enviado a Telegram.")

        # Enviar imagen
        if os.path.exists(image_path):
            with open(image_path, "rb") as img:
                resp_photo = requests.post(
                    f"{TELEGRAM_API_URL}/sendPhoto",
                    data={"chat_id": TELEGRAM_CHAT_ID},
                    files={"photo": img},
                    timeout=10,
                )
            resp_photo.raise_for_status()
            logging.info("Gráfica enviada a Telegram.")
        else:
            logging.warning(f"No se encontró la imagen para enviar: {image_path}")

    except Exception as e:
        logging.error(f"Error enviando reporte a Telegram: {e}")
        print("Error al enviar reporte a Telegram. Revisa logs/app.log.")
