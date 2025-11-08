
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, DECIMAL, Index
from sqlalchemy.orm import relationship
from .base import Base
import enum


class OrderStatus(str, enum.Enum):
    draft = "draft"
    paid = "paid"
    shipped = "shipped"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.draft)
    subtotal = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    total = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")



class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    qty = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    line_total = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    order = relationship("Order", back_populates="items")

