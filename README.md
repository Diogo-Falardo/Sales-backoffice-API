# Sales-backoffice-API

Sales management backoffice API built with **FastAPI** and **MySQL**.  
This project provides a complete backend solution for managing customers, products, and orders, including real-time stock tracking, order status management, and authentication.

---

## 🔐 Authentication System
- Secure endpoints for **user registration**, **login**, and **token refresh**.

---

## 👥 Customer Management
- Create, update, activate, or deactivate customers.  
- Advanced search and filtering support.

---

## 📦 Product Management
- Add, update, delete, or deactivate products.  
- Automatic stock tracking (low / near / green).  
- Product value and profitability calculations.

---

## 🧾 Order Management
- Create and manage orders with multiple items.  
- Manage order statuses: **draft**, **paid**, **shipped**, **cancelled**.  
- Retrieve and group orders by status.

---

## ⚙️ Tech Stack
- **FastAPI** — Python web framework  
- **SQLAlchemy** — ORM for database management  
- **MySQL** — Relational database  
- **Docker Compose** — Containerized development environment  
- **Pydantic v2** — Data validation and schema management  

---

## 🗂️ Project Structure
```
app/
 ├── core/              # Configuration, security, dependencies
 ├── models/            # SQLAlchemy models
 ├── schemas/           # Pydantic schemas
 ├── routes/            # API routes (auth, customer, product, order)
 ├── services/          # Business logic
 └── utils/             # Helpers and custom exceptions
```

---

## 🚀 Setup and Usage
```bash
# Clone the repository
git clone https://github.com/<your-username>/Sales-backoffice-API.git
cd Sales-backoffice-API

# Run with Docker
docker-compose up --build
```

Once the containers are running, the API will be available at:  
- **API Base URL:** http://localhost:8000  
- **Swagger UI:** http://localhost:8000/docs  

---

## 📌 Project Status
This project is finalized and no further development is planned.  
It serves as a clean, functional base for future sales management systems or as a learning reference for **FastAPI**, **MySQL**, and **Docker** integration.

---

## 📝 License
MIT License © 2025 — Diogo Falardo
