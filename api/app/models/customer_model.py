from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from .base import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(32), nullable=True)
    nif = Column(String(32), nullable=True, unique=True)
    address = Column(Text, nullable=True)
    country = Column(String(64), nullable=True)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', email='{self.email}', active={self.active})>"
