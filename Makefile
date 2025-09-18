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
	cd frontend && npm run dev -- --host --port=5175

# Stop Flask + React started by "make dev"
.PHONY: stop
stop:
	- kill -9 $$(lsof -ti:5000) 2>/dev/null || true
	- kill -9 $$(lsof -ti:5175) 2>/dev/null || true
	- pkill -f "python3 -m app.main" 2>/dev/null || true
	- rm -f .flask_pid .vite_pid



