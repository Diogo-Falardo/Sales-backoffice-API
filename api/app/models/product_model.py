from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, Numeric, Index, UniqueConstraint
)
from .base import Base 

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    sku = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False, default=0.00)
    cost = Column(Numeric(10, 2), nullable=True)
    stock = Column(Integer, nullable=False, default=0)
    min_stock = Column(Integer, nullable=False, default=0)
    category = Column(String(100), nullable=True)
    image_url = Column(String(255), nullable=True)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("idx_products_name", "name"),
        Index("idx_products_category", "category"),
        UniqueConstraint("sku", name="uq_products_sku"),
    )

    def __repr__(self):
        return f"<Product(id={self.id}, sku='{self.sku}', name='{self.name}', price={self.price}, stock={self.stock})>"
