from flask import Blueprint
llm_bp = Blueprint("llm", __name__)


@llm_bp.get("/ping")
def ping():
    return {"llm": "stub", "status": "online"}
