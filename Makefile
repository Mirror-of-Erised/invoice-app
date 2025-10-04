# ---- Config ----
APP_DIR ?= backend
MODULE  ?= app.asgi:app
HOST    ?= 127.0.0.1
PORT    ?= 8000
VENV    ?= $(APP_DIR)/.venv

FRONTEND_DIR ?= frontend
NPM          ?= npm

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

# --- Python / venv paths (repo-root) ---
PYTHON  := python3
VENVPY  := $(VENV)/bin/python
PIP     := $(VENVPY) -m pip
UVICORN := $(VENVPY) -m uvicorn

# ---- Phonies ----
.PHONY: bootstrap dev dev-no-reload lint fmt flake dev-tools seed pshell api urls \
        customers invoices create-invoice create-invoice-dup \
        add-line-item line-items smoke test clean clean-venv \
        start start-backend start-frontend up install start-prod venv-info

# --- Setup: create venv + install deps (requirements.txt if present) + ensure fastapi/uvicorn/pytest/psycopg2-binary
bootstrap:
	@test -d "$(VENV)" || $(PYTHON) -m venv "$(VENV)"
	@$(PIP) install -U pip setuptools wheel
	@if [ -f "$(APP_DIR)/requirements.txt" ]; then $(PIP) install -r "$(APP_DIR)/requirements.txt"; fi
	@$(PIP) install "fastapi[standard]" uvicorn pytest psycopg2-binary

# --- Developer tools (auto-install ruff/black/flake8 if missing) ---
dev-tools:
	@test -d "$(VENV)" || $(PYTHON) -m venv "$(VENV)"
	@$(PIP) install -U pip setuptools wheel >/dev/null
	@$(VENVPY) -m pip show ruff   >/dev/null 2>&1 || $(PIP) install ruff
	@$(VENVPY) -m pip show black  >/dev/null 2>&1 || $(PIP) install black
	@$(VENVPY) -m pip show flake8 >/dev/null 2>&1 || $(PIP) install flake8

flake: dev-tools
	$(VENV)/bin/flake8 $(APP_DIR)

lint: dev-tools
	-$(VENV)/bin/ruff check $(APP_DIR)

fmt: dev-tools
	-$(VENV)/bin/ruff check $(APP_DIR) --fix
	-$(VENV)/bin/black $(APP_DIR)

# --- Run FastAPI (backend only) ---
dev:
	@$(MAKE) bootstrap
	@$(VENVPY) -m uvicorn $(MODULE) --reload --host $(HOST) --port $(PORT) --app-dir $(APP_DIR)

dev-no-reload:
	@$(VENVPY) -m uvicorn $(MODULE) --host $(HOST) --port $(PORT) --app-dir $(APP_DIR)

# --- Frontend only ---
start-frontend:
	@cd "$(FRONTEND_DIR)" && $(NPM) install && $(NPM) run dev

# --- Start both backend (8000) and frontend (5173) together ---
start: bootstrap
	@echo "Starting backend on $(HOST):$(PORT) and Vite on 5173..."
	@bash -c 'set -m; \
	  ( $(VENVPY) -m uvicorn $(MODULE) --reload --host $(HOST) --port $(PORT) --app-dir $(APP_DIR) ) & \
	  BACK_PID=$$!; \
	  ( cd "$(FRONTEND_DIR)" && $(NPM) install && $(NPM) run dev ) & \
	  FRONT_PID=$$!; \
	  trap "kill $$BACK_PID $$FRONT_PID 2>/dev/null || true" INT TERM; \
	  wait'

# Backend only (no reload)
start-prod: bootstrap
	@$(VENVPY) -m uvicorn $(MODULE) --host $(HOST) --port $(PORT) --app-dir $(APP_DIR)

# Short alias
up: start

# Seed demo data
seed:
	$(VENVPY) $(APP_DIR)/app/scripts/seed_demo.py

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

# --- Tests & cleanup -------------------------------------------
test:
	@$(VENVPY) -m pytest -q $(APP_DIR)

clean:
	@find "$(APP_DIR)" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@rm -rf "$(APP_DIR)/.pytest_cache" 2>/dev/null || true

clean-venv:
	@rm -rf "$(VENV)"

# Debug helper to confirm we're using the right interpreter
venv-info: bootstrap
	@echo "Using interpreter: $(VENVPY)"
	@$(VENVPY) -c "import sys; print('sys.executable =', sys.executable)"
	@$(VENVPY) -c "import fastapi, uvicorn; print('fastapi =', fastapi.__version__, '| uvicorn =', uvicorn.__version__)"
