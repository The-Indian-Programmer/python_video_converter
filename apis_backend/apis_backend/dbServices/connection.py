from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

DATABASE_URL = f"mysql+mysqlconnector://{config('DB_USER')}:{config('DB_PASSWORD')}@" \
               f"{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
