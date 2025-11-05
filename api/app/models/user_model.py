from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Enum, DateTime
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum("admin", "staff", name="user_roles"), nullable=False, default="staff")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_login = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
