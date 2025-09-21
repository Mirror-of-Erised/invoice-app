from app.api.customers import bp as customers_bp
from app.api.health import bp as health_bp
from flask import Flask


def create_app():
    app = Flask(__name__)
    # mount at /api
    app.register_blueprint(health_bp, url_prefix="/api/health")
    app.register_blueprint(customers_bp, url_prefix="/api/customers")
    return app


app = create_app()
