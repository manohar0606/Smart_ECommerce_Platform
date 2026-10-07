from datetime import datetime
from decimal import Decimal
from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fastapi_app.auth_dependencies import require_roles
from fastapi_app.database import get_db
from fastapi_app.models import OrderItem, Product
from fastapi_app.schemas import ProductCreate, ProductResponse


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get("/", response_model=list[ProductResponse])
def get_products(
    category: str | None = Query(default=None),
    min_price: Decimal | None = Query(default=None, ge=0),
    max_price: Decimal | None = Query(default=None, ge=0),
    sort_by: Literal[
        "newest",
        "price_low",
        "price_high",
        "popularity",
    ] = Query(default="newest"),
    db: Session = Depends(get_db),
):
    statement = select(Product).where(
        Product.is_active.is_(True)
    )

    if category:
        statement = statement.where(
            Product.category == category
        )

    if min_price is not None:
        statement = statement.where(
            Product.price >= min_price
        )

    if max_price is not None:
        statement = statement.where(
            Product.price <= max_price
        )

    if sort_by == "price_low":
        statement = statement.order_by(
            Product.price.asc()
        )

    elif sort_by == "price_high":
        statement = statement.order_by(
            Product.price.desc()
        )

    elif sort_by == "popularity":
        popularity = (
            select(
                func.coalesce(
                    func.sum(OrderItem.quantity),
                    0,
                )
            )
            .where(
                OrderItem.product_id == Product.id
            )
            .correlate(Product)
            .scalar_subquery()
        )

        statement = statement.order_by(
            popularity.desc(),
            Product.created_at.desc(),
        )

    else:
        statement = statement.order_by(
            Product.created_at.desc()
        )

    return db.scalars(statement).all()


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=201,
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles("admin", "staff")
    ),
):
    now = datetime.now()

    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category=product.category,
        is_active=product.is_active,
        image_url=product.image_url,
        created_at=now,
        updated_at=now,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product