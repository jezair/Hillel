from datetime import datetime
import enum
from typing import List
from sqlalchemy import (
    String, Integer, DateTime, ForeignKey, Text, Enum, Float, Table, Boolean
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship
)


class Base(DeclarativeBase):
    pass


# ============================
#           ENUMS
# ============================
class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    DRIVER = "DRIVER"
    CUSTOMER = "CUSTOMER"


class OrderStatus(str, enum.Enum):
    PROCESSING = "PROCESSING"
    ON_THE_WAY = "ON_THE_WAY"
    CANCELLED = "CANCELLED"
    DELIVERED = "DELIVERED"


# ============================
#           USERS
# ============================
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    delivery_address: Mapped[str] = mapped_column(Text, nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), default=RoleEnum.CUSTOMER)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    orders: Mapped[List["Order"]] = relationship(back_populates="customer")


# ============================
#           DISHES
# ============================
class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    order_items: Mapped[List["OrderDish"]] = relationship(back_populates="dish")


# ============================
#           ORDERS
# ============================
class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PROCESSING)
    scheduled_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    delivery_address: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    customer: Mapped[User] = relationship(back_populates="orders")
    dishes: Mapped[List["OrderDish"]] = relationship(back_populates="order", cascade="all, delete-orphan")


# ============================
# ORDER <-> DISH (many-to-many)
# ============================
class OrderDish(Base):
    __tablename__ = "order_dishes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    dish_id: Mapped[int] = mapped_column(ForeignKey("dishes.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    order: Mapped[Order] = relationship(back_populates="dishes")
    dish: Mapped[Dish] = relationship(back_populates="order_items")
