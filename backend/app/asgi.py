from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import customers, invoices  # <-- import your routers

app = FastAPI(title="Invoice API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


# Mount routers  ⬇️
app.include_router(customers.router)
app.include_router(invoices.router)
