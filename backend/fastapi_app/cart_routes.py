from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from fastapi_app.auth_dependencies import get_current_user
from fastapi_app.database import get_db
from fastapi_app.notification_service import send_realtime_notification
from fastapi_app.models import Cart, Product, User
from fastapi_app.schemas import CartItemCreate, CartItemResponse


router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


@router.get("/", response_model=list[CartItemResponse])
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    statement = (
        select(Cart)
        .options(joinedload(Cart.product))
        .where(Cart.user_id == current_user.id)
        .order_by(Cart.id.desc())
    )

    return db.scalars(statement).unique().all()


@router.post(
    "/",
    response_model=CartItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_to_cart(
    cart_data: CartItemCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if cart_data.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than zero",
        )

    product = db.scalar(
        select(Product).where(
            Product.id == cart_data.product_id,
            Product.is_active.is_(True),
        )
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    if cart_data.quantity > product.stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Requested quantity exceeds available stock",
        )

    existing_cart_item = db.scalar(
        select(Cart).where(
            Cart.user_id == current_user.id,
            Cart.product_id == cart_data.product_id,
        )
    )

    if existing_cart_item:
        new_quantity = existing_cart_item.quantity + cart_data.quantity

        if new_quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Total quantity exceeds available stock",
            )

        existing_cart_item.quantity = new_quantity
        cart_item = existing_cart_item
    else:
        cart_item = Cart(
            user_id=current_user.id,
            product_id=cart_data.product_id,
            quantity=cart_data.quantity,
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    # Reload product relationship for the response.
    cart_item = db.scalar(
        select(Cart)
        .options(joinedload(Cart.product))
        .where(Cart.id == cart_item.id)
    )

    background_tasks.add_task(
        send_realtime_notification,
        current_user.id,
        "cart",
        f"{product.name} was added to your cart.",
    )

    return cart_item


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_from_cart(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cart_item = db.scalar(
        select(Cart)
        .options(joinedload(Cart.product))
        .where(
            Cart.user_id == current_user.id,
            Cart.product_id == product_id,
        )
    )

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product is not in the cart",
        )

    product_name = cart_item.product.name

    db.delete(cart_item)
    db.commit()

    await send_realtime_notification(
        current_user.id,
        "cart",
        f"{product_name} was removed from your cart.",
    )

    return None