import secrets
import uuid
from datetime import datetime, timezone
import enum

from sqlalchemy.orm import relationship

from app.repositories.database import db
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Enum, Index


class UserRole(enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    WAREHOUSE_STAFF = "warehouse_staff"
    DELIVERY_STAFF = "delivery_staff"


class Address(db.Model):
    __tablename__ = "addresses"
    address_id = Column(String(20), primary_key=True, index=True, default=lambda : secrets.token_hex(10))
    street = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    zipcode = Column(String(20), nullable=False)
    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=False)
    user = relationship("UserModel", back_populates="address")

    def __repr__(self):
        return f"<Address(city:{self.city} | state:{self.state} | zipcode:{self.zipcode})>"


class UserModel(db.Model):
    __tablename__ = "users"
    user_id = Column(String(36), primary_key=True, index=True, default=lambda : str(uuid.uuid4()))
    full_name = Column(String(255), nullable= False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda : datetime.now(timezone.utc))
    address = relationship("Address", back_populates="user", lazy="dynamic", cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_on': role,
        'polymorphic_identity': 'user'
    }

    __table_args__ = (
        Index('idx_user_role_active', 'role', 'is_active'),
        Index('idx_user_created', 'created_at'),
    )

    def __repr__(self):
        return f"<UserModel(email:{self.email} | role:{self.role})>"


class Customer(UserModel):
    __mapper_args__ = {
        "polymorphic_identity": UserRole.CUSTOMER
    }


class Admin(UserModel):
    __mapper_args__ = {
        "polymorphic_identity": UserRole.ADMIN
    }


class SuperAdmin(UserModel):
    __mapper_args__ = {
        "polymorphic_identity": UserRole.SUPER_ADMIN
    }


class WarehouseStaff(UserModel):
    __mapper_args__ = {
        "polymorphic_identity": UserRole.WAREHOUSE_STAFF
    }


class DeliveryStaff(UserModel):
    __mapper_args__ = {
        "polymorphic_identity": UserRole.DELIVERY_STAFF
    }
