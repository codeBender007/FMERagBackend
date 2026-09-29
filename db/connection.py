from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

# SQLAlchemy URL builder jo driver ko safely load karta hai
connection_url = URL.create(
    "mssql+pyodbc",
    host=settings.DB_SERVER,
    database=settings.DB_NAME,
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "trusted_connection": "yes",
        "TrustServerCertificate": "yes",
    }
)
engine = create_engine(
    connection_url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()