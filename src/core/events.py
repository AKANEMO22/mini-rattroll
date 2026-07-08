from typing import Callable, Dict, List, Any
from dataclasses import dataclass

@dataclass
class Event:
    name: str
    payload: Dict[str, Any]

class EventManager:
    """Pub/Sub Event Manager for Adaptive Controller."""
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Event], None]]] = {}

    def subscribe(self, event_name: str, handler: Callable[[Event], None]):
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)

    def publish(self, event: Event):
        if event.name in self._subscribers:
            for handler in self._subscribers[event.name]:
                handler(event)
