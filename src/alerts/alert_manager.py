import json
import os

class AlertManager:
    def __init__(self):
        self.file = "data/alerts.jsonl"
        if not os.path.exists("data"):
            os.makedirs("data")

    
    def save_alerts(self, alerts):
        with open(self.file, "a", encoding="utf-8") as f:
            for alert in alerts:
                f.write(json.dumps(alert) + "\n")