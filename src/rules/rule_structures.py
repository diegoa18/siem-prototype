from typing import Any, Dict, List, Optional
from collections import deque
import time

#clase para manejar el buffer de eventos (ventana de tiempo)
class RuleEventBuffer:
    def __init__(self):
        #almacenamiento -> {rule_id:{group_key: deque(timestamps)}}
        self._store: Dict[str, Dict[str, deque]] = {}

    #agrega un evento al buffer
    def add_event(self, rule_id, group_key, timestamp, window_seconds):
        if rule_id not in self._store:
            self._store[rule_id] = {}
        if group_key not in self._store[rule_id]:
            self._store[rule_id][group_key] = deque()
        
        dq = self._store[rule_id][group_key]
        dq.append(timestamp)
        
        #limpieza (Watermark): borrar eventos mas viejos que la ventana
        min_time = timestamp - window_seconds
        
        while dq and dq[0] < min_time:
            dq.popleft()

    #obtiene la cantidad de eventos en la ventana actual
    def get_count(self, rule_id: str, group_key: str) -> int:
        if rule_id in self._store and group_key in self._store[rule_id]:
            return len(self._store[rule_id][group_key])
        return 0

    #limpia datos de una regla
    def clear_rule(self, rule_id: str):
        if rule_id in self._store:
            del self._store[rule_id]
