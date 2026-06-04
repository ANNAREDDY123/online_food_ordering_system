from pydantic import BaseModel
from typing import Optional

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class RestaurantCreate(BaseModel):
    name: str
    location: str

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None

class FoodItemCreate(BaseModel):
    name: str
    price: float
    restaurant_id: int

class FoodItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

class CustomerCreate(BaseModel):
    name: str
    phone: str
    email: str

class OrderCreate(BaseModel):
    customer_id: int
    food_id: int
    quantity: int


class OrderStatusUpdate(BaseModel):
    status: str
