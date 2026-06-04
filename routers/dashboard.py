from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import DashboardResponse, PortfolioItemResponse, TransactionResponse
from services.market import  simulate_price
import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db # mantener abierto la base de datos
    finally:
        db.close() # cerrar cuando ya no uses


@router.get("/dashboard/{user_id}", response_model=DashboardResponse)
def get_dashboard(user_id : int, db : Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code= 404, detail= "Usuario no encontrado")

    portfolio_items = (db.query(models.Portfolio, models.Asset)
                       .join(models.Asset, models.Portfolio.asset_id == models.Asset.id)
                       .filter(models.Portfolio.user_id == user_id).all())
    # primero haces una consulta a las 2 tablas, luego añades la tabla de asset a la tabla portfolio y como estan juntas, comparas el asset_id de portfolio con el de la tabla asset
    # despues de tenerlo, haces un filter comparando el user_id del portfolio con el user_id que es el parametro de la funcion
    #portfolio_items = db.query(models.Portfolio).filter(models.Portfolio.user_id == user_id).all()
# obtener todo el portafolio del usuario

    portfolio_value = 0
    portfolio_response = []
    transaction_response = []

# iteramos dentro del portafolio para tener todo detallado y separado:
    for portfolio, asset in portfolio_items:
    #for item in portfolio_items:
    #    asset = db.query(models.Asset).filter(models.Asset.id == item.asset_id).first()
# consultamos el asset_id de la tabla de datos para que sea igual a la del portafolio

        sim_price = simulate_price(asset.price)
        asset_value = portfolio.quantity * sim_price
        portfolio_value += asset_value
# sacamos el precio simulado, luego lo sumamos con la cantidad de asset que tengamos
# y se suma al valor total de portafolio que tengamos

        portfolio_response.append(PortfolioItemResponse(
        asset_id = asset.id,
        asset_name = asset.name,
        symbol = asset.symbol,
        quantity = portfolio.quantity,
        current_price = sim_price,
        total_value = round(asset_value, 2)

    ))

    transactions = db.query(models.Transaction).filter(models.Transaction.user_id == user_id).order_by(models.Transaction.id.desc()).all()
# crea variable de transaccion que consulte n la tabla de transaccion y compare que su id sea el mismo que el user id
# luego con order_by que ordene todas sus transacciones por medio de su id y de forma descreciente

    for tx in transactions:
        transaction_response.append(TransactionResponse(
            id = tx.id,
            user_id = tx.user_id,
            asset_id = tx.asset_id,
            quantity = tx.quantity,
            total_price = tx.total_price,
            type        = tx.type,
            timestamp   = tx.timestamp
        ))

    return DashboardResponse(
        user_id = user.id,
        balance = user.balance,
        portfolio_value = round(portfolio_value, 2),
        total_assets  = len(portfolio_items),
        total_transaction = len(transactions),
        portfolio = portfolio_response,
        transactions = transaction_response
    )
