from app.routers.auth import router as auth_router
from app.routers.company import router as company_router
from app.routers.drivers import router as drivers_router
from app.routers.brokers import router as brokers_router
from app.routers.loads import router as loads_router
from app.routers.invoices import router as invoices_router
from app.routers.documents import router as documents_router
from app.routers.flows import router as flows_router
from app.routers.codriver import router as codriver_router
from app.routers.admin import router as admin_router

__all__ = [
    "auth_router", "company_router", "drivers_router",
    "brokers_router", "loads_router", "invoices_router",
    "documents_router", "flows_router", "codriver_router", "admin_router",
]
