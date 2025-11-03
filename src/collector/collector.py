import os
import json
from datetime import datetime
import win32evtlog
from src.collector.state_manager import CollectorState


class EventCollector:
    LOG_TYPES = ["System", "Application"]
    MAX_PER_LOG = 500


    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, "data", "logs_raw")
        os.makedirs(self.data_dir, exist_ok=True)

        self.state = CollectorState(base_dir)


    def collect_all(self):
        all_events = []
        updated_state = {}

        for log_type in self.LOG_TYPES:
            last_seen = self.state.get(log_type)
            events, max_seen = self._collect_from_log(log_type, last_seen)

            if events:
                print(f"[+] {len(events)} eventos nuevos leidos desde '{log_type}' "
                      f"(last_seen={last_seen} -> max_seen={max_seen})")
                all_events.extend(events)

            else:
                print(f"[.] no hay eventos nuevos en '{log_type}' (last_seen={last_seen})")

            updated_state[log_type] = max(self.state.get(log_type, 0), max_seen or 0)

        if all_events:
            self._save_to_file(all_events)
            self.state.update(updated_state)
        else:
            print("[*] no se genero el archivo (no hubo eventos nuevos)")

        
    def _collect_from_log(self, log_type, last_seen_record):
        server = "localhost"
        handle = win32evtlog.OpenEventLog(server, log_type)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

        collected = []
        total = 0
        max_record_seen = last_seen_record or 0

        while True:
            records = win32evtlog.ReadEventLog(handle, flags, 0)
            if not records:
                break

            for event in records:
                total += 1
                rn = getattr(event, "RecordNumber", None)

                if rn is None or last_seen_record is None or rn > last_seen_record:
                    normalized = self._normalize_event(event, log_type)
                    collected.append(normalized)
                    if rn and rn > max_record_seen:
                        max_record_seen = rn

                if total >= self.MAX_PER_LOG:
                    break

            if total >= self.MAX_PER_LOG:
                break

        win32evtlog.CloseEventLog(handle)
        return collected, max_record_seen

    def _normalize_event(self, event, log_type):
        try:
            record_number = int(event.RecordNumber)
        except Exception:
            record_number = None


        try:
            evt_time = event.TimeGenerated.Format()
        except Exception:
            evt_time = None
        message = None


        try:
            if event.StringInserts:
                message = " | ".join([str(s) for s in event.StringInserts if s is not None])
        except Exception:
            message = None



        return {
            "log_type": log_type,
            "record_number": record_number,
            "event_id": int(event.EventID) & 0xFFFF,
            "source": str(getattr(event, "SourceName", "")),
            "time_generated": evt_time,
            "computer_name": str(getattr(event, "ComputerName", "")),
            "category": str(getattr(event, "EventCategory", "")),
            "message": message,
        }

    def _save_to_file(self, events):
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        out_file = os.path.join(self.data_dir, f"logs_{ts}.json")


        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(events, f, indent=2, ensure_ascii=False)


        print(f"[+] {len(events)} eventos guardados en {out_file}")