from app.db.unit_of_work import UnitOfWork
from app.schemas.product import CreateProduct, Product


class ProductService:
    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self.uow = uow

    def create(self, data: CreateProduct) -> Product:
        with self.uow:
            product = self.uow.product_repo.create(data)

        return product

    def get_all(self) -> list[Product]:
        with self.uow:
            products = self.uow.product_repo.get_all()

        return products
