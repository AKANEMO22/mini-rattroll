import json
import os
import random
import time
from typing import Dict, Any, List

class SimulationService:
    def __init__(self, rec_service, state_file="data/drift_state.json", log_file="data/simulated_drift_log.json"):
        self.rec_service = rec_service
        self.state_file = state_file
        self.log_file = log_file
        
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        if not os.path.exists(self.state_file):
            self.reset_state()
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)
                
    def get_state(self) -> Dict[str, Any]:
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return self.reset_state()
        
    def reset_state(self) -> Dict[str, Any]:
        state = {"type": "None", "severity": 0.0}
        self.set_state(state)
        with open(self.log_file, 'w') as f:
            json.dump([], f)
        return state
        
    def set_state(self, state: Dict[str, Any]):
        with open(self.state_file, 'w') as f:
            json.dump(state, f)
            
    def get_logs(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                return json.load(f)
        return []

    def inject_drift(self, drift_type: str, severity: float):
        # Always clear previous data before a new test to ensure distinct charts
        if hasattr(self.rec_service, 'recent_events'):
            self.rec_service.recent_events.clear()
        else:
            self.rec_service.recent_scores.clear()
            
        if drift_type == "None":
            self.reset_state()
            return {"status": "success", "message": "Cleared all simulated data."}
            
        # Generate synthetic noise based on drift type
        noise_scores = []
        logs = []
        num_items = 200
        
        for i in range(num_items):
            user_id = random.randint(1000, 9999)
            movie_id = random.randint(1, 1000)
            
            if drift_type == "Preference Drift":
                # Suddenly rate everything terribly
                score = round(random.uniform(1.0, 2.0), 2)
            elif drift_type == "Interaction Drift":
                # Sparse and polarized
                score = random.choice([1.0, 5.0])
            elif drift_type == "Structural Drift":
                # Completely random noise destroying patterns
                score = round(random.uniform(1.0, 5.0), 2)
            else:
                score = round(random.uniform(1.0, 3.0), 2)
                
            noise_scores.append(score)
            logs.append({
                "timestamp": time.strftime('%H:%M:%S'),
                "user_id": user_id,
                "movie_id": movie_id,
                "score": score,
                "type": "Synthetic"
            })
            
        # Push into rec_service to trigger monitoring
        # We now use recent_events (Dict with cluster_id) instead of recent_scores (raw floats)
        synthetic_events = []
        for score in noise_scores:
            synthetic_events.append({
                "cluster_id": random.randint(0, 9),
                "score": score
            })
            
        if hasattr(self.rec_service, 'recent_events'):
            self.rec_service.recent_events.extend(synthetic_events)
            if len(self.rec_service.recent_events) > 1000:
                self.rec_service.recent_events = self.rec_service.recent_events[-1000:]
        else:
            self.rec_service.recent_scores.extend(noise_scores)
        
        # Save logs
        with open(self.log_file, 'w') as f:
            json.dump(logs, f)
            
        state = {
            "type": drift_type,
            "severity": severity
        }
        self.set_state(state)
        return {"status": "success", "message": f"Injected {len(noise_scores)} synthetic ratings."}
