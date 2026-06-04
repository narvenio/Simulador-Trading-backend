from fastapi import APIRouter, Depends, HTTPException
from database import  SessionLocal
from sqlalchemy.orm import Session
from schemas import BuyRequest, BuyResponse
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

@router.post("/buy")
def buy_asset(buy: BuyRequest, db: Session = Depends(get_db) ):

    user = db.query(models.User).filter(models.User.id == buy.user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail= "No se consiguio al usuario")

    asset = db.query(models.Asset). filter(models.Asset.id == buy.asset_id).first()

    if asset is None:
        raise HTTPException(status_code=404, detail="No se consiguio Asset")
# usamos buy.user_id y buy.asset_id porque "buy" es la variable que declaramos y tiene el formato
# de "BuyRequest", esta consultado en la base de datos que user_id sea igual al user_id de BuyRequest
# mismo caso que en asset_id con buy.asset_id
    sim_price = simulate_price(asset.price)
    total_cost = sim_price * buy.quantity

    if user.balance < total_cost:
        raise HTTPException(status_code= 400, detail="Saldo Insuficiente")

    user.balance -= total_cost
    db.commit()
    db.refresh(user)
    print("Saldo Insuficiente")

    snapshot = models.BalanceHistory (
        user_id = user.id,
        balance = user.balance
    )
    db.add(snapshot)
    db.commit()
    transaction = models.Transaction(
        user_id = user.id,
        asset_id = asset.id,
        quantity = buy.quantity,
        total_price = total_cost,
        type         = "BUY"
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)
# guardamos la transaccion de la compra en la base de datos...

    update_portafolio(db, user.id, asset.id, buy.quantity, "BUY" )
    print(f"Recibido: {buy}")
    return BuyResponse (
        transaction_id = transaction.id,
        user_id = user.id,
        asset_id = asset.id,
        quantity = buy.quantity,
        total_cost = total_cost,
        type       = "BUY",
        remaining_balance = user.balance
    )