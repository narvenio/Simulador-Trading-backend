from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, column, ForeignKey, DateTime
from database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True, index= True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=0)

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key= True, index= True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable= False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable= False)
    quantity = Column(Float, nullable= False)
    total_price = Column(Float, nullable= False)
    type         = Column(String, nullable= False)
    timestamp    = Column(DateTime, default = datetime.now)
print("Models.py cargado con timestamp")


class Portfolio(Base):
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key= True, index = True)
    user_id= Column(Integer, ForeignKey("users.id"), nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable= False)
    quantity = Column(Float, nullable=False)

class BalanceHistory(Base):
    __tablename__ = "balance_history"

    id = Column(Integer, primary_key= True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable= False)
    balance = Column(Float)
    timestamp = Column(DateTime, default = datetime.now)