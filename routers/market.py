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
        id_crypto = asset.id
        nombre_crypto = asset.name
        simbolo_crypto = asset.symbol
        precio_base = asset.price
        precio_simulado = simulate_price(precio_base)
        simulated = precio_simulado
        
# recorremos todos los assets, lo guardamos en "asset" y definimos el precio simulado

        market_data.append(
            MarketItemResponse(
                
                asset_id = id_crypto,
                name = nombre_crypto,
                symbol = simbolo_crypto,
                base_price = precio_base,
                simulated_price = simulated

        )
    )

    return MarketResponse(market = market_data)
