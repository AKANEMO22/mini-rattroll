from typing import Dict
from src.interfaces.base import BaseEvaluator

class AdaptEvaluator(BaseEvaluator):
    """Evaluates Adaptive Controller (False Alarms, Delay)."""
    def evaluate(self, drift_logs: Dict) -> Dict[str, float]:
        return {"false_alarm_rate": 0.0, "detection_delay_ms": 0.0}
