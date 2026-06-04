from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True)
    password = Column(String(255))


class Restaurant(Base):
    __tablename__ = "restaurants"

    restaurant_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    location = Column(String(100))
    is_deleted = Column(Boolean, default=False)


class FoodItem(Base):
    __tablename__ = "food_items"

    food_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    price = Column(Float)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"))
    is_deleted = Column(Boolean, default=False)


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100), unique=True)


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    food_id = Column(Integer, ForeignKey("food_items.food_id"))
    quantity = Column(Integer)
    total_amount = Column(Float)
    status = Column(String(30), default="Pending")
