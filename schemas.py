from datetime import  datetime
from symtable import Class

from pydantic import BaseModel
# Create = lo que el usuario envia
# Response = lo que la API devuelve

class AssetCreate(BaseModel):
    symbol: str
    name: str
    price: float
# esto es para que valide los datos

class AssetResponse(BaseModel):
    id: int
    name: str
    symbol: str
    price: float

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str
    email: str
    balance: float

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    balance: float

    class Config:
        from_attributes = True
# con "from_atributes" pydantic lee los atributos de los objetos
class SellRequest(BaseModel):
    user_id: int
    asset_id: int
    quantity: float

class SellResponse(BaseModel):
    transaction_id: int
    user_id: int
    asset_id: int
    quantity: float
    total_cost: float
    type: str
    remaining_balance: float

    class Config:
        from_attributes = True


class BuyRequest(BaseModel):
    user_id: int
    asset_id: int
    quantity: float

class BuyResponse(BaseModel):
    transaction_id: int
    user_id: int
    asset_id: int
    quantity: float
    total_cost: float
    type : str
    remaining_balance: float

    class Config:
        from_attributes = True

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    asset_id: int
    quantity: float
    total_price: float
    type: str
    timestamp: datetime


    class Config:
        from_attributes = True

class PortfolioItemResponse(BaseModel):
    asset_id : int
    asset_name : str
    symbol : str
    quantity   : float
    current_price : float
    total_value : float


class MarketItemResponse(BaseModel):
    asset_id : int
    name: str
    symbol : str
    base_price : float
    simulated_price : float
# el response de cada asset(item)


class MarketResponse(BaseModel):
    market: list[MarketItemResponse]
    class Config:
        from_attributes = True



class DashboardResponse(BaseModel):
    user_id : int
    balance : float
    portfolio_value : float
    total_assets : float
    total_transaction : float
    portfolio : list
    transactions : list

    class Config:
        from_attributes = True

class BalanceHistoryResponse(BaseModel):
    user_id : int
    balance: float
    timestamp: datetime

    class Config:
        from_attributes = True