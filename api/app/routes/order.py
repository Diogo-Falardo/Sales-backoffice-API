from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from typing import Any, List

# core
# session
from app.core.session import get_db

# schemas
from app.models.schemas.order_schema import OrderCreate, OrderOut, OrderStatusUpdate, OrderGroupResponse

# utils
# exceptions
from app.utils.exceptions import THROW_ERROR

# services
from app.services import order_service

router = APIRouter(prefix="/order", tags=["order"])

# create an order
@router.post("/create", response_model=OrderOut, name="createOrder")
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db)
):
    return order_service.insert_order(payload, db)

# update order status
@router.put("/status", response_model=OrderOut)
def update_status(
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db)
): 
    return order_service.update_order_status(payload,db)

# get order by status
@router.get("/orders", response_model=OrderGroupResponse)
def orders(
    db: Session = Depends(get_db)
):
    return order_service.order_by_status(db)
    
    


