import json
from typing import Dict, Any
from src.config.config import STATE_FILE
from src.utils.logger import logger


#gestionar estado del colector
class CollectorState:
    
    def __init__(self):
        self.state: Dict[str, int] = {}
        self._load_state()

    #cargar estado
    def _load_state(self):
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    self.state = json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Archivo de estado corrupto en {STATE_FILE}. Iniciando con estado vacío.")
                self.state = {}
            except Exception as e:
                logger.error(f"Fallo al cargar archivo de estado: {e}")
                self.state = {}
        else:
            logger.info("No se encontró estado previo. Iniciando desde cero.")
            self.state = {}

    #retornar ultimo numero de registro visto
    def get_last_seen(self, log_type: str) -> int:
        return self.state.get(log_type, 0)

    #actualizar y guardar el estado
    def save(self, new_state: Dict[str, int]):
        self.state.update(new_state)
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            logger.error(f"Fallo al guardar archivo de estado: {e}")