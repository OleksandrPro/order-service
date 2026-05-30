from app.repositories.product_repository import ProductRepository
from app.schemas.product import CreateProduct, Product


class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def create(self, data: CreateProduct) -> Product:
        return self.repo.create(data)
