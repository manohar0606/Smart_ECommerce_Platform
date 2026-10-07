from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_app.auth_dependencies import get_current_user
from fastapi_app.database import get_db
from fastapi_app.models import Notification, User
from fastapi_app.schemas import NotificationResponse


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.get("/", response_model=list[NotificationResponse])
def get_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notifications = db.scalars(
        select(Notification)
        .where(Notification.user_id == current_user.id)
        .order_by(Notification.timestamp.desc())
    ).all()

    return notifications


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notification = db.scalar(
        select(Notification).where(
            Notification.id == notification_id,
            Notification.user_id == current_user.id,
        )
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    notification.is_read = True
    db.commit()
    db.refresh(notification)

    return notification