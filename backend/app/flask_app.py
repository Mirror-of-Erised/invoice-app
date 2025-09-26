from flask import Flask
from app.api.customers import bp as customers_bp
from app.api.health import bp as health_bp


def create_flask_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(health_bp, url_prefix="/api")            # <— was /api/health
    app.register_blueprint(customers_bp, url_prefix="/api/customers")
    return app
