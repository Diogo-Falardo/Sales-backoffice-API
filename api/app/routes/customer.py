from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from typing import Any, List
from datetime import datetime, timezone

# core
# session
from app.core.session import get_db

# models 
from app.models.customer_model import Customer
# schemas
from app.models.schemas.customer_schema import CustomerCreate, CustomerUpdate, CustomerOut, CustomerId

# utils
# exceptions
from app.utils.exceptions import THROW_ERROR

# services
from app.services import customer_service

router = APIRouter(prefix="/customer", tags=["customer"])

# create the customer
@router.post("/add", response_model=CustomerOut, name="addCustomer")
def add_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db)
):
    if customer_service.check_email(payload.email, db) is True:
        THROW_ERROR("Email already in use.",400)

    data: dict[str, Any] = payload.model_dump(exclude_unset=True)

    for item, value in data.items():
        if item == "phone":
            if customer_service.check_phone(value,db) is True:
                THROW_ERROR("Phone number already in use", 400)
        if item == "nif":
            if customer_service.check_nif(value, db) is True:
                THROW_ERROR("NIF/Tax ID already in use", 400)

    return customer_service.insert_customer(data, db)

        
# update the customer
@router.patch("/update", response_model=CustomerOut, name="updateCustomer")
def update_customer(
    payload: CustomerUpdate,
    db: Session = Depends(get_db)
):
    
    if customer_service.check_id(payload.id) is not True:
        THROW_ERROR("**NOT FOUND** - Error with customer id!", 400)

    data: dict[str, Any] = payload.model_dump(exclude_unset=True)

    for item, value in data.items():
        if item == "email":
            if customer_service.check_email(payload.email, db) is True:
                THROW_ERROR("Email already in use.",400)
        if item == "phone":
            if customer_service.check_phone(value,db) is True:
                THROW_ERROR("Phone number already in use", 400)
        if item == "nif":
            if customer_service.check_nif(value, db) is True:
                THROW_ERROR("NIF/Tax ID already in use", 400)
    
    return customer_service.update_customer(payload.id,data, db)
  

# inactivate a customer
@router.put("/inactive", response_model=CustomerOut, name="inactiveCustomer")
def inactive_customer(
    payload: CustomerId,
    db: Session = Depends(get_db),
):
    if customer_service.check_id(payload.id) is not True:
        THROW_ERROR("**NOT FOUND** - Error with customer id!", 400)

    return customer_service.inactive_customer(payload.id, db)


# seach for a customer
@router.get("/search/{value}", response_model=List[CustomerOut], name="searchCustomer")
def search_customer(
    value: str = Path(..., min_length=2, max_length=64, description="Value to search for"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(25, ge=1, le=100, description="Results per page"),
    db: Session = Depends(get_db),
):
    value = value.strip()
    if not value:
        THROW_ERROR("You didnt insert anything to search for!", 400)
    
    return customer_service.search_customer_variable(value,page,size,db)


# get customers -> active
@router.get("/customers", response_model=List[CustomerOut], name="listCustomersActive")
def customers(
    db: Session = Depends(get_db),
):
    return customer_service.customers(db)

# get customers -> inactive
@router.get("/inactive-customers", response_model=List[CustomerOut], name="listCustomersInactive")
def customers(
    db: Session = Depends(get_db),
):
    return customer_service.i_customers(db)