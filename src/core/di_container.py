from typing import Dict, Type, Any, Callable

class DIContainer:
    """Simple Dependency Injection Container."""
    def __init__(self):
        self._services: Dict[Type, Any] = {}
        self._factories: Dict[Type, Callable[[], Any]] = {}

    def register(self, interface: Type, implementation: Any):
        self._services[interface] = implementation

    def register_factory(self, interface: Type, factory: Callable[[], Any]):
        self._factories[interface] = factory

    def resolve(self, interface: Type) -> Any:
        if interface in self._services:
            return self._services[interface]
        if interface in self._factories:
            return self._factories[interface]()
        raise KeyError(f"No implementation registered for {interface}")
