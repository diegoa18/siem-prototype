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


            if "event_id" in cond and event.get("event_id") == cond["event_id"]:
                alert = {
                    "rule": cond["name"],
                    "description": rule.get("description"),
                    "severity": rule.get("severity", "low"),
                    "event": event,
                }
                alerts.append(alert)

        return alerts