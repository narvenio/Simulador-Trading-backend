from sqlalchemy.orm import Session
import models

def update_portafolio(db: Session, user_id:int, asset_id: int, quantity: float, operation: str):

    item = db.query(models.Portfolio).filter(models.Portfolio.user_id == user_id,
                                            models.Portfolio.asset_id == asset_id).first()
# creas una variable que guarde la consulta de user y asset dentro de la tabla de portfolio y luego la compra con las actuales

    if not item:
        item = models.Portfolio(
            user_id = user_id,
            asset_id = asset_id,
            quantity = 0
        )
        db.add(item)
# si no existe item, crealo dentro de la tabla "Porfolio" y que se guarde

    if operation == "BUY":
        cantidad = item.quantity
        cantidad += quantity

    if operation == "SELL":
        cantidad = item.quantity
        cantidad -= quantity

    db.commit()
    db.refresh(item)
    return item