# ---- Config ----
APP_DIR ?= backend
MODULE  ?= app.asgi:app
HOST    ?= 127.0.0.1
PORT    ?= 8000
VENV    ?= .venv

# Derived
API ?= http://$(HOST):$(PORT)/api

# Auto-pick the first customer / invoice if not provided
CUSTOMER_ID ?= $(shell curl -s $(API)/customers | jq -r '.[0].id')
INVOICE_ID  ?= $(shell curl -s $(API)/invoices  | jq -r '.[0].id')

# Random-ish invoice number and defaults
INV_NUM ?= INV-$(shell jot -r 1 1000 9999 2>/dev/null || echo $$RANDOM)
TOTAL   ?= 199.99

# Line-item defaults
DESC ?= Design work
QTY  ?= 2
PRICE?= 100.00

# ---- Phonies ----
.PHONY: dev dev-no-reload lint fmt seed pshell api urls \
        customers invoices create-invoice create-invoice-dup \
        add-line-item line-items smoke

# Run FastAPI (Uvicorn) in the foreground
dev:
	$(VENV)/bin/uvicorn $(MODULE) --reload --app-dir $(APP_DIR) --host $(HOST) --port $(PORT)

# If you want a non-reload run
dev-no-reload:
	$(VENV)/bin/uvicorn $(MODULE) --app-dir $(APP_DIR) --host $(HOST) --port $(PORT)

# Lint/format (optional — requires ruff/black installed)
lint:
	-$(VENV)/bin/ruff check $(APP_DIR)

fmt:
	-$(VENV)/bin/ruff check $(APP_DIR) --fix
	-$(VENV)/bin/black $(APP_DIR)

# Seed demo data (adjust path if yours differs)
seed:
	$(VENV)/bin/python $(APP_DIR)/app/scripts/seed_demo.py

# Quick psql shell
pshell:
	psql -h localhost -p 5432 -U "$$USER" -d invoice_app

# Smoke test helper (basic)
api:
	curl -s $(API)/health
	curl -s $(API)/customers
	curl -s $(API)/invoices

# Show useful URLs
urls:
	@echo "Health:     $(API)/health"
	@echo "Customers:  $(API)/customers"
	@echo "Invoices:   $(API)/invoices"

# ---- Quick lists ----------------------------------------------
customers:
	@curl -sS "$(API)/customers" | jq .

invoices:
	@curl -sS "$(API)/invoices" | jq .

# ---- Create invoice (random number) ---------------------------
create-invoice:
	@echo "Using CUSTOMER_ID=$(CUSTOMER_ID) INV_NUM=$(INV_NUM) TOTAL=$(TOTAL)"
	@jq -n \
	  --arg number "$(INV_NUM)" \
	  --arg cust   "$(CUSTOMER_ID)" \
	  --arg total  "$(TOTAL)" \
	  '{number:$number, customer_id:$cust, total:($total|tonumber)}' | \
	curl -sS -X POST "$(API)/invoices" \
	  -H "Content-Type: application/json" \
	  -d @- | jq .

# ---- Duplicate number test (should 409) -----------------------
create-invoice-dup:
	@echo "Posting duplicate invoice number INV-1001 (expect 409)"
	@jq -n \
	  --arg number "INV-1001" \
	  --arg cust   "$(CUSTOMER_ID)" \
	  --arg total  "50" \
	  '{number:$number, customer_id:$cust, total:($total|tonumber)}' | \
	curl -i -sS -X POST "$(API)/invoices" \
	  -H "Content-Type: application/json" \
	  -d @-

# ---- Add a line item to first (or specified) invoice ----------
add-line-item:
	@echo "Using INVOICE_ID=$(INVOICE_ID) DESC=$(DESC) QTY=$(QTY) PRICE=$(PRICE)"
	@jq -n \
	  --arg desc  "$(DESC)" \
	  --arg qty   "$(QTY)" \
	  --arg price "$(PRICE)" \
	  '{description:$desc, qty:($qty|tonumber), unit_price:($price|tonumber)}' | \
	curl -sS -X POST "$(API)/invoices/$(INVOICE_ID)/line-items" \
	  -H "Content-Type: application/json" \
	  -d @- | jq .

line-items:
	@curl -sS "$(API)/invoices/$(INVOICE_ID)/line-items" | jq .

# ---- One-shot smoke test --------------------------------------
smoke:
	$(MAKE) customers
	$(MAKE) create-invoice
	$(MAKE) invoices
	$(MAKE) create-invoice-dup || true
