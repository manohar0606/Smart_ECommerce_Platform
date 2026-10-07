# Smart E-Commerce Platform

Backend-focused Smart E-Commerce Platform built with FastAPI, Django, and MySQL.

## Scope

This submission focuses on backend and admin functionality.

Frontend/mobile-responsive development is excluded from the current scope.

## Technology Stack

- Python 3.14
- FastAPI
- Django
- MySQL
- SQLAlchemy
- JWT Authentication
- Role-Based Access Control
- WebSockets
- SMTP Email Notifications
- Stripe integration with Mock Payment fallback
- ReportLab
- Chart.js

## Architecture

### FastAPI User/API Backend

- User registration
- User login
- JWT authentication
- Role-based access control
- Product browsing
- Category filtering
- Price filtering
- Popularity sorting
- Cart add/remove
- Checkout
- Payment processing
- Payment success/failure
- Order history
- Order status
- In-app notifications
- WebSocket real-time notifications
- Email notifications

### Django Admin Backend

- User management
- Role management
- Product management
- Order management
- Payment management
- Notification management
- Analytics dashboard
- CSV export
- PDF export

## Models / Entities

- User
- UserProfile
- Product
- Cart
- Order
- OrderItem
- Payment
- Notification

## Authentication

JWT authentication is used for the FastAPI API.

Roles:

- Admin
- Staff
- Customer

Protected endpoints use role-based authorization.

## Product APIs

### Get Products

```text
GET /products/