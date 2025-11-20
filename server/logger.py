import logging
from logging.handlers import RotatingFileHandler
import os
import requests

SUMO_ENDPOINT = os.getenv("SUMO_ENDPOINT")
class SumoLogicHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        try:
            requests.post(SUMO_ENDPOINT, data=log_entry.encode("utf-8"))
        except Exception:
            pass  # don't crash app on logging failure


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logging(ci_mode=False):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG if ci_mode else logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if not ci_mode:
        file_handler = RotatingFileHandler(
            f"{LOG_DIR}/server.log",
            maxBytes=5_000_000,
            backupCount=5
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    sumo_handler = SumoLogicHandler()
    sumo_handler.setFormatter(formatter)
    logger.addHandler(sumo_handler)
    
    return logger