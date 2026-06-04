from typing import List

from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal
from schemas import BalanceHistoryResponse
import models

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db  # mantener abierto la base de datos
    finally:
        db.close()  # cerrar cuando ya no uses


@router.get("/users/{user_id}/balance-history", response_model=List[BalanceHistoryResponse])
def balance_history(user_id: int, db: SessionLocal = Depends(get_db)):
    balance_history = db.query(models.BalanceHistory).filter(models.BalanceHistory.user_id == user_id).all()

    if not balance_history:
        raise HTTPException(status_code=404, detail="El usuario no tiene historial de balance")
    return balance_history
