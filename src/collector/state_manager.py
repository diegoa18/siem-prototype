import os
import json

class CollectorState:
    def __init__(self, base_dir):
        self.state_file = os.path.join(base_dir, "data", "collector_state.json")
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        self._state = self._load()

    def _load(self):
        if not os.path.exists(self.state_file):
            return {}
        
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
        

    def save(self):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self._state, f, indent=2)

    def get(self, log_type, default=0):
        return self._state.get(log_type, default)

    

    def update(self, new_data):
        self._state.update(new_data)
        self.save()