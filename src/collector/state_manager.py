import json
import os
STATE_FILE = "data/collector_state.json"


class CollectorState:
    def __init__(self):
        if not os.path.exists("data"):
            os.makedirs("data")

        
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                self.state = json.load(f)

        else:
            self.state = {}


    def get_last_seen(self, log_type):
        return self.state.get(log_type, 0)
    


    def save(self, new_state):
        self.state.update(new_state)
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)