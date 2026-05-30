from flask import Flask
from app.routes.customer_routes import customer_bp
from app.routes.product_routes import product_bp
from app.exceptions.handlers import register_error_handlers
from app.utils.logging import configure_logging


configure_logging()

app = Flask(__name__)

app.register_blueprint(customer_bp)
app.register_blueprint(product_bp)
register_error_handlers(app)
