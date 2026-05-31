from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.db.models.product import Product as ProductModel
from app.schemas.product import CreateProduct, Product as ProductSchema
from app.db.manager import DatabaseManager
from app.exceptions.domain import SKUAlreadyExistsError


class ProductRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def create(self, data: CreateProduct) -> ProductSchema:
        try:
            product = ProductModel(**data.model_dump())
            saved = self.db.add_record(product)

            return ProductSchema.model_validate(saved)
        except IntegrityError:
            raise SKUAlreadyExistsError(data.sku)

    def get(self, product_id: int) -> ProductSchema | None:
        query = select(ProductModel).where(ProductModel.id == product_id)
        result = self.db.get_first(query)

        return ProductSchema.model_validate(result) if result else None

    def get_many(self, product_ids: list[int]) -> dict[int, ProductSchema]:
        query = select(ProductModel).where(ProductModel.id.in_(product_ids))
        products = self.db.get_all(query)

        return {
            product.id: ProductSchema.model_validate(product)
            for product in products
        }
