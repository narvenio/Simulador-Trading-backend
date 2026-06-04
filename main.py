from fastapi import FastAPI
from database import engine, metadata, SessionLocal
from contextlib import asynccontextmanager
from services.seed import seed_assets
from routers import assets, buy, dashboard, market, portfolio, sell, transaction, users, balance_history
from fastapi.middleware.cors import  CORSMiddleware

@asynccontextmanager
async def inicio(app:FastAPI):
    seed_assets()
    yield

app = FastAPI(lifespan = inicio)

metadata.create_all(bind=engine)

origenes_permitidos = [
    "https://narvenio.github.io/Simulador-Trading-frontend/",
    "https://simulador-trading-backend.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origenes_permitidos,
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers = ["*"]
# aqui estamos usando un intermediario "middelware" que interviene entre el servidor y el navegador
# llamamos a la funcion importada y "allow_origins" permite a la direccion http o https de donde estes probando la pagina
# allow_methods ["*"] cuando es asi "*" dices que permites a todos los metodos funcionar, como post, get. delete etc
# allow_headers ["*"] cuando es asi dices que permites a todos los headers, que son esos con el content/type de las apis
)
def get_db():
    db = SessionLocal()
    try:
        yield db # mantener abierto la base de datos
    finally:
        db.close() # cerrar cuando ya no uses



app.include_router(assets.router)
app.include_router(buy.router)
app.include_router(dashboard.router)
app.include_router(market.router)
app.include_router(portfolio.router)
app.include_router(sell.router)
app.include_router(transaction.router)
app.include_router(users.router)
app.include_router(balance_history.router)

@app.get("/")
def read_root():
    return {"status: ok"}







            

















