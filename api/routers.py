from fastapi import Depends
from utils.unitofwork import SqlAlchemyUnitOfWork
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Пример фабрики сессий
engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# Dependency
def UoWDepends():
    with SqlAlchemyUnitOfWork(SessionLocal) as uow:
        yield uow
