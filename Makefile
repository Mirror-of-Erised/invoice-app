# ---- Config ----
APP_DIR ?= backend
MODULE  ?= app.asgi:app
HOST    ?= 127.0.0.1
PORT    ?= 8000
VENV    ?= .venv

# ---- Phonies ----
.PHONY: dev dev-no-reload lint fmt seed pshell api urls

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

# Smoke test helper
api:
	curl -s http://$(HOST):$(PORT)/api/health
	curl -s http://$(HOST):$(PORT)/api/customers 
	curl -s http://$(HOST):$(PORT)/api/invoices

# Show useful URLs
urls:
	@echo "Health:     http://$(HOST):$(PORT)/api/health"
	@echo "Customers:  http://$(HOST):$(PORT)/api/customers/"
	@echo "Invoices:   http://$(HOST):$(PORT)/api/invoices/"
