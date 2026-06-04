from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./trading.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit= False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
#actua como una clase "padre" que guarda todos los registros de las tablas
metadata: MetaData = Base.metadata