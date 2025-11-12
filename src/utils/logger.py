import logging
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "siem.log")

def setup_logger():
    if not os.path.exists("SIEM"):
        os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger("SIEM")
    logger.setLevel(logging.DEBUG)


    if logger.hasHandlers():
        logger.handlers.clear()

    
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)


    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()