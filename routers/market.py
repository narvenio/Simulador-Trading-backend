from fastapi import APIRouter, Depends
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import MarketResponse, MarketItemResponse
from services.market import  simulate_price
import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db # mantener abierto la base de datos
    finally:
        db.close() # cerrar cuando ya no uses

@router.get("/market", response_model=MarketResponse)
def get_market(db: Session = Depends(get_db)):
    assets = db.query(models.Asset).all()

    market_data = []

    for asset in assets:
        simulated = simulate_price(asset.price)
# recorremos todos los assets, lo guardamos en "asset" y definimos el precio simulado

        market_data.append(
            MarketItemResponse(
                asset_id = asset.id,
                name = asset.name,
                symbol = asset.symbol,
                base_price = asset.price,
                simulated_price = simulated

        )
    )

    return MarketResponse(market = market_data)
