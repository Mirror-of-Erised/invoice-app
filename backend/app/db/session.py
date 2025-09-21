from contextlib import contextmanager
from typing import Generator

from app.db.engine import SessionLocal
from sqlalchemy.orm import Session


@contextmanager
def get_session() -> Generator[Session, None, None]:
    s = SessionLocal()
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()
