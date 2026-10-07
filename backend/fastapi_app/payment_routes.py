import os
from pathlib import Path
from uuid import uuid4

import stripe
from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from fastapi_app.auth_dependencies import get_current_user
from fastapi_app.database import get_db
from fastapi_app.email_service import send_email
from fastapi_app.models import Order, OrderItem, Payment, User
from fastapi_app.notification_service import (
    create_notification,
    send_realtime_notification,
)


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")


stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
PAYMENT_MODE = os.getenv("PAYMENT_MODE", "stripe")

SUCCESS_URL = os.getenv(
    "STRIPE_SUCCESS_URL",
    "http://127.0.0.1:8000/payments/success",
)

CANCEL_URL = os.getenv(
    "STRIPE_CANCEL_URL",
    "http://127.0.0.1:8000/payments/cancel",
)


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post("/checkout/{order_id}")
def create_checkout_session(
    order_id: int,
    background_tasks: BackgroundTasks,
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
            status_code=404,
            detail="Order not found",
        )

    if order.payment_status == "paid":
        raise HTTPException(
            status_code=400,
            detail="Order is already paid",
        )

    # ==========================================================
    # MOCK PAYMENT SUCCESS
    # ==========================================================
    if PAYMENT_MODE == "mock":
        payment = db.scalar(
            select(Payment).where(
                Payment.order_id == order.id
            )
        )

        if not payment:
            payment = Payment(
                order_id=order.id,
                amount=order.total,
                payment_method="stripe",
                transaction_id=None,
                status="pending",
            )
            db.add(payment)

        payment.transaction_id = f"mock_{uuid4().hex}"
        payment.status = "success"

        order.payment_status = "paid"
        order.order_status = "confirmed"

        payment_message = (
            f"Payment for Order #{order.id} was successful."
        )

        create_notification(
            db=db,
            user_id=current_user.id,
            notification_type="payment",
            message=payment_message,
        )

        db.commit()

        db.refresh(payment)
        db.refresh(order)

        background_tasks.add_task(
            send_realtime_notification,
            current_user.id,
            "payment",
            payment_message,
        )

        background_tasks.add_task(
            send_email,
            current_user.email,
            f"Payment Successful - Order #{order.id}",
            (
                f"Hello {current_user.first_name or current_user.username},\n\n"
                f"Your payment for Order #{order.id} was successful.\n"
                f"Amount paid: ₹{order.total}\n"
                f"Payment status: Paid\n"
                f"Order status: Confirmed\n\n"
                f"Thank you for shopping with us."
            ),
        )

        return {
            "message": "Mock payment successful",
            "order_id": order.id,
            "payment_status": order.payment_status,
            "order_status": order.order_status,
            "transaction_id": payment.transaction_id,
            "amount": str(payment.amount),
        }

    # ==========================================================
    # REAL STRIPE MODE
    # ==========================================================
    if not stripe.api_key:
        raise HTTPException(
            status_code=500,
            detail="Stripe secret key is not configured",
        )

    line_items = []

    for item in order.items:
        line_items.append(
            {
                "price_data": {
                    "currency": "inr",
                    "product_data": {
                        "name": item.product.name,
                    },
                    "unit_amount": int(item.price * 100),
                },
                "quantity": item.quantity,
            }
        )

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=line_items,
            success_url=(
                f"{SUCCESS_URL}?session_id="
                "{CHECKOUT_SESSION_ID}"
            ),
            cancel_url=(
                f"{CANCEL_URL}?order_id={order.id}"
            ),
            customer_email=current_user.email,
            client_reference_id=str(order.id),
            metadata={
                "order_id": str(order.id),
                "user_id": str(current_user.id),
            },
        )

    except stripe.error.StripeError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Stripe payment service error: {str(exc)}",
        )

    payment = db.scalar(
        select(Payment).where(
            Payment.order_id == order.id
        )
    )

    if not payment:
        payment = Payment(
            order_id=order.id,
            amount=order.total,
            payment_method="stripe",
            transaction_id=session.id,
            status="pending",
        )
        db.add(payment)

    else:
        payment.transaction_id = session.id
        payment.status = "pending"

    db.commit()

    return {
        "message": "Stripe Checkout Session created",
        "order_id": order.id,
        "session_id": session.id,
        "checkout_url": session.url,
    }


@router.post("/fail/{order_id}")
def fail_payment(
    order_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = db.scalar(
        select(Order).where(
            Order.id == order_id,
            Order.user_id == current_user.id,
        )
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    if order.payment_status == "paid":
        raise HTTPException(
            status_code=400,
            detail="Order is already paid",
        )

    payment = db.scalar(
        select(Payment).where(
            Payment.order_id == order.id
        )
    )

    if not payment:
        payment = Payment(
            order_id=order.id,
            amount=order.total,
            payment_method="stripe",
            transaction_id=None,
            status="pending",
        )
        db.add(payment)

    payment.transaction_id = f"mock_failed_{uuid4().hex}"
    payment.status = "failed"

    order.payment_status = "failed"

    payment_message = (
        f"Payment for Order #{order.id} failed."
    )

    create_notification(
        db=db,
        user_id=current_user.id,
        notification_type="payment",
        message=payment_message,
    )

    db.commit()

    db.refresh(payment)
    db.refresh(order)

    background_tasks.add_task(
        send_realtime_notification,
        current_user.id,
        "payment",
        payment_message,
    )

    background_tasks.add_task(
        send_email,
        current_user.email,
        f"Payment Failed - Order #{order.id}",
        (
            f"Hello {current_user.first_name or current_user.username},\n\n"
            f"Unfortunately, your payment for Order #{order.id} failed.\n"
            f"Amount: ₹{order.total}\n"
            f"Payment status: Failed\n\n"
            f"Please try again or use another payment method.\n\n"
            f"Thank you."
        ),
    )

    return {
        "message": "Mock payment failed",
        "order_id": order.id,
        "payment_status": order.payment_status,
        "order_status": order.order_status,
        "transaction_id": payment.transaction_id,
        "amount": str(payment.amount),
    }