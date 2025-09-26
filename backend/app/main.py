from app.api.customers import bp as customers_bp
from app.api.health import bp as health_bp
from flask import Flask
from fastapi import FastAPI
from app.api.routes.invoices import router as invoices_router

app = FastAPI()
app.include_router(invoices_router)


def create_app():
    app = Flask(__name__)
    # mount at /api
    app.register_blueprint(health_bp, url_prefix="/api/health")
    app.register_blueprint(customers_bp, url_prefix="/api/customers")
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
