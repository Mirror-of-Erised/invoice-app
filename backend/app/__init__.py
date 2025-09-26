# backend/app/__init__.py
from __future__ import annotations

from fastapi import FastAPI
from .asgi import app as _fastapi_app

__all__: list[str] = ["create_app"]


def create_app() -> FastAPI:
    """
    Compatibility shim for any legacy code expecting `create_app()`.
    Returns the FastAPI app defined in app/asgi.py.
    """
    return _fastapi_app
