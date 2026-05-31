from typing import TypeVar, Optional, Sequence, Any
from sqlalchemy import Executable, update
from sqlalchemy.orm import Session 
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .models import Base


T = TypeVar("T", bound=Base)


class DatabaseManager:
    def __init__(self, session: Session):
        self.session = session

    def add_record(self, model_instance: T, err_msg: str = "Error adding record") -> T:
        try:
            self.session.add(model_instance)
            self.session.commit()
            self.session.refresh(model_instance)
            return model_instance
        except IntegrityError:
            self.session.rollback()
            # logger.warning(f"Integrity error (duplicate?): {err_msg}")
            raise
        except SQLAlchemyError:
            self.session.rollback()
            # logger.exception(err_msg)
            raise

    def get_first(self, query: Executable, err_msg: str = "Error executing query") -> Optional[T]:
        try:
            result = self.session.scalars(query)
            return result.first()
        except SQLAlchemyError:
            # logger.exception(err_msg)
            raise

    def get_all(self, query: Executable, err_msg: str = "Error fetching record list") -> Sequence[T]:
        try:
            result = self.session.scalars(query)
            return result.all()
        except SQLAlchemyError:
            # logger.exception(err_msg)
            raise
    
    def bulk_update(self, model: type[T], values: list[dict[str, Any]], err_msg: str = "Error executing bulk update") -> None:
        if not values:
            return

        try:
            self.session.execute(update(model), values)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise
