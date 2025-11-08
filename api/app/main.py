from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # -> *WARNING* -> dont use this in production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# auth
from app.routes.auth import router as auth_router
app.include_router(auth_router)

# customer
from app.routes.customer import router as customer_router
app.include_router(customer_router)

# products
from app.routes.products import router as product_router
app.include_router(product_router)

# oder
from app.routes.order import router as order_router
app.include_router(order_router)

