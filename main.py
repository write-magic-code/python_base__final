import fastapi
from routers import order, warehous
app = fastapi.FastAPI(
    title="Kaishek Backend",
    description="Transportation panel of Kaishek",
    version="0.1.0"
)

app.include_router(
    order.router,
    prefix="/order",
    tags=["order"]
)
app.include_router(
    warehous.router,
    prefix="/warehous",
    tags=["warehouse"]
)