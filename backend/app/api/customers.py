from app.repositories.memory.customer_repo import InMemoryCustomerRepo
from flask import Blueprint, jsonify, request

bp = Blueprint("customers", __name__)
repo = InMemoryCustomerRepo()


@bp.get("/api/customers")
def list_customers():
    return jsonify(repo.list())


@bp.post("/api/customers")
def create_customer():
    data = request.get_json() or {}
    customer = repo.create(data)
    return jsonify(customer), 201


@bp.get("/api/customers/<cid>")
def get_customer(cid):
    c = repo.get(cid)
    if not c:
        return jsonify({"error": "not found"}), 404
    return jsonify(c)
