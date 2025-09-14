.PHONY: dev dev-backend dev-frontend stop

# Run Flask + React together
dev:
	( cd backend && python -m app.main & echo $$! > .flask_pid ) ; \
	( cd frontend && npm run dev -- --host & echo $$! > .vite_pid ) ; \
	wait

# Run just the backend
dev-backend:
	cd backend && python -m app.main

# Run just the frontend
dev-frontend:
	cd frontend && npm run dev -- --host

# Stop Flask + React started by "make dev"
stop:
	@if [ -f .flask_pid ]; then kill $$(cat .flask_pid) || true; rm .flask_pid; fi
	@if [ -f .vite_pid ]; then kill $$(cat .vite_pid) || true; rm .vite_pid; fi
	@echo "Stopped Flask + React"
