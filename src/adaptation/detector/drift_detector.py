from typing import Dict, Any
from scipy import stats
from src.interfaces.base import BaseDriftDetector
from src.core.events import EventManager, Event

class StatisticalDriftDetector(BaseDriftDetector):
    """Applies statistical tests (KS-Test, PSI) to detect data drift."""
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        self.event_manager.subscribe("trigger_drift_detection", self.on_trigger)

    def on_trigger(self, event: Event):
        # In real code: actual = event.payload, expected = get_baseline()
        actual_dist = [0.1] * 100 # Mock
        expected_dist = [0.12] * 100 # Mock
        
        result = self.detect(actual_dist, expected_dist)
        if result["is_drift"]:
            self.event_manager.publish(Event(name="drift_detected", payload=result))

    def detect(self, actual: Any, expected: Any) -> Dict[str, Any]:
        # Kolmogorov-Smirnov test for continuous distributions
        statistic, p_value = stats.ks_2samp(actual, expected)
        
        is_drift = p_value < 0.05
        return {
            "is_drift": is_drift,
            "p_value": float(p_value),
            "drift_score": float(statistic),
            "method": "KS-Test"
        }
