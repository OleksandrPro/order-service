from .manager import DatabaseManager

class UnitOfWork:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc:
            self.db_manager.session.rollback()
        else:
            self.db_manager.commit()