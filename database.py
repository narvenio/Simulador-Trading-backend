from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
import os
#DATABASE_URL = "sqlite:///./trading.db"
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit= False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
#actua como una clase "padre" que guarda todos los registros de las tablas
metadata: MetaData = Base.metadata