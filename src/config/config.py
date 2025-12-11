import os
from pathlib import Path

#raiz
BASE_DIR = Path(__file__).resolve().parent.parent.parent

#directorios de datos
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
RULES_DIR = BASE_DIR / "rules"

#rutas de archivos
ALERT_FILE = DATA_DIR / "alerts.jsonl"
STATE_FILE = DATA_DIR / "collector_state.json"
LOG_FILE = LOG_DIR / "siem.log"

#asegurar que existan los directorios
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

def get_event_store_path(log_type: str) -> Path: #para tipo de log especifico
    return DATA_DIR / f"{log_type.lower()}_events.jsonl"