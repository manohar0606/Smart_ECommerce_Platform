from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Table

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "auth_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False)
    username: Mapped[str] = mapped_column(String(150), nullable=False)
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    is_staff: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    date_joined: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    profile: Mapped["UserProfile"] = relationship(
        back_populates="user",
        uselist=False,
    )


class UserProfile(Base):
    __tablename__ = "users_userprofile"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    role: Mapped[str] = mapped_column(String(10), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(10), nullable=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("auth_user.id"),
        nullable=False,
        unique=True,
    )

    user: Mapped["User"] = relationship(
        back_populates="profile",
    )


class Product(Base):
    __tablename__ = "products_product"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(200), nullable=True)



order_products = Table(
    "orders_order_products",
    Base.metadata,
    Column("id", BigInteger, primary_key=True),
    Column("order_id", BigInteger, ForeignKey("orders_order.id"), nullable=False),
    Column("product_id", BigInteger, ForeignKey("products_product.id"), nullable=False),
)


class Cart(Base):
    __tablename__ = "orders_cart"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("auth_user.id"),
        nullable=False,
    )
    product_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("products_product.id"),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    user: Mapped["User"] = relationship()
    product: Mapped["Product"] = relationship()


class Order(Base):
    __tablename__ = "orders_order"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("auth_user.id"),
        nullable=False,
    )
    total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    payment_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    order_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    user: Mapped["User"] = relationship()
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        lazy="selectin",
    )


class OrderItem(Base):
    __tablename__ = "orders_orderitem"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("orders_order.id"),
        nullable=False,
    )
    product_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("products_product.id"),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    order: Mapped["Order"] = relationship(
        back_populates="items",
    )
    product: Mapped["Product"] = relationship()
    

class Payment(Base):
    __tablename__ = "orders_payment"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("orders_order.id"),
        nullable=False,
        unique=True,
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    payment_method: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    transaction_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    order: Mapped["Order"] = relationship()



class Notification(Base):
    __tablename__ = "orders_notification"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("auth_user.id"),
        nullable=False,
    )
    type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    is_read: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    user: Mapped["User"] = relationship()