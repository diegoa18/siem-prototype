import yaml
import glob
from collections import defaultdict, deque
import time
class RuleEngine:
    def __init__(self):
        self.rules = []
        self.buffers = defaultdict(lambda: defaultdict(deque)) #buffers[rule_id][group_value] -> deque de timestamps
        for rule_file in glob.glob("rules/*.yaml"):
            with open(rule_file, "r", encoding="utf-8") as f:
                self.rules.append(yaml.safe_load(f))

    def evaluate(self, event):
        alerts = []

        event_id = str(event.get("event_id"))
        event_time = time.time()

        for rule in self.rules:
            cond = rule.get("condition", {})
            rule_id = rule.get("id", rule.get("name"))


            if "event_id" in cond and event_id != str(cond["event_id"]):
                continue

            if "threshold" not in cond:
                alert = self._build_alert(rule, event)
                alerts.append(alert)
                continue

            group_field = cond.get("group_by")
            threshold = cond.get("threshold")
            window = cond.get("timeframe_seconds", 60)

            if not group_field:
                continue

            group_value = event.get(group_field)
            if not group_value:
                continue

            dq = self.buffers[rule_id][group_value]
            dq.append(event_time)

            while dq and event_time - dq[0] > window:
                dq.popleft()

            if len(dq) > threshold:
                alert = self._build_alert(rule, event)
                alert["correlation"] = {
                    "count": len(dq),
                    "timeframe_seconds": window,
                    "group_by": group_field,
                    "group_value": group_value
                }
                alerts.append(alert)


        return alerts


    def _build_alert(self, rule, event):
        filtered_event = {
            key: event.get(key)
            for key in rule.get("fields", [])
        }

        return {
            "rule": rule.get("name"),
            "description": rule.get("description"),
            "severity": rule.get("severity", "low"),
            "category": rule.get("category"),
            "tags": rule.get("tags", []),

            "event": {
                "time_generated": event.get("time_generated"),
                "computer": event.get("computer"),
                "event_id": event.get("event_id"),
                **filtered_event
            }
        }