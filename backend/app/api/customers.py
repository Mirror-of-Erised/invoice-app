from app.config.settings import settings
from flask import Blueprint, jsonify, request

bp = Blueprint("customers", __name__)


def _get_repo():
    if settings.repo_backend == "sql":
        from app.db.session import get_session
        from app.repositories.sql.customer_repo import SqlCustomerRepo

        return get_session(), SqlCustomerRepo
    else:
        from app.repositories.sql.customer_repo import InMemoryCustomerRepo

        return None, InMemoryCustomerRepo


@bp.get("")
@bp.get("/")
def list_customers():
    cm, Repo = _get_repo()
    org = request.args.get("organization_id")
    if cm:
        with cm as s:
            return jsonify(Repo(s).list(organization_id=org))
    return jsonify(Repo().list())


@bp.post("")
@bp.post("/")
def create_customer():
    data = request.get_json() or {}
    cm, Repo = _get_repo()
    if cm:
        with cm as s:
            created = Repo(s).create(data)
            return jsonify(created), 201
    created = Repo().create(data)
    return jsonify(created), 201


@bp.get("/<cid>")
def get_customer(cid):
    cm, Repo = _get_repo()
    if cm:
        with cm as s:
            found = Repo(s).get(cid)
            if not found:
                return jsonify({"error": "not found"}), 404
            return jsonify(found)
    found = Repo().get(cid)
    if not found:
        return jsonify({"error": "not found"}), 404
    return jsonify(found)
