from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.services.seed import seed_database
from app.routers import (
    auth_router, company_router, drivers_router,
    brokers_router, loads_router, invoices_router,
    documents_router, flows_router, codriver_router, admin_router,
)
from app.routers.admin import seed_role_permissions


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
        seed_role_permissions(db)
    finally:
        db.close()
    yield


app = FastAPI(title="HWY TMS API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(company_router)
app.include_router(drivers_router)
app.include_router(brokers_router)
app.include_router(loads_router)
app.include_router(invoices_router)
app.include_router(documents_router)
app.include_router(flows_router)
app.include_router(codriver_router)
app.include_router(admin_router)


@app.get("/api/v1/health")
def health():
    return {"data": {"status": "ok", "version": "1.0.0"}}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": str(exc)})
