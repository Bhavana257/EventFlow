# app/models/database.py
from os import getenv
from time import sleep

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = getenv(
    "DATABASE_URL", "postgresql://user:password@localhost/orders_db"
)

MAX_RETRIES = 10
RETRY_DELAY = 5

engine = create_engine(DATABASE_URL)

for i in range(MAX_RETRIES):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(" Database connected successfully.")
        break
    except OperationalError:
        print(f" Database not ready, retrying ({i+1}/{MAX_RETRIES})...")
        sleep(RETRY_DELAY)
else:
    raise RuntimeError(" Could not connect to the database after max retries.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
