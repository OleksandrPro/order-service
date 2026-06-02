from flask import Flask
from flask_cors import CORS
from app.routes.customer_routes import customer_bp
from app.routes.product_routes import product_bp
from app.routes.order_routes import order_bp
from app.exceptions.handlers import register_error_handlers
from app.utils.logging import configure_logging


configure_logging()

app = Flask(__name__)

app.register_blueprint(customer_bp)
app.register_blueprint(product_bp)
app.register_blueprint(order_bp)
register_error_handlers(app)

CORS(app, resources={r"/*": {"origins": "*"}})
