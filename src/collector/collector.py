import win32evtlog
import json
from typing import List, Tuple, Dict, Any
from src.config import get_event_store_path
from .state_manager import CollectorState
from .event_parser import parse_event
from src.rules.rule_engine import RuleEngine
from src.alerts.alert_manager import AlertManager
from src.utils.logger import logger

LOG_SOURCES = ["System", "Security"]

class Collector: #recoleccion de logs de windows  
    def __init__(self):
        self.state = CollectorState()
        self.rule_engine = RuleEngine()
        self.alert_manager = AlertManager()
        
    #lee nuevos eventos de distinta fuente desde el ultimo ID visto
    def collect_from_log(self, log_type: str, last_seen_id: int) -> Tuple[List[Dict[str, Any]], int]:
        events = []
        max_seen = last_seen_id
        
        #IMPORTANTE -> leer hacia ADELANTE (viejo -> nuevo) para que las reglas temporales funcionen bien.
        flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        
        try:
            #intentar abrir el log
            handle = win32evtlog.OpenEventLog(None, log_type)
        except Exception as e:
            logger.error(f"Fallo al abrir log de eventos {log_type}: {e}")
            return [], last_seen_id

        #bucle de lectura
        read = True
        while read:
            try:
                records = win32evtlog.ReadEventLog(handle, flags, 0)
                if not records:
                    read = False
                    break

                #iterar sobre los eventos leidos
                for record in records:
                    if record.RecordNumber <= last_seen_id:
                        read = False
                        break

                    parsed = parse_event(record)
                    events.append(parsed)
                    max_seen = max(max_seen, record.RecordNumber)
            #prevenir loops infinitos
            except Exception as e:
                logger.error(f"Error leyendo log de eventos {log_type}: {e}")
                read = False

        win32evtlog.CloseEventLog(handle)
        return events, max_seen
    
    #iterar sobre todas las fuentes de logs configuradas y recolectar nuevos eventos
    def collect_all(self):
        updated_state = {}

        for log_type in LOG_SOURCES:
            last_seen = self.state.get_last_seen(log_type)
            events, max_seen = self.collect_from_log(log_type, last_seen)

            if events:
                logger.info(f"[+] {len(events)} nuevos eventos de '{log_type}' (último={last_seen} -> {max_seen})")
                
                #guardar evento
                store_path = get_event_store_path(log_type)
                try:
                    with open(store_path, "a", encoding="utf-8") as f:
                        for e in events:
                            f.write(json.dumps(e) + "\n")
                except Exception as e:
                    logger.error(f"Fallo al escribir eventos en {store_path}: {e}")

                #procesar las reglas
                for e in events:
                    alerts = self.rule_engine.evaluate(e)
                    if alerts:
                        self.alert_manager.save_alerts(alerts)
                        logger.warning(f"[!] ALERTA generada: {len(alerts)} para evento {e.get('event_id')}")

            updated_state[log_type] = max_seen

        self.state.save(updated_state)


def run_collector():
    collector = Collector()
    collector.collect_all()
