from fastapi import APIRouter, Depends, HTTPException
from schemas import AssetCreate, AssetResponse
from database import  SessionLocal
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List
import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db # mantener abierto la base de datos
    finally:
        db.close() # cerrar cuando ya no uses


@router.post("/assets", response_model=AssetResponse)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    try:
        new_asset = models.Asset(
            name = asset.name,
            symbol = asset.symbol,
            price  = asset.price
        )
        db.add(new_asset)

        db.commit()

        db.refresh(new_asset)
        return new_asset
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=404, detail= "El simbolo del activo ya existe o hay un error de integridad")
    except Exception as e:
        db.rollback()
        print(f"Error inesperado: {e}")

# la variable "asset" es del formato "AssetCreate" y devuelve un valor
# db es una variable cualquier del tipo "Session" de sqlalchemy y ejecuta esta funcion como dependencia

@router.get("/assets", response_model=List[AssetResponse])
def get_assets(db: Session = Depends(get_db)):
    assets = db.query(models.Asset).all() #consultame todo sobre la tabla asset
    return assets

@router.get("/assets/{asset_id}", response_model=AssetResponse)
def get_asset(asset_id : int, db: Session = Depends(get_db)):

    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
# crea una variable que busque en las tablas de models. Asset y que filtre por el id y
# y que eso se guarde en asset_id, con el firts devuelve si existe y si no no hay

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset no encontrado")

    return asset
# devuelve asset