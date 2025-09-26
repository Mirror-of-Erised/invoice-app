from flask import Blueprint, jsonify


bp = Blueprint("api", __name__, url_prefix="/api")  # ← remove strict_slashes

@bp.get("/health")   # choose no trailing slash
def health():
    return jsonify({"status": "ok"})
