# Smart E-Commerce Platform
## Backend Project Documentation

## 1. Project Overview

The Smart E-Commerce Platform is a backend-focused e-commerce system built using FastAPI, Django, and MySQL.

The current submission scope includes the complete backend and administration functionality. Frontend development is excluded from this submission.

---

## 2. Project Objectives

The platform provides:

- User registration and login
- JWT authentication
- Role-based access control
- Product browsing and filtering
- Cart management
- Order management
- Payment processing
- Payment success and failure handling
- Email notifications
- In-app notifications
- Real-time WebSocket notifications
- Django administration
- Analytics dashboard
- CSV and PDF report exports
- MySQL database support

---

## 3. Technology Stack

### Backend

- Python
- FastAPI
- Django
- SQLAlchemy

### Database

- MySQL

### Authentication

- JWT
- Auth0 support

### Communication

- REST APIs
- WebSockets
- SMTP email

### Payments

- Stripe integration
- Mock payment mode for testing/submission

### Reporting and Analytics

- Django Admin
- Chart.js
- ReportLab
- CSV export

---

## 4. System Architecture

The application contains two backend components.

### FastAPI Backend

FastAPI provides the user/API layer.

Responsibilities:

- Authentication
- Product browsing
- Cart management
- Checkout
- Payments
- Orders
- Notifications
- WebSocket communication

### Django Admin Backend

Django provides the administration layer.

Responsibilities:

- User management
- Role management
- Product management
- Order management
- Payment management
- Notification management
- Analytics dashboard
- CSV reports
- PDF reports

Both systems use the same MySQL database.

---

## 5. Main Entities

### User

Stores:

- User ID
- Username
- Name
- Email
- Password
- Staff/admin flags
- Active status

### UserProfile

Stores:

- User relationship
- Role
- Phone number

Roles:

- Admin
- Staff
- Customer

### Product

Stores:

- Product name
- Description
- Price
- Stock
- Category
- Active status
- Image URL
- Created date
- Updated date

### Cart

Stores:

- User
- Product
- Quantity

### Order

Stores:

- User
- Total
- Payment status
- Order status
- Timestamp

Order statuses:

- pending
- confirmed
- shipped
- delivered
- cancelled

### OrderItem

Stores:

- Order
- Product
- Quantity
- Purchase price

### Payment

Stores:

- Order
- Amount
- Payment method
- Transaction ID
- Payment status
- Created date

Payment statuses:

- pending
- success
- failed

### Notification

Stores:

- User
- Notification type
- Message
- Read/unread status
- Timestamp

---

## 6. Authentication

The FastAPI backend uses JWT authentication.

Normal authentication flow:

1. Register user
2. Login with email and password
3. Receive JWT access token
4. Use the token for protected endpoints

JWT roles include:

- admin
- staff
- customer

Role-based permissions are applied to protected endpoints.

---

## 7. Auth0 Support

Auth0 support is included for external authentication.

The FastAPI backend provides an Auth0 authentication endpoint which validates Auth0 access tokens.

Required configuration:

```env
AUTH0_DOMAIN=your-auth0-domain
AUTH0_AUDIENCE=your-auth0-api-audience

---

## 8. API Endpoints

### Authentication

```text
POST /auth/register
POST /auth/login
POST /auth/auth0


---

## 9. Payment Processing

The platform supports payment processing through the payment API.

### Successful Payment

```text
POST /payments/checkout/{order_id}