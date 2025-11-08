import yaml
import glob

class RuleEngine:
    def __init__(self):
        self.rules = []
        for rule_file in glob.glob("rules/*.yaml"):
            with open(rule_file, "r", encoding="utf-8") as f:
                self.rules.append(yaml.safe_load(f))

    def evaluate(self, event):
        alerts = []
        for rule in self.rules:
            cond = rule.get("condition", {})


            if "event_id" in cond and str(event.get("event_id")) == str(cond["event_id"]):

                filtered_event = {
                    field: event.get(field, None)
                    for field in rule.get("fields", [])
                }

                alert = {
                    "rule": rule.get("name"),
                    "description": rule.get("description"),
                    "severity": rule.get("severity", "low"),
                    "time": event.get("time_generated"),
                    "event_id": event.get("event_id"),
                    "computer": event.get("computer"),
                    "details": filtered_event,
                }
                alerts.append(alert)

        return alerts