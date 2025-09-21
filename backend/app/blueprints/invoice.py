from flask import Blueprint, request

invoice_bp = Blueprint("invoice", __name__)


@invoice_bp.get("/hello")
def hello_invoice():
    return {"message": "Invoice service ready"}


@invoice_bp.post("/create")
def create_invoice():
    data = request.json or {}
    # TODO: validate & persist
    return {"ok": True, "invoice": data}, 201
