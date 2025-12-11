import logging
import sys
from src.config.config import LOG_FILE, LOG_DIR

#CONFIGURACION DE LOGGER
def setup_logger(name="SIEM", log_level=logging.DEBUG):
    #asegurar directorio de logs
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"[FATAL] No se pudo crear directorio {LOG_DIR}: {e}")
    
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.propagate = False #evitar duplicados

    if logger.hasHandlers():
        logger.handlers.clear()

    #formato del log
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    #handler consola (solo info o superior)
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)

    #handler archivo (debug, todo el detalle)
    try:
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"[ERROR] Fallo al configurar log en archivo: {e}")

    return logger

logger = setup_logger()