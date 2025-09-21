from flask import Flask
from app.api.invoices import bp as invoices_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    @app.teardown_appcontext
    def remove_session(_=None):
        try:
            from app.db.engine import SessionLocal

            SessionLocal.remove()

        except Exception:
            pass

    from app.api.health import bp as health_bp

    app.register_blueprint(health_bp, url_prefix="/api")

    from app.api.customers import bp as customers_bp

    app.register_blueprint(customers_bp, url_prefix="/api/customers")

    app.register_blueprint(invoices_bp, url_prefix="/api/invoices")

    return app
