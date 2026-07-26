from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


SQLALCHEMY_DATABASE_URL = "sqlite:///./bookshelf.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args = {"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    with SessionLocal() as db:
        yield db