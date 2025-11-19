from dataclasses import dataclass
from .event_bus import event_bus

@dataclass
class PriceUpdateEvent:
    concert_id: int
    artist: str
    city: str
    old_price: float
    new_price: float

def publish_price_update(concert_id: int, artist: str, city: str, old_price: float, new_price: float):
    event = PriceUpdateEvent(
        concert_id=concert_id,
        artist=artist,
        city=city,
        old_price=old_price,
        new_price=new_price,
    )
    event_bus.publish("price.update", event)
