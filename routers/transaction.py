from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session, joinedload
from typing import List
from schemas import TransactionResponse
import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db # mantener abierto la base de datos
    finally:
        db.close() # cerrar cuando ya no uses


@router.get("/users/{user_id}/transactions", response_model= List[TransactionResponse])
def get_user_transactions(user_id: int, db: Session = Depends(get_db)):
    
    transactions = (
        db.query(models.Transaction)
        .options(joinedload(models.Transaction.asset))
        .filter(models.Transaction.user_id == user_id)
        .all()
    )
    return transactions
    #transactions = db.query(models.Transaction).filter(models.Transaction.user_id == user_id).all()
# consultamos en la tabla de transacciones, luego filtramos hasta llegar al usuario
# y que sea igual al user_id que creamos. Luego trae todo eso y guardalo en la variable

    if not transactions:
        raise HTTPException(status_code= 404, detail="El usuario no tiene Transacciones")
    return transactions