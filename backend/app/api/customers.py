# backend/app/api/customers.py
from flask import Blueprint, request, jsonify
from app.repositories.memory.organization_repo import InMemoryOrganizationRepo
from app.repositories.memory.customer_repo import InMemoryCustomerRepo

bp = Blueprint("customers", __name__)
org_repo = InMemoryOrganizationRepo()
cust_repo = InMemoryCustomerRepo()

@bp.post("/api/orgs")
def create_org():
    data = request.get_json() or {}
    org = org_repo.create(name=data["name"], email=data.get("email"))
    return jsonify(org), 201

@bp.post("/api/customers")
def create_customer():
    data = request.get_json() or {}
    c = cust_repo.create(
        organization_id=data["organization_id"],
        name=data["name"],
        email=data.get("email"),
        phone=data.get("phone"),
        billing_address=data.get("billing_address"),
    )
    return jsonify(c), 201

@bp.get("/api/customers/by-org/<int:org_id>")
def list_customers(org_id: int):
    return jsonify(list(cust_repo.list_by_org(org_id)))
