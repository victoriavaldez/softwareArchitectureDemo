from typing import Callable, Dict, List, Any

class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[Any], None]):
        self.subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event_type: str, payload: Any):
        handlers = self.subscribers.get(event_type, [])
        for h in handlers:
            h(payload)

#singleton bus for the demo
event_bus = EventBus()
