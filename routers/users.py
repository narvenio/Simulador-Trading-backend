from schemas import UserResponse, UserCreate
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import models
from database import engine, metadata, SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db # mantener abierto la base de datos
    finally:
        db.close() # cerrar cuando ya no uses

router = APIRouter()

@router.post("/users", response_model = UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    try:
        new_user = models.User(
        name = user.name,
        email = user.email,
        balance = user.balance

        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        db.rollback()
        raise HTTPException (status_code = 404, detail= "El Usuario ya existe o hay un error de integridad")
    except Exception as e:
        db.rollback()
        print(f"Error inesperado: {e}")
# usamos user porque hace referencia a la variable de la funcion y no la clase, son 2 cosas distintas
# response y el UserCreate son los formatos que debe tener, luego se envia y se convierte archivo json
# por eso}acemos referencia que debe tener ese formato.

@router.get("/users", response_model = List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/users/{user_id}", response_model = UserResponse)
def get_user(user_id : int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()
# creamos una variable que sea = a consultar en la base de datos dentro de models. User
# filtramos exactamente lo que queremos y con firts obtenemos el primer resultado.
    if user is None:
        raise HTTPException(status_code = 404, detail= "Usuario no encontrado")
    return user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code= 400, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()
    return {"message": "Usuario Eliminado Correctamente"}