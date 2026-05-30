from flask import Flask
from app.routes.customer_routes import customer_bp
from app.exceptions.handlers import register_error_handlers


app = Flask(__name__)

app.register_blueprint(customer_bp)
register_error_handlers(app)
