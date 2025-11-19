from .event_bus import event_bus
from .price_fetcher import PriceUpdateEvent

ALERT_LOG: list[str] = []

def handle_price_update(event: PriceUpdateEvent):
    if event.new_price < event.old_price:
        msg = (
            f"[ALERT] {event.artist} in {event.city}: "
            f"price dropped from {event.old_price} to {event.new_price}"
        )
        ALERT_LOG.append(msg)
        print(msg)  #in the real working model, it'd send an email or push notification

def register_handlers():
    event_bus.subscribe("price.update", handle_price_update)
