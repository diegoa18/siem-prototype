import json
import os
from src.utils.file_utils import ensure_dir
from src.config import ALERT_FILE, DATA_DIR

class AlertManager:
    def __init__(self):
        ensure_dir(DATA_DIR)
        self.file = ALERT_FILE
        if not os.path.exists("data"):
            os.makedirs("data")

    
    def save_alerts(self, alerts):
        with open(self.file, "a", encoding="utf-8") as f:
            for alert in alerts:

                serializable = {
                    k: v for k, v in alert.items()
                    if isinstance(v, (str, int, float, list, dict, bool, type(None)))
                }

                f.write(json.dumps(serializable) + "\n")
                self.bonito(alert)


    def bonito(self, alert):
        event = alert.get("event", {})
        print("\n" + "="*50)
        print(f"regla:        {alert.get('rule')}")
        print(f"descripcion:  {alert.get('description')}")
        print(f"severidad:    {alert.get('severity').upper()}")
        print("detalles del evento:")
        print(f" - equipo:       {event.get('computer', 'N/A')}")
        print(f" - hora:         {event.get('time_generated', 'N/A')}")

        msg = event.get("message")
        if msg:
            msg_str = str(msg)
            if len(msg_str) > 120:
                msg_str = msg_str[:120] + "... (truncado)"
            print(f" - mensaje: {msg_str}")