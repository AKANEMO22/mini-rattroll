import pytest
from src.adaptation.controller import AdaptiveController, ControllerState
from src.core.events import EventManager, Event

def test_controller_initial_state():
    em = EventManager()
    controller = AdaptiveController(em)
    assert controller.state == ControllerState.IDLE

def test_controller_drift_detected_transition():
    em = EventManager()
    controller = AdaptiveController(em)
    
    # Simulate drift detection event
    em.publish(Event(name="drift_detected", payload={"is_drift": True}))
    
    # After the mock synchronous transitions, state should be UPDATING
    assert controller.state == ControllerState.UPDATING
