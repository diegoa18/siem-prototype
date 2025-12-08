import yaml
import glob
from collections import defaultdict
from src.common.schema import ParsedFields
from src.rules.rule_structures import RuleEventBuffer
from src.utils.logger import logger
from src.common.taxonomy import RuleCategory, RuleSeverity

class RuleEngine:
    def __init__(self):
        self.rules = []
        self.buffer = RuleEventBuffer() #abstraccion del buffer (para posible DB, ahi la pienso la vd)
        self._load_rules()

    #carga reglas desde archivos YAML
    def _load_rules(self):
        self.rules = []
        #validacion de taxonomia (categorias y severidades validas)
        valid_cats = {v for k,v in RuleCategory.__dict__.items() if not k.startswith('_')}
        valid_sevs = {v for k,v in RuleSeverity.__dict__.items() if not k.startswith('_')}

        for rule_file in glob.glob("rules/*.yaml"):
            try:
                with open(rule_file, "r", encoding="utf-8") as f:
                    rule_doc = yaml.safe_load(f)
                    if rule_doc:
                        #validacion de taxonomia (categorias y severidades validas)
                        cat = rule_doc.get("category")
                        if cat and cat not in valid_cats:
                            logger.warning(f"Regla '{rule_doc.get('name')}' usa categoria no estandar: '{cat}'")
                        
                        sev = rule_doc.get("severity")
                        if sev and sev not in valid_sevs:
                            logger.warning(f"Regla '{rule_doc.get('name')}' usa severidad no estandar: '{sev}'")

                        self.rules.append(rule_doc)
            except Exception as e:
                logger.error(f"Error cargando regla {rule_file}: {e}")

    #ayuda a obtener un campo del evento (soporta claves simples por ahora)
    def _get_field(self, event: dict, field_path: str):
        if field_path in event:
            return event[field_path]
        return None

    #evalua un evento contra todas las reglas cargadas
    def evaluate(self, event: dict):
        alerts = []
        
        #asegurar que tenemos timestamp
        event_time = event.get(ParsedFields.TIMESTAMP)
        if event_time is None:
            return []

        #optimizacion: ID de evento actual
        current_event_id = event.get(ParsedFields.WIN_SYSTEM_EVENT_ID)

        for rule in self.rules:
            cond = rule.get("condition", {})
            rule_id = rule.get("id", rule.get("name"))

            #filtrar por Event ID
            rule_ev_id = str(cond.get("event_id", ""))
            if rule_ev_id and rule_ev_id != str(current_event_id):
                 continue

            #otros filtros de campos (PENDIENTEEEEEEEEEEE)
            pass 
            
            #logica de umbral (threshold)
            if "threshold" not in cond:
                #regla sin estado (salta directo si coincide el ID)
                alert = self._build_alert(rule, event)
                alerts.append(alert)
                continue

            group_field = cond.get("group_by")
            threshold = cond.get("threshold")
            window = cond.get("timeframe_seconds", 60)

            if not group_field:
                continue

            #obtener valor para agrupar (podria ser el IP origen x ejemplo)
            group_value = self._get_field(event, group_field)
            if not group_value:
                continue

            #actualizar buffer
            self.buffer.add_event(rule_id, group_value, event_time, window)
            
            #ver si se supero el buffer
            if self.buffer.get_count(rule_id, group_value) > threshold:
                alert = self._build_alert(rule, event)
                #agregar info de correlacion a la alerta
                alert["correlation"] = {
                    "count": self.buffer.get_count(rule_id, group_value),
                    "timeframe_seconds": window,
                    "group_by": group_field,
                    "group_value": group_value
                }
                alerts.append(alert)

        return alerts
        

    #construye el objeto de alerta final
    def _build_alert(self, rule, event):
        #extraer campos interesantes definidos en la regla
        filtered_event = {}
        for key in rule.get("fields", []):
            val = self._get_field(event, key)
            if val is not None:
                filtered_event[key] = val

        return {
            "rule": rule.get("name"),
            "description": rule.get("description"),
            "severity": rule.get("severity", "low"),
            "category": rule.get("category"),
            "tags": rule.get("tags", []),
            "timestamp": event.get(ParsedFields.TIMESTAMP),
            "event_dump": filtered_event,  #subconjunto limpio
            "full_context": {
                "computer": event.get(ParsedFields.WIN_SYSTEM_COMPUTER),
                "event_id": event.get(ParsedFields.WIN_SYSTEM_EVENT_ID)
            }
        }