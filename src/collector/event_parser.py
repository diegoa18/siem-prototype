import importlib
from src.utils.logger import logger
_logged_extractors = set()

def safe_str(value):
    try:
        return str(value)
    except Exception:
        return None

def parse_event(record):
    inserts = record.StringInserts or []

    parsed = {
        "event_id": safe_str(record.EventID),
        "record_number": safe_str(record.RecordNumber),
        "source": safe_str(record.SourceName),
        "time_generated": safe_str(getattr(record, "TimeGenerated", None)),
        "category": safe_str(record.EventCategory),
        "computer": safe_str(record.ComputerName),
        "message": inserts,
        "event_type": safe_str(record.EventType),
        "event_type_name": safe_str(getattr(record, "EventTypeName", None)),
    }

    try:
        event_id = int(record.EventID) & 0xFFFF
    except Exception:
        return parsed

    module_name = f"src.collector.extractors.windows_{event_id}"

    try:
        mod = importlib.import_module(module_name)

        if not hasattr(mod, "extract"):
            return parsed

        parsed_before = dict(parsed)
        parsed = mod.extract(record, parsed) or parsed

        if parsed != parsed_before and event_id not in _logged_extractors:
            added = [k for k in parsed.keys() if k not in parsed_before.keys()]
            logger.info(f"[debug] extractor windows_{event_id} aplicado. campos añadidos: {added}")
            _logged_extractors.add(event_id)

    except ModuleNotFoundError:
        pass
    except Exception as e:
        logger.error(f"[debug] extractor {module_name} falló: {e}")

    return parsed
