import json
import os
from typing import Dict, Any

class SimulationService:
    def __init__(self, state_file="data/drift_state.json"):
        self.state_file = state_file
        # Ensure dir exists
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        # Init default state if not exists
        if not os.path.exists(self.state_file):
            self.reset_state()
            
    def get_state(self) -> Dict[str, Any]:
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return self.reset_state()
        
    def reset_state(self) -> Dict[str, Any]:
        state = {"type": "None", "severity": 0.0}
        self.set_state(state)
        return state
        
    def set_state(self, state: Dict[str, Any]):
        with open(self.state_file, 'w') as f:
            json.dump(state, f)
            
    def inject_drift(self, drift_type: str, severity: float):
        state = {
            "type": drift_type,
            "severity": severity
        }
        self.set_state(state)
        return {"status": "success", "message": f"Injected {drift_type} with severity {severity}"}
