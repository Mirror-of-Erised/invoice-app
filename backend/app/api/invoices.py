from __future__ import annotations
from flask import Blueprint, jsonify, request
from app.config.settings import settings


bp = Blueprint("invoices", __name__)



def _get_repo():
    if settings.repo_backend == "sql":
        from app.db.session import get_session
        from app.repositories.sql.invoice_repo import SqlInvoiceRepo
        return get_session(), SqlInvoiceRepo
    else:
        raise NotImplementedError("Memory repo not implemented for invoices")


@bp.get("")
@bp.get("/")
def list_invoices():
    cm, Repo = _get_repo()
    org = request.args.get("organization_id")
    customer = request.args.get("customer_id")
    with cm as s:
        return jsonify(Repo(s).list(organization_id=org, customer_id=customer))


@bp.post("")
@bp.post("/")
def create_invoice():
    data = request.get_json() or {}
    cm, Repo = _get_repo()
    with cm as s:
        created = Repo(s).create(data)
        return jsonify(created), 201
