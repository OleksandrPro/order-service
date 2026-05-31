import logging
from flask import jsonify
from werkzeug.exceptions import HTTPException
from pydantic import ValidationError
from app.exceptions.base import OrderServiceError
from app.exceptions.domain import (
    CustomerNotFoundError,
    EmailAlreadyTakenError,
    ProductNotFoundError,
    SKUAlreadyExistsError
)


logger = logging.getLogger(__name__)

def register_error_handlers(app):

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({
            "error": error.name.upper().replace(" ", "_"),
            "message": error.description,
        }), error.code

    @app.errorhandler(CustomerNotFoundError)
    def customer_not_found(error):
        logger.warning(str(error))
        return jsonify({
            "error": "CUSTOMER_NOT_FOUND",
            "message": str(error),
        }), 404
    
    @app.errorhandler(ProductNotFoundError)
    def product_not_found(error):
        logger.warning(str(error))
        return jsonify({
            "error": "PRODUCT_NOT_FOUND",
            "message": str(error),
        }), 404

    @app.errorhandler(EmailAlreadyTakenError)
    def handle_email_taken(error):
        logger.warning(str(error))
        return jsonify({
            "error": "EMAIL_ALREADY_TAKEN",
            "message": str(error),
        }), 409
    
    @app.errorhandler(SKUAlreadyExistsError)
    def handle_sku_taken(error):
        logger.warning(str(error))
        return jsonify({
            "error": "SKU_ALREADY_EXISTS",
            "message": str(error),
        }), 409

    @app.errorhandler(OrderServiceError)
    def handle_domain_error(error):
        logger.warning(str(error))
        return jsonify({
            "error": "DOMAIN_ERROR",
            "message": str(error),
        }), 400

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        logger.warning(str(error))
        return jsonify({
            "error": "VALIDATION_ERROR",
            "message": "Invalid request payload",
            "details": error.errors()
        }), 400

    @app.errorhandler(Exception)
    def handle_unexpected(error):
        logger.exception("Unhandled exception", exc_info=True)

        return jsonify({
            "error": "INTERNAL_ERROR",
            "message": "Unexpected server error",
        }), 500
