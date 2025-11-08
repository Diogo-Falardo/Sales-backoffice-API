from decimal import Decimal, InvalidOperation
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, field_validator
import enum

# utils
# exceptions
from app.utils.exceptions import THROW_ERROR

# core
# security
from app.core.security import validate_int_id

def validate_decimal(value: Optional[Decimal], title: str = "Value") -> Decimal:
    if value is None:
        THROW_ERROR(f"{title} cannot be blank.", 400)

    try:
        value = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        THROW_ERROR(f"Invalid {title} format.", 400)

    if value < 0:
        THROW_ERROR(f"{title} must be a positive number.", 400)

    if value > Decimal("9999999.99"):
        THROW_ERROR(f"{title} is too large.", 400)

    return value

def validate_int(value: Optional[int], title: str = "Value") -> int:
    if value is None:
        THROW_ERROR(f"{title} cannot be blank.", 400)
    if not isinstance(value, int):
        THROW_ERROR(f"{title} not in the correct format", 400)

    try:
        value = int(value)
    except (TypeError, ValueError):
        THROW_ERROR(f"{title} must be an integer.", 400)

    if value < 0:
        THROW_ERROR(f"{title} cannot be negative.", 400)
    if value > 1_000_000_000:
        THROW_ERROR(f"{title} value is too large.", 400)

    return value

class OrderStatus(str, enum.Enum):
    draft = "draft"
    paid = "paid"
    shipped = "shipped"
    cancelled = "cancelled"

# ---- Create -----
class OrderItemCreate(BaseModel):
    product_id: int
    qty: int
    unit_price: Decimal

    @field_validator("product_id", mode="before")
    @classmethod
    def _id(cls, id):
        return validate_int_id(id)
    
    @field_validator("qty", mode="before")
    @classmethod
    def _qty(cls, qty):
        return validate_int(qty, title="Quantity")
    
    @field_validator("unit_price", mode="before")
    @classmethod
    def _unit_price(cls, unit_price):
        return validate_decimal(unit_price, title="Unit Price")
    
class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


# --- Patch ---
class OrderStatusUpdate(BaseModel):
    order_id: int
    status: OrderStatus

    @field_validator("order_id", mode="before")
    @classmethod
    def _id(cls, id):
        return validate_int_id(id)



# ---- Out ----
class OrderItemOut(BaseModel):
    id: int
    product_id: int
    qty: int
    unit_price: Decimal
    line_total: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OrderOut(BaseModel):
    id: int
    status: OrderStatus
    subtotal: Decimal
    total: Decimal
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemOut] = []

    model_config = ConfigDict(from_attributes=True)

class OrderGroupResponse(BaseModel):
    draft: List[OrderOut]
    paid: List[OrderOut]
    shipped: List[OrderOut]
    cancelled: List[OrderOut]
    totals: dict
