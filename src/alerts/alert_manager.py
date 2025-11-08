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
                self.bonito(alert)

    def bonito(self, alert):
        print("\n" + "="*50)
        print(f"regla:        {alert.get('rule')}")
        print(f"descripcion:  {alert.get('description')}")
        print(f"severidad:    {alert.get('severity').upper()}")
        event = alert.get("event", {})
        print("detalles del evento:")
        print(f" - equipo:       {event.get('computer', 'N/A')}")
        print(f" - hora:         {event.get('time_generated', 'N/A')}")

        msg = event.get("message")
        if msg:
            msg_str = str(msg)
            if len(msg_str) > 120:
                msg_str = msg_str[:120] + "... (truncado)"
            print(f" - mensaje: {msg_str}")