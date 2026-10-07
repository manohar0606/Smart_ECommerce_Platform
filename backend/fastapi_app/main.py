from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_app.cart_routes import router as cart_router
from fastapi_app.database import engine
from fastapi_app.product_routes import router as product_router
from fastapi_app.auth_routes import router as auth_router
from fastapi_app.order_routes import router as order_router
from fastapi_app.payment_routes import router as payment_router
from fastapi_app.notification_routes import router as notification_router
from fastapi_app.websocket_routes import websocket_endpoint

app = FastAPI(title="Smart E-Commerce Platform")

# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router)
app.include_router(auth_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(notification_router)
app.websocket("/ws")(websocket_endpoint)


@app.get("/")
def home():
    return {"message": "Smart E-Commerce Platform API is running"}