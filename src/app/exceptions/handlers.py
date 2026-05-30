from flask import jsonify
from app.exceptions.base import OrderServiceError
from app.exceptions.domain import EmailAlreadyTakenError


def register_error_handlers(app):

    @app.errorhandler(EmailAlreadyTakenError)
    def handle_email_taken(error):
        return jsonify({
            "error": "EMAIL_ALREADY_TAKEN",
            "message": str(error),
        }), 409

    @app.errorhandler(OrderServiceError)
    def handle_domain_error(error):
        return jsonify({
            "error": "DOMAIN_ERROR",
            "message": str(error),
        }), 400

    @app.errorhandler(Exception)
    def handle_unexpected(error):
        return jsonify({
            "error": "INTERNAL_ERROR",
            "message": "Unexpected server error",
        }), 500