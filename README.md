# Online Food Ordering System

## Objective

Backend application to manage Restaurants, Food Items, Customers, and Orders.

## Tech Stack

- Python 3
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite / MySQL
- JWT Authentication

## Features

### Restaurant Management
- Add Restaurant
- View Restaurants
- Update Restaurant
- Soft Delete Restaurant

### Food Item Management
- Add Food Item
- View Food Items
- Update Food Item
- Soft Delete Food Item

### Customer Management
- Add Customer
- View Customers

### Order Management
- Place Order
- View Orders
- Cancel Order
- Update Order Status

### Business Rules
- Customer must exist before placing order
- Food item must exist before ordering
- Order total calculated automatically
- Cancelled orders cannot be modified

### Bonus Features
- JWT Authentication
- Pagination
- Search & Filters
- Soft Delete
- Swagger Documentation

## Run Project

pip install -r requirements.txt
uvicorn main:app --reload

Swagger:

http://127.0.0.1:8000/docs

Explanation

I created five tables: Users, Restaurants, Food Items, Customers, and Orders.

Restaurants contain food items, customers place orders, and order totals are calculated automatically using food price and quantity.

JWT Authentication is implemented using Register and Login APIs.

Soft delete is implemented for Restaurants and Food Items.

Business rules ensure valid customers, valid food items, automatic total calculation, and prevent updates to cancelled orders.

Submission Files
Source Code
SQL Schema Script
SQL Report Queries
Postman Collection
README

