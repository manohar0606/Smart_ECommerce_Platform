from datetime import datetime

from sqlalchemy.orm import Session

from fastapi_app.models import Notification
from fastapi_app.websocket_manager import manager


def create_notification(
    db: Session,
    user_id: int,
    notification_type: str,
    message: str,
):
    notification = Notification(
        user_id=user_id,
        type=notification_type,
        message=message,
        is_read=False,
        timestamp=datetime.now(),
    )

    db.add(notification)

    return notification


async def send_realtime_notification(
    user_id: int,
    notification_type: str,
    message: str,
):
    await manager.send_to_user(
        user_id,
        {
            "type": notification_type,
            "message": message,
        },
    )