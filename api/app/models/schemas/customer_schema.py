from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator

# utils
# helpers
from app.utils.helpers import user_helper, customer_helper

# core
# security
from app.core.security import validate_int_id

# ---- Base ----
class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str

    @field_validator("name", mode="before")
    @classmethod
    def _name(cls, name):
        return customer_helper.validate_name(name)
    
    @field_validator("email", mode="before")
    @classmethod
    def _email(cls, email):
        return user_helper.validate_email(email)
    

# ---- Create ----
class CustomerCreate(CustomerBase):
    phone: Optional[str] = None
    nif: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None

    @field_validator("phone", mode="before")
    @classmethod
    def _phone(cls, phone):
        return customer_helper.validate_phone(phone)

    @field_validator("nif", mode="before")
    @classmethod
    def _nif(cls, nif):
        return customer_helper.validate_nif(nif)
    
    @field_validator("address", mode="before")
    @classmethod
    def _address(cls, address):
        return customer_helper.validate_address(address)
    
    @field_validator("country", mode="before")
    @classmethod
    def _country(cls, country):
        return customer_helper.validate_country(country)

# ---- Update ----
class CustomerUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    nif: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None

    @field_validator("id", mode="before")
    @classmethod
    def _id(cls, id):
        return validate_int_id(id)

    @field_validator("name", mode="before")
    @classmethod
    def _name(cls, name):
        return customer_helper.validate_name(name)
    
    @field_validator("email", mode="before")
    @classmethod
    def _email(cls, email):
        return user_helper.validate_email(email)
    
    @field_validator("phone", mode="before")
    @classmethod
    def _phone(cls, phone):
        return customer_helper.validate_phone(phone)
    
    
    @field_validator("nif", mode="before")
    @classmethod
    def _nif(cls, nif):
        return customer_helper.validate_nif(nif)
    
    @field_validator("address", mode="before")
    @classmethod
    def _address(cls, address):
        return customer_helper.validate_address(address)
    
    @field_validator("country", mode="before")
    @classmethod
    def _country(cls, country):
        return customer_helper.validate_country(country)


# ---- ID ----
class CustomerId(BaseModel):
    id: int

    @field_validator("id", mode="before")
    @classmethod
    def _id(cls, id):
        return validate_int_id(id)

# ---- Read/Out---
class CustomerOut(CustomerBase):
    created_at: datetime
    updated_at: datetime
    active: int

    model_config = ConfigDict(from_attributes=True)


