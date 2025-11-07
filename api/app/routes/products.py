from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from typing import Any, List

# core
# session
from app.core.session import get_db

# schemas
from app.models.schemas.product_schema import ProductOut, ProductCreate, ProductUpdate, ProductId, StockHealthResponse, StockValue

# utils
# exceptions
from app.utils.exceptions import THROW_ERROR

# services
from app.services import product_service

router = APIRouter(prefix="/products", tags=["products"])

# create a product
@router.post("/add", response_model=ProductOut, name="addProduct")
def add_product(
    payload: ProductCreate,
    db: Session = Depends(get_db)
):
    if product_service.check_sku(payload.sku , db) is True:
        THROW_ERROR("Sku already in use!",400)

    data: dict[str, Any] = payload.model_dump(exclude_unset=True)

    return product_service.insert_product(data, db)

# update a product
@router.patch("/update", response_model=ProductOut, name="updateProduct")
def update_product(
    payload: ProductUpdate,
    db: Session = Depends(get_db)
):
    if product_service.check_id(payload.id, db) is False:
        THROW_ERROR("**NOT FOUND** - Product dont exist!", 400)

    if product_service.check_sku(payload.sku , db) is True:
        THROW_ERROR("Sku already in use!",400)

    data: dict[str, Any] = payload.model_dump(exclude_unset=True)

    return product_service.update_product(payload.id, data, db)

# inactive product
@router.put("/inactive", response_model=ProductOut, name="inactiveProduct")
def inactive_product(
    payload: ProductId,
    db: Session = Depends(get_db)
):
    if product_service.check_id(payload.id, db) is False:
        THROW_ERROR("**NOT FOUND** - Product dont exist!", 400)

    return product_service.inactive_product(payload.id, db)

# delete product
@router.delete("/delete", response_model=ProductOut, name="deleteProduct")
def delete_product(
    payload: ProductId,
    db: Session = Depends(get_db)
):
    if product_service.check_id(payload.id, db) is False:
        THROW_ERROR("**NOT FOUND** - Product dont exist!", 400)

    return product_service.delete_product(payload.id, db)

# get products 
@router.get("/products", response_model=List[ProductOut], name="products")
def produdcts(
    db: Session = Depends(get_db)
):
    return product_service.products(db)

# get products inactive
@router.get("/inactive-products", response_model=List[ProductOut], name="inactiveProducts")
def inactive_products(
    db: Session = Depends(get_db)
):
    return product_service.i_products(db)


# stock products -> low/mid/good 
@router.get("/stock-products", response_model=StockHealthResponse, name="stockResponse")
def stock_response(
    near_low: int = Query(5, ge=0, description="Threshold for near low stock"),
    db: Session = Depends(get_db)
):
    return product_service.Mstock(near_low, db)


# stock products -> value
@router.get("/stock-value", response_model=StockValue, name="stockValue")
def stock_value(
    db: Session = Depends(get_db)
):
    return product_service.Vstock(db)
    