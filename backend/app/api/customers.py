# backend/app/api/customers.py
from __future__ import annotations

from flask import Blueprint, jsonify, request

from app.config.settings import settings

# SQL path
from app.db.session import SessionLocal
from app.repositories.sql.customer_repo import SqlCustomerRepo

# Memory path
from app.repositories.memory.customer_repo import CustomerRepoMemory

bp = Blueprint("customers", __name__)  # prefix is set in flask_app.py


def _use_sql() -> bool:
    return getattr(settings, "use_sql_repos", False)


@bp.get("")
@bp.get("/")
def list_customers():
    org = request.args.get("organization_id")

    if _use_sql():
        with SessionLocal() as s:
            rows = SqlCustomerRepo(s).list(organization_id=org)
            return jsonify(rows)

    # memory fallback
    rows = CustomerRepoMemory().list(organization_id=org)
    return jsonify(rows)


@bp.post("")
@bp.post("/")
def create_customer():
    data = request.get_json() or {}

    if _use_sql():
        with SessionLocal() as s:
            created = SqlCustomerRepo(s).create(data)
            return jsonify(created), 201

    created = CustomerRepoMemory().create(data)
    return jsonify(created), 201


@bp.get("/<cid>")
def get_customer(cid: str):
    if _use_sql():
        with SessionLocal() as s:
            found = SqlCustomerRepo(s).get(cid)
            if not found:
                return jsonify({"error": "not found"}), 404
            return jsonify(found)

    found = CustomerRepoMemory().get(cid)
    if not found:
        return jsonify({"error": "not found"}), 404
    return jsonify(found)
