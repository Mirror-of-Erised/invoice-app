from flask import Blueprint

user_bp = Blueprint("user", __name__)


@user_bp.get("/")
def me():
    return {"id": "demo", "name": "Adam"}
