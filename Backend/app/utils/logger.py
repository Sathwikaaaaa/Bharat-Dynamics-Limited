import logging
import os

from app.utils.config import OUTPUT_DIR


LOG_DIR = os.path.join(OUTPUT_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)


LOG_FILE = os.path.join(
    LOG_DIR,
    "application.log"
)


def get_logger(name):
    """
    Create and return a configured application logger.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    console_handler = logging.StreamHandler()

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger