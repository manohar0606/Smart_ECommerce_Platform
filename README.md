# OrderNow — Smart E-Commerce Platform

A full-stack Smart E-Commerce Platform where customers can browse products, manage their cart, place orders, make payments, track orders, and receive notifications.

The platform includes a React customer frontend, FastAPI user/API backend, Django admin panel, and MySQL database.

---

## Features

### Customer Features

- User registration
- User login
- JWT authentication
- Role-based access control
- Product browsing
- Product category filtering
- Product price filtering
- Product popularity sorting
- Add products to cart
- View cart
- Remove products from cart
- Dynamic checkout
- Order creation
- Mock payment processing
- Payment success and failure handling
- Order history
- Order status tracking
- Customer notifications
- Mark notifications as read

### Admin Features

- Django Admin panel
- User management
- User profile management
- Product management
- Cart management
- Order management
- Order item management
- Payment management
- Notification management
- Role management
- Analytics support
- CSV/PDF reporting support

---

## Technology Stack

### Frontend

- React
- Vite
- React Router
- Axios
- JavaScript
- CSS

### Backend

- Python
- FastAPI
- Django
- SQLAlchemy
- JWT Authentication
- Role-Based Access Control

### Database

- MySQL

### Additional Technologies

- Uvicorn
- WebSockets
- SMTP Email Notifications
- Stripe integration support
- Mock Payment fallback
- ReportLab
- Chart.js

---

## Project Architecture

```text
Smart_ECommerce_Platform/
│
├── backend/
│   ├── fastapi_app/
│   │   ├── routes/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   ├── auth_utils.py
│   │   └── main.py
│   │
│   ├── django_admin/
│   │   ├── manage.py
│   │   ├── users/
│   │   ├── products/
│   │   ├── orders/
│   │   └── ...
│   │
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
│
├── database/
├── docs/
├── postman/
└── README.md