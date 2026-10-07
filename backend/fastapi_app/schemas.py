from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Literal

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    stock: int
    category: str
    is_active: bool
    image_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    name: str
    description: str
    price: Decimal
    stock: int
    category: str = "General"
    is_active: bool = True
    image_url: str | None = None


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductResponse

    model_config = ConfigDict(from_attributes=True)

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: Decimal
    product: ProductResponse

    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: int
    total: Decimal
    payment_status: str
    order_status: str
    timestamp: datetime
    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)

class NotificationResponse(BaseModel):
    id: int
    type: str
    message: str
    is_read: bool
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)




class OrderStatusUpdate(BaseModel):
    order_status: Literal[
        "pending",
        "confirmed",
        "shipped",
        "delivered",
        "cancelled",
    ]