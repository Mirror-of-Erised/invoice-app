import os
from dotenv import load_dotenv


def load_config(app):
    # Try backend/.env first, then project_root/.env
    backend_base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    project_root = os.path.dirname(backend_base)

    for path in (
        os.path.join(backend_base, ".env"),
        os.path.join(project_root, ".env"),
    ):
        if os.path.exists(path):
            load_dotenv(path, override=True)
            break

    app.config.update(
        {
            "ENV": os.getenv("ENV", "development"),
            "SECRET_KEY": os.getenv("SECRET_KEY", "dev-secret"),
            "SQLALCHEMY_DATABASE_URI": os.getenv(
                "DATABASE_URL", "sqlite:///dev.db"
            ),
        }
    )
