import importlib
import time
from typing import Dict, Any, Optional
from datetime import datetime
from src.utils.logger import logger
from src.common.schema import ParsedFields

_logged_extractors = set() #evitar spam de logs

#convierte valor a string de forma segura (maneja nulos)
def safe_str(value: Any) -> Optional[str]:
    try:
        if value is None:
            return None
        return str(value)
    except Exception:
        return None

#procesa el campo TimeGenerated de windows y lo pasa a float (epoch)
def parse_time_generated(time_obj: Any) -> float:
    try:
        #win32evtlog suele devolver un objeto datetime
        if hasattr(time_obj, 'timestamp'):
             return time_obj.timestamp()
        #si llega como string
        if isinstance(time_obj, str):
             dt = datetime.fromisoformat(time_obj)
             return dt.timestamp()
        #si todo falla, usar tiempo actual
        return time.time()
    except Exception:
        return time.time()

#parsea un registro de evento crudo a un diccionario estandarizado
def parse_event(record: Any) -> Dict[str, Any]:
    inserts = record.StringInserts or []
    
    #obtener timestamp real del evento
    raw_time = getattr(record, "TimeGenerated", None)
    event_timestamp = parse_time_generated(raw_time)

    #construir diccionario base usando los campos estandar (ParsedFields)
    event_id_val = safe_str(record.EventID)
    try:
        #quitar los bits extra mediante masking
        win_id = int(record.EventID) & 0xFFFF
    except Exception:
        win_id = 0
        
    parsed = {
        ParsedFields.TIMESTAMP: event_timestamp, #timestamp real del evento
        ParsedFields.WIN_SYSTEM_EVENT_ID: str(win_id), #ID del evento (windows)
        ParsedFields.WIN_SYSTEM_CHANNEL: safe_str(record.SourceName), #canal del evento
        ParsedFields.WIN_SYSTEM_COMPUTER: safe_str(record.ComputerName), #nombre del computador
        ParsedFields.WIN_SYSTEM_RECORD_NUMBER: safe_str(record.RecordNumber), #numero de registro
        ParsedFields.EVENT_CATEGORY: safe_str(record.EventCategory), #categoria del evento
        ParsedFields.MESSAGE: inserts, #mensaje del evento

        #campos extra (debug o legado)
        "event_type": safe_str(record.EventType), #tipo de evento
    }

    #extraccion dinamica (si existe un extractor para este ID)
    module_name = f"src.collector.extractors.windows_{win_id}"
    try:
        mod = importlib.import_module(module_name)
        if hasattr(mod, "extract"):
            #el extractor modifica el diccionario 'parsed' agregando campos extra
            mod.extract(record, parsed)
            
            #loguear solo la primera vez que usamos este extractor
            if win_id not in _logged_extractors:
                logger.debug(f"Extractor {module_name} aplicado correctamente.")
                _logged_extractors.add(win_id)
                
    except ModuleNotFoundError:
        pass #no pasa nada si no hay extractor :p
    except Exception as e:
        logger.error(f"Extractor {module_name} fallo: {e}")

    return parsed
