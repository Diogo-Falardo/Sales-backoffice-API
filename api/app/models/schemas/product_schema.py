from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, field_validator

# utils
# helpers
from app.utils.helpers import customer_helper, product_helper

# core
# security
from app.core.security import validate_int_id

# ---- Base ----
class ProductBase(BaseModel):
    name: str
    sku: str
    price: Decimal
    stock: int
    min_stock: int

    @field_validator("name", mode="before")
    @classmethod
    def _name(cls, name):
        return customer_helper.validate_name(name)
    
    @field_validator("sku", mode="before")
    @classmethod
    def _sku(cls, sku):
        return product_helper.validate_sku(sku)
    
    @field_validator("price", mode="before")
    @classmethod
    def _price(cls, price):
        return product_helper.validate_price_cost(price,"Price")
    
    @field_validator("stock", mode="before")
    @classmethod
    def _stock(cls, stock):
        return product_helper.validate_stock(stock)
    
    @field_validator("min_stock", mode="before")
    @classmethod
    def _stock(cls, min_stock):
        return product_helper.validate_stock(min_stock)


# ---- Create ----
class ProductCreate(ProductBase):
    description: Optional[str] = None
    cost: Optional[Decimal] = None
    category: Optional[str] = None
    image_url: Optional[str] = None

    @field_validator("description", mode="before")
    @classmethod
    def _description(cls, description):
        return product_helper.validate_description(description)
    
    @field_validator("cost", mode="before")
    @classmethod
    def _price(cls, cost):
        return product_helper.validate_price_cost(cost,"Cost")
    
    @field_validator("category", mode="before")
    @classmethod
    def _category(cls, category):
        return product_helper.validate_category(category)
    
    @field_validator("image_url", mode="before")
    @classmethod
    def _image_url(cls, img_url):
        return product_helper.validate_img_url(img_url)

# ---- Update ----
    id: int
    name: Optional[str] = None
    sku:  Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None
    min_stock: Optional[int] = None
    description: Optional[str] = None
    cost: Optional[Decimal] = None
    category: Optional[str] = None
    image_url: Optional[str] = None

    @field_validator("id", mode="before")
    @classmethod
    def _id(cls, id):
        return validate_int_id(id)
    
    @field_validator("name", mode="before")
    @classmethod
    def _name(cls, name):
        return customer_helper.validate_name(name)
    
    @field_validator("sku", mode="before")
    @classmethod
    def _sku(cls, sku):
        return product_helper.validate_sku(sku)
    
    @field_validator("price", mode="before")
    @classmethod
    def _price(cls, price):
        return product_helper.validate_price_cost(price,"Price")
    
    @field_validator("stock", mode="before")
    @classmethod
    def _stock(cls, stock):
        return product_helper.validate_stock(stock)
    
    @field_validator("min_stock", mode="before")
    @classmethod
    def _stock(cls, min_stock):
        return product_helper.validate_stock(min_stock)
    
    @field_validator("description", mode="before")
    @classmethod
    def _description(cls, description):
        return product_helper.validate_description(description)
    
    @field_validator("cost", mode="before")
    @classmethod
    def _price(cls, cost):
        return product_helper.validate_price_cost(cost,"Cost")
    
    @field_validator("category", mode="before")
    @classmethod
    def _category(cls, category):
        return product_helper.validate_category(category)
    
    @field_validator("image_url", mode="before")
    @classmethod
    def _image_url(cls, img_url):
        return product_helper.validate_img_url(img_url)
    
# ---- ID ----
class ProductId(BaseModel):
    id: int

    @field_validator("id", mode="before")
    @classmethod
    def _id(cls, id):
        return validate_int_id(id)

    
# ---- Read/Out ----
class ProductOut(ProductBase):
    created_at: datetime
    updated_at: datetime
    active: int

    model_config = ConfigDict(from_attributes=True)
