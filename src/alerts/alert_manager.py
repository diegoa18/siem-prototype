import json
import os
from src.utils.file_utils import ensure_dir
from src.config import ALERT_FILE, DATA_DIR
from src.utils.logger import logger

class AlertManager:
    def __init__(self):
        ensure_dir(DATA_DIR)
        self.file = ALERT_FILE
        if not os.path.exists("data"):
            os.makedirs("data")

    
    def save_alerts(self, alerts):
        if not alerts:
            logger.debug("no hay alertas para guardar")
            return


        with open(self.file, "a", encoding="utf-8") as f:
            for alert in alerts:

                serializable = {
                    k: v for k, v in alert.items()
                    if isinstance(v, (str, int, float, list, dict, bool, type(None)))
                }

                f.write(json.dumps(serializable) + "\n")
                logger.info(f"Alerta guardada: {alert.get('rule')} - {alert.get('severity').upper()}")
                self.bonito(alert)


    def bonito(self, alert):
        event = alert.get("event", {})
        rule = alert.get("rule", "N/A")
        desc = alert.get("description", "N/A")
        sev = alert.get("severity", "unknown").upper()

        equipo = event.get("computer", "N/A")
        hora = event.get("time_generated", "N/A")
        msg = event.get("message", "")

        if msg and len(msg) > 100:
            msg = msg[:100] + "... (truncado)"

        formatted = (
            "══════════════════════════════════════════════════════════════════════\n"
            " [!] ALERTA DETECTADA\n"
            " ===============================================================\n"
            f" REGLA:        {rule}\n"
            f" DESCRIPCIÓN:  {desc}\n"
            f" SEVERIDAD:    {sev}\n"
            f" EQUIPO:       {equipo}\n"
            f" HORA:         {hora}\n"
        )

        if msg:
            formatted += f" MENSAJE:      {msg}\n"

        formatted += "══════════════════════════════════════════════════════════════════════"

        logger.warning(formatted)