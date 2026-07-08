from typing import Dict, Any
from src.core.events import EventManager, Event

class SelectiveRetrainer:
    """Decides and executes retraining only for the faulty component."""
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        self.event_manager.subscribe("diagnosis_completed", self.execute_retrain)

    def execute_retrain(self, event: Event) -> None:
        faulty_component = event.payload.get("faulty_component")
        
        # Decision Logic (Selective Retraining)
        if faulty_component == "MF":
            # Retrain SVD, KMeans, ClusterLR sequentially
            self.event_manager.publish(Event(name="start_retraining", payload={"strategy": "retrain_all"}))
        elif faulty_component == "ClusterLR":
            # Only retrain LR and Meta, freeze MF embeddings
            self.event_manager.publish(Event(name="start_retraining", payload={"strategy": "retrain_ranking_only"}))
        else:
            self.event_manager.publish(Event(name="start_retraining", payload={"strategy": "retrain_all"}))
