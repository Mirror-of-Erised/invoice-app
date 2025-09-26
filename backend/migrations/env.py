# backend/migrations/env.py
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# NEW: read .env so DATABASE_URL is available
try:
    from dotenv import load_dotenv  # pip install python-dotenv

    load_dotenv()
except Exception:
    pass

# Import Base + models so autogenerate sees them
from app.db.base import Base  # noqa
from app.models.customer import Customer  # noqa
from app.models.organization import Organization  # noqa

config = context.config

# NEW: if env var exists, override the alembic.ini value
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
config = context.config
target_metadata = None


def run_migrations_offline():
    url = os.environ.get("DATABASE_URL")
    if url:
        config.set_main_option("sqlalchemy.url", url)
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    url = os.environ.get("DATABASE_URL")
    if url:
        config.set_main_option("sqlalchemy.url", url)
    connectable = engine_from_config(
        config.get_section(config.config_ini_section) or {}, prefix="sqlalchemy.", poolclass=pool.NullPool
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
