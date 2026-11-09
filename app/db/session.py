from pathlib import Path

from sqlalchemy import create_engine

from sqlalchemy.orm import Session,sessionmaker

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_URL = f"sqlite:///{PROJECT_ROOT/'student_management.db'}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

SessionLocal = sessionmaker(
    bind = engine,
    class_ = Session,
    autoflush= False,
    expire_on_commit=False,
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()