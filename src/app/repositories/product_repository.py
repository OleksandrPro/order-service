from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.db.models.product import Product as ProductModel
from app.schemas.product import CreateProduct, Product as ProductSchema, ProductStockUpdate
from app.db.manager import DatabaseManager
from app.exceptions.domain import SKUAlreadyExistsError


class ProductRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create(self, data: CreateProduct) -> ProductSchema:
        try:
            product = ProductModel(**data.model_dump())
            saved = self.db_manager.add_record(product)

            return ProductSchema.model_validate(saved)
        except IntegrityError:
            raise SKUAlreadyExistsError(data.sku)

    def get(self, product_id: int) -> ProductSchema | None:
        query = select(ProductModel).where(ProductModel.id == product_id)
        result = self.db_manager.get_first(query)

        if result is None:
            return None

        return ProductSchema.model_validate(result)

    def get_many(self, product_ids: list[int]) -> dict[int, ProductSchema]:
        query = select(ProductModel).where(ProductModel.id.in_(product_ids))
        products = self.db_manager.get_all(query)

        return {
            product.id: ProductSchema.model_validate(product)
            for product in products
        }
    
    def update_stock(self, stock_updates: list[ProductStockUpdate]) -> None:

        if stock_updates:
            update_data = [
                {"id": su.product_id, "stock": su.stock}
                for su in stock_updates
            ]
            self.db_manager.bulk_update(ProductModel, update_data)
