from typing import Dict, Any, List
from src.core.events import EventManager, Event

class BehaviorMonitor:
    """Listens to interaction streams and aggregates behavioral metrics."""
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        self.buffer: List[Dict[str, Any]] = []
        self.event_manager.subscribe("interaction_logged", self.on_interaction)

    def on_interaction(self, event: Event):
        # Buffer incoming interactions
        self.buffer.append(event.payload)
        
        # If buffer reaches threshold, trigger drift detection
        if len(self.buffer) >= 1000:
            self._trigger_detection()

    def _trigger_detection(self):
        # Extract features from buffer and publish event to Detector
        stats = {"recent_ctr": 0.04, "sample_size": len(self.buffer)}
        self.event_manager.publish(Event(name="trigger_drift_detection", payload=stats))
        self.buffer.clear()
