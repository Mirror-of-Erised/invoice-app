from __future__ import annotations
from .asgi import app


def create_app() -> asgi:
    app = asgi(__name__)
    app.url_map.strict_slashes = False

    @app.teardown_appcontext
    def remove_session(_=None):
        try:
            from app.db.engine import SessionLocal

            SessionLocal.remove()

        except Exception:
            pass


    return app
