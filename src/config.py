import os
from pathlib import Path

# Raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Directorios de datos
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
RULES_DIR = BASE_DIR / "rules"

# Rutas de archivos
ALERT_FILE = DATA_DIR / "alerts.jsonl"
STATE_FILE = DATA_DIR / "collector_state.json"
LOG_FILE = LOG_DIR / "siem.log"

# Asegurar que existan los directorios
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

def get_event_store_path(log_type: str) -> Path:
    """Devuelve la ruta para almacenar eventos de un tipo de log específico."""
    return DATA_DIR / f"{log_type.lower()}_events.jsonl"