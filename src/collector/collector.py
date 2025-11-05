import win32evtlog
import json
import os
from .state_manager import CollectorState
from .event_parser import parse_event

LOG_SOURCES = ["System", "Security"]

class Collector:
    def __init__(self):
        self.state = CollectorState()

    def collect_from_log(self, log_type, last_seen_id):
        events = []

        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        handle = win32evtlog.OpenEventLog(None, log_type)

        read = True
        max_seen = last_seen_id


        while read:
            records = win32evtlog.ReadEventLog(handle, flags, 0)
            if not records:
                read = False
                break

            for record in records:
                if record.RecordNumber <= last_seen_id:
                    read = False
                    break

                parsed = parse_event(record)
                events.append(parsed)
                max_seen = max(max_seen, record.RecordNumber)

        win32evtlog.CloseEventLog(handle)
        return events, max_seen
    

    
    def collect_all(self):
        updated_state = {}

        for log_type in LOG_SOURCES:
            last_seen = self.state.get_last_seen(log_type)
            events, max_seen = self.collect_from_log(log_type, last_seen)

            print(f"[+] {len(events)} eventos nuevos desde '{log_type}' (last={last_seen} -> {max_seen})")

            updated_state[log_type] = max_seen

            if events:
                if not os.path.exists("data"):
                    os.makedirs("data")

                with open(f"data/{log_type.lower()}_events.jsonl", "a", encoding="utf-8") as f:
                    for e in events:
                        f.write(json.dumps(e) + "\n")

        self.state.save(updated_state)


def run_collector():
    collector = Collector()
    collector.collect_all()
