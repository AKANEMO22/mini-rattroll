import os
import json
from datetime import datetime
from typing import Dict, Any

class ExperimentTracker:
    """Logs parameters, metrics, and models for MLflow-like tracking."""
    def __init__(self, base_path: str):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)
        self.current_run = None

    def start_run(self, run_name: str):
        self.current_run = {
            "run_id": datetime.utcnow().strftime("%Y%m%d_%H%M%S"),
            "name": run_name,
            "metrics": {},
            "params": {}
        }

    def log_metric(self, key: str, value: float):
        if self.current_run:
            self.current_run["metrics"][key] = value

    def log_param(self, key: str, value: Any):
        if self.current_run:
            self.current_run["params"][key] = value

    def end_run(self):
        if self.current_run:
            run_file = os.path.join(self.base_path, f"{self.current_run['run_id']}.json")
            with open(run_file, 'w') as f:
                json.dump(self.current_run, f)
            self.current_run = None
