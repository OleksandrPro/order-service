from app.db.unit_of_work import UnitOfWork
from app.repositories.product_repository import ProductRepository
from app.schemas.product import CreateProduct, Product


class ProductService:
    def __init__(
        self,
        product_repo: ProductRepository,
        uow: UnitOfWork,
    ):
        self.product_repo = product_repo
        self.uow = uow

    def create(self, data: CreateProduct) -> Product:
        with self.uow:
            product = self.product_repo.create(data)

        return product
