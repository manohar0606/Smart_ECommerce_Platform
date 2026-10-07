from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from fastapi_app.auth_dependencies import get_current_user, require_roles
from fastapi_app.database import get_db
from fastapi_app.email_service import send_email
from fastapi_app.models import Cart, Order, OrderItem, Payment, User
from fastapi_app.notification_service import (
    create_notification,
    send_realtime_notification,
)
from fastapi_app.schemas import OrderResponse, OrderStatusUpdate


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post(
    "/checkout",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def checkout(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cart_items = db.scalars(
        select(Cart)
        .options(joinedload(Cart.product))
        .where(Cart.user_id == current_user.id)
    ).unique().all()

    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty",
        )

    for cart_item in cart_items:
        if cart_item.quantity > cart_item.product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for {cart_item.product.name}",
            )

    total = sum(
        cart_item.product.price * cart_item.quantity
        for cart_item in cart_items
    )

    order = Order(
        user_id=current_user.id,
        total=total,
        payment_status="pending",
        order_status="pending",
        timestamp=datetime.now(),
    )

    db.add(order)
    db.flush()

    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.product.price,
        )
        db.add(order_item)

    payment = Payment(
        order_id=order.id,
        amount=total,
        payment_method="stripe",
        transaction_id=None,
        status="pending",
        created_at=datetime.now(),
    )

    db.add(payment)

    for cart_item in cart_items:
        db.delete(cart_item)

    order_message = f"Order #{order.id} has been placed successfully."

    create_notification(
        db=db,
        user_id=current_user.id,
        notification_type="order",
        message=order_message,
    )

    background_tasks.add_task(
        send_realtime_notification,
        current_user.id,
        "order",
        order_message,
    )

    background_tasks.add_task(
        send_email,
        current_user.email,
        f"Order #{order.id} Confirmation",
        (
            f"Hello {current_user.first_name or current_user.username},\n\n"
            f"Your order #{order.id} has been placed successfully.\n"
            f"Order total: ₹{total}\n"
            f"Order status: Pending\n\n"
            f"Thank you for shopping with us."
        ),
    )

    db.commit()

    order = db.scalar(
        select(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product)
        )
        .where(Order.id == order.id)
    )

    return order


@router.get("/", response_model=list[OrderResponse])
def get_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    orders = db.scalars(
        select(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product)
        )
        .where(Order.user_id == current_user.id)
        .order_by(Order.timestamp.desc())
    ).unique().all()

    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = db.scalar(
        select(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product)
        )
        .where(
            Order.id == order_id,
            Order.user_id == current_user.id,
        )
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return order


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
)
async def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(require_roles("admin", "staff")),
    db: Session = Depends(get_db),
):
    order = db.scalar(
        select(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product)
        )
        .where(Order.id == order_id)
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    order.order_status = status_data.order_status

    notification_type = (
        "shipping"
        if status_data.order_status in {"shipped", "delivered"}
        else "order"
    )

    notification_message = (
        f"Order #{order.id} status changed to "
        f"{status_data.order_status}."
    )

    create_notification(
        db=db,
        user_id=order.user_id,
        notification_type=notification_type,
        message=notification_message,
    )

    db.commit()

    # Send WebSocket notification directly.
    await send_realtime_notification(
        order.user_id,
        notification_type,
        notification_message,
    )

    user = db.scalar(
        select(User).where(User.id == order.user_id)
    )

    if user:
        status_subject = (
            f"Order #{order.id} is "
            f"{status_data.order_status.title()}"
        )

        status_email = (
            f"Hello {user.first_name or user.username},\n\n"
            f"Your order #{order.id} status has been updated.\n"
            f"Current status: {status_data.order_status.title()}\n"
            f"Order total: ₹{order.total}\n\n"
            f"Thank you for shopping with us."
        )

        background_tasks.add_task(
            send_email,
            user.email,
            status_subject,
            status_email,
        )

    order = db.scalar(
        select(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product)
        )
        .where(Order.id == order.id)
    )

    return order