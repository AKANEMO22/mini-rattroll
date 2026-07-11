from typing import Dict, Any, Optional
from scipy import stats
from src.interfaces.base import BaseDriftDetector
from src.core.events import EventManager, Event

class StatisticalDriftDetector(BaseDriftDetector):
    """Applies statistical tests (KS-Test) to detect data drift."""
    def __init__(self, event_manager: Optional[EventManager] = None):
        self.event_manager = event_manager
        if self.event_manager:
            self.event_manager.subscribe("trigger_drift_detection", self.on_trigger)

    def on_trigger(self, event: Event):
        actual_dist = event.payload.get("actual_dist", [])
        expected_dist = event.payload.get("expected_dist", [])
        
        if not actual_dist or not expected_dist:
            return
            
        result = self.detect(actual_dist, expected_dist)
        
        if result["is_drift"] and self.event_manager:
            self.event_manager.publish(Event(name="drift_detected", payload=result))

    def detect(self, actual: Any, expected: Any) -> Dict[str, Any]:
        # Kolmogorov-Smirnov test for continuous distributions
        if not actual or not expected:
            return {"is_drift": False, "p_value": 1.0, "drift_score": 0.0, "method": "KS-Test"}
            
        statistic, p_value = stats.ks_2samp(actual, expected)
        
        is_drift = bool(p_value < 0.05)
        return {
            "is_drift": is_drift,
            "p_value": round(float(p_value), 4),
            "drift_score": round(float(statistic), 4),
            "method": "KS-Test"
        }
