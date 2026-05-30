from flask import Blueprint, request
from app.db.session import SessionFactory
from app.dependencies import get_product_service
from app.schemas.product import CreateProduct


product_bp = Blueprint("products", __name__, url_prefix="/products")


@product_bp.post("/")
def create_product():
    data = CreateProduct.model_validate(request.get_json())

    with SessionFactory() as session:
        service = get_product_service(session)
        product = service.create(data)

        return product.model_dump(), 201
