from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List

from ..services.price_fetcher import publish_price_update
from ..services.notifier import register_handlers, ALERT_LOG

app = FastAPI(title="Ticket Price Tracker - Event Based")

class Concert(BaseModel):
    id: int
    artist: str
    city: str
    date: str
    best_price: float

class PriceChangeRequest(BaseModel):
    concert_id: int
    new_price: float

CONCERTS: Dict[int, Concert] = {
    1: Concert(id=1, artist="Taylor Swift", city="Arlington", date="2026-05-01", best_price=250.0),
    2: Concert(id=2, artist="Olivia Rodrigo", city="Houston", date="2026-06-10", best_price=180.0),
}

#register event handlers when app starts
register_handlers()

@app.get("/concerts", response_model=List[Concert])
def list_concerts():
    return list(CONCERTS.values())

@app.post("/price_change")
def price_change(req: PriceChangeRequest):
    concert = CONCERTS.get(req.concert_id)
    if concert is None:
        return {"status": "error", "message": "Concert not found"}

    old_price = concert.best_price
    concert.best_price = req.new_price
    CONCERTS[req.concert_id] = concert

    #difference from client-server!
    #instead of directly doing it all, it publishes an event
    publish_price_update(
        concert_id=concert.id,
        artist=concert.artist,
        city=concert.city,
        old_price=old_price,
        new_price=req.new_price,
    )

    return {"status": "ok", "old_price": old_price, "new_price": req.new_price}

@app.get("/alerts")
def get_alerts():
    return {"alerts": ALERT_LOG}
