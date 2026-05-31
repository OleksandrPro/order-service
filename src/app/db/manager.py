from typing import TypeVar, Optional, Sequence, Any
from sqlalchemy import Executable, update
from sqlalchemy.orm import Session 
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .models import Base


T = TypeVar("T", bound=Base)


class DatabaseManager:
    def __init__(self, session: Session):
        self.session = session

    def add_record(self, model_instance: T) -> T:
        self.session.add(model_instance)
        self.session.flush()
        self.session.refresh(model_instance)
        return model_instance

    def get_first(self, query: Executable) -> Optional[T]:
        result = self.session.scalars(query)
        return result.first()

    def get_all(self, query: Executable) -> Sequence[T]:
        result = self.session.scalars(query)
        return result.all()

    def bulk_update(
        self,
        model: type[T],
        values: list[dict[str, Any]],
    ) -> None:
        if not values:
            return

        self.session.execute(update(model), values)
        self.session.flush()

    def commit(self) -> None:
        try:
            self.session.commit()
        except SQLAlchemyError:
            self.rollback()
            raise

    def rollback(self) -> None:
        self.session.rollback()
