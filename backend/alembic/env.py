# backend/alembic/env.py
from __future__ import annotations
from app.models import invoice_line_item as _ili  # noqa: F401
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# --- App imports (so Alembic knows your models) ---
# Make sure "backend" is on PYTHONPATH when running alembic (run from backend/)
from app.config.settings import Settings
from app.db.base import Base

# Import models so they are registered on Base.metadata
# If you add new models, import them here too.
from app.models import customer as _customer_model  # noqa: F401
from app.models import invoice as _invoice_model  # noqa: F401


# --------------------------------------------------

# this is the Alembic Config object, which provides access
# to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Provide target_metadata for 'autogenerate'
target_metadata = Base.metadata

# Get DB URL from app settings (ignore sqlalchemy.url in alembic.ini)
settings = Settings()
DB_URL = settings.database_url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = DB_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,  # detect column type changes
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = DB_URL

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
