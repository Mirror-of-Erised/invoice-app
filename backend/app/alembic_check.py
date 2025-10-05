from sqlalchemy import text
from alembic.config import Config
from alembic.script import ScriptDirectory


def log_migration_status(engine):
    with engine.connect() as conn:
        db_rev = conn.execute(text("SELECT version_num FROM alembic_version")).scalar()
    cfg = Config("alembic.ini")
    head_rev = ScriptDirectory.from_config(cfg).get_current_head()
    if db_rev != head_rev:
        print(f"[WARN] Alembic not at head (db={db_rev}, head={head_rev})")
