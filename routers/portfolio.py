from fastapi import APIRouter, Depends
from database import  SessionLocal
from sqlalchemy.orm import Session
from typing import List
from schemas import PortfolioItemResponse
import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db # mantener abierto la base de datos
    finally:
        db.close() # cerrar cuando ya no uses



@router.get("/portafolio/{user_id}", response_model= List[PortfolioItemResponse])
def get_portfolio(user_id: int, db: Session = Depends(get_db)):

    items = db.query(models.Portfolio).filter(models.Portfolio.user_id == user_id).all()
# creamos una variale que consulte dentro de la tabla de portfolio y filtre sus usuarios y que sea igual al user que buscamos

    response = []

    for item in items:
        asset = db.query(models.Asset).filter(models.Asset.id == item.asset_id).first()
# recorremos la variable anterior en "item" y creamos otra variable que consulte en la tabla de "Asset"
# y que compare y verifique sea igual el id del asset con el asset_id de la tabla "portfolio" de nuestro usuario a buscar

        total_value = item.quantity * asset.price

        response.append(
            PortfolioItemResponse(
                asset_id = asset.id,
                asset_name = asset.name,
                symbol     = asset.symbol,
                quantity = item.quantity,
                current_price = asset.price,
                total_value = total_value

        )
    )
    return response