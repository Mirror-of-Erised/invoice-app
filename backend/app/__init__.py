from flask import Flask
from flask_cors import CORS

from .config.settings import load_config
from .blueprints.user import user_bp
from .blueprints.invoice import invoice_bp
from .blueprints.llm import llm_bp
from .blueprints.nostr import nostr_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    load_config(app)

    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(invoice_bp, url_prefix="/api/invoice")
    app.register_blueprint(llm_bp, url_prefix="/api/llm")
    app.register_blueprint(nostr_bp, url_prefix="/api/nostr")

    @app.route("/api/health")
    def health():
        return {"status": "ok"}

    return app
