from typing import Dict, Any
from src.core.events import EventManager, Event

class ComponentImpactAnalyzer:
    """Diagnoses which component (MF, KMeans, LR) is causing the drift."""
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        self.event_manager.subscribe("drift_detected", self.diagnose)

    def diagnose(self, event: Event) -> None:
        # Evaluate embedding distance or cluster stability dynamically based on drift signal
        drift_score = event.payload.get("drift_score", 0.0)
        
        # Heuristic: If drift_score is very high, MF is faulty. Otherwise, ClusterLR.
        if drift_score > 0.5:
            faulty = "MF"
            reason = f"High Embedding Drift (Score: {drift_score:.2f} > 0.5)"
        else:
            faulty = "ClusterLR"
            reason = f"Moderate Ranking Drift (Score: {drift_score:.2f} <= 0.5)"
            
        diagnosis_result = {
            "faulty_component": faulty,
            "impact_score": min(1.0, drift_score * 2.0), # Normalize or scale impact score
            "reason": reason
        }
        self.event_manager.publish(Event(name="diagnosis_completed", payload=diagnosis_result))
