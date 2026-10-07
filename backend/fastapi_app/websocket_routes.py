from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jose import JWTError, jwt

from fastapi_app.auth_utils import JWT_ALGORITHM, JWT_SECRET_KEY
from fastapi_app.websocket_manager import manager


router = APIRouter(
    tags=["WebSocket"],
)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008)
        return

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        user_id = int(payload.get("sub"))

        if not user_id:
            await websocket.close(code=1008)
            return

    except (JWTError, TypeError, ValueError):
        await websocket.close(code=1008)
        return

    await manager.connect(user_id, websocket)

    try:
        await websocket.send_json(
            {
                "type": "connection",
                "message": "WebSocket connected successfully",
                "user_id": user_id,
            }
        )

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(user_id)

    except Exception as exc:
        print(
            f"WebSocket error for user_id={user_id}: {exc}"
        )
        manager.disconnect(user_id)