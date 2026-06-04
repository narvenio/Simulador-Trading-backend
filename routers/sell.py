from fastapi import APIRouter, Depends, HTTPException
from database import  SessionLocal
from sqlalchemy.orm import Session
from schemas import SellRequest, SellResponse
from services.market import  simulate_price
from services.portfolio_service import update_portafolio
import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db # mantener abierto la base de datos
    finally:
        db.close() # cerrar cuando ya no uses




@router.post("/sell")
def sell_asset(sell: SellRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == sell.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail= "Usuario No Encontrado")

    asset = db.query(models.Asset).filter(models.Asset.id == sell.asset_id).first()
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset no encontrado")
# se usa sell. porque lo estamos guardando directamente en el "user_id" y en "asset_id"
# porque tiene un formato que tiene ese tipo de dato

    portfolio_items = db.query(models.Portfolio).filter(models.Portfolio.user_id == user.id,
                                                         models.Portfolio.asset_id == asset.id).first()

    if portfolio_items is None:
        raise HTTPException(status_code=404, detail= "Usuario no tiene Asset")

    if portfolio_items.quantity < sell.quantity:
        raise HTTPException(status_code=400, detail="El usuario intenta vender mas de lo que tiene")


    sim_price = simulate_price(asset.price)
    total_cost = sim_price * sell.quantity


    user.balance += total_cost
    db.commit()
    db.refresh(user)

    snapshot = models.BalanceHistory (
        user_id = user.id,
        balance = user.balance
    )
    db.add(snapshot)
    db.commit()

    transaction = models.Transaction (
        user_id = user.id,
        asset_id = asset.id,
        quantity = sell.quantity,
        total_price = total_cost,
        type        = "SELL"
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    update_portafolio(db, user.id, asset.id, sell.quantity, "SELL")
# funcion que actualiza el portafolio, esos son los parametros que sigue y si no hay portafolio crea uno


    return SellResponse(
        transaction_id = transaction.id,
        user_id = user.id,
        asset_id = asset.id,
        quantity = sell.quantity,
        total_cost = total_cost,
        type= "SELL",
        remaining_balance = user.balance

    )