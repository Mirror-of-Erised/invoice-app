# backend/app/flask_app.py
from __future__ import annotations

from flask import Flask
from app.api.customers import bp as customers_bp
from app.api.health import bp as health_bp


def create_flask_app() -> Flask:
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    # mount blueprints here (after app is created)
    app.register_blueprint(health_bp, url_prefix="/api")            # -> /flask/api/health
    app.register_blueprint(customers_bp, url_prefix="/api/customers")  # -> /flask/api/customers
    return app
