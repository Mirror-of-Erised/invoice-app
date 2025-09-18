# backend/app/main.py
from flask import Flask
from flask_cors import CORS
from app.api.health import bp as health_bp
from app.api.customers import bp as customers_bp
from app.api.main import bp as orgs_bp  # adjust if orgs live elsewhere
from app.db.base import Base
from app.db.engine import engine

def create_app():
    app = Flask(__name__)
    CORS(app)

    # create tables (dev-only)
    Base.metadata.create_all(bind=engine)

    # register blueprints
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(customers_bp, url_prefix="/api")
    app.register_blueprint(orgs_bp, url_prefix="/api")
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
