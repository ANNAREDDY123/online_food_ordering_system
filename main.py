from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models
import schemas
from database import Base, engine, get_db
from auth import hash_password, verify_password, create_access_token

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Online Food Ordering System")


@app.get("/")
def home():
    return {"message": "Online Food Ordering System API Running"}


# ---------------- AUTH ----------------

@app.post("/register")
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):

    existing = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = models.User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}


@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username})

    return {"access_token": token}


# ---------------- RESTAURANTS ----------------

@app.post("/restaurants")
def add_restaurant(
    restaurant: schemas.RestaurantCreate,
    db: Session = Depends(get_db)
):

    new_restaurant = models.Restaurant(**restaurant.dict())

    db.add(new_restaurant)
    db.commit()

    return {"message": "Restaurant added successfully"}


@app.get("/restaurants")
def view_restaurants(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):

    query = db.query(models.Restaurant).filter(
        models.Restaurant.is_deleted == False
    )

    total = query.count()

    restaurants = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {"total": total, "restaurants": restaurants}


@app.put("/restaurants/{restaurant_id}")
def update_restaurant(
    restaurant_id: int,
    restaurant: schemas.RestaurantUpdate,
    db: Session = Depends(get_db)
):

    db_restaurant = db.query(models.Restaurant).filter(
        models.Restaurant.restaurant_id == restaurant_id
    ).first()

    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    for key, value in restaurant.dict(exclude_unset=True).items():
        setattr(db_restaurant, key, value)

    db.commit()

    return {"message": "Restaurant updated successfully"}


@app.delete("/restaurants/{restaurant_id}")
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):

    restaurant = db.query(models.Restaurant).filter(
        models.Restaurant.restaurant_id == restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    restaurant.is_deleted = True

    db.commit()

    return {"message": "Restaurant soft deleted"}


# ---------------- FOOD ITEMS ----------------

@app.post("/food-items")
def add_food_item(
    food: schemas.FoodItemCreate,
    db: Session = Depends(get_db)
):

    restaurant = db.query(models.Restaurant).filter(
        models.Restaurant.restaurant_id == food.restaurant_id,
        models.Restaurant.is_deleted == False
    ).first()

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    new_food = models.FoodItem(**food.dict())

    db.add(new_food)
    db.commit()

    return {"message": "Food item added successfully"}


@app.get("/food-items")
def view_food_items(
    search: str = "",
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):

    query = db.query(models.FoodItem).filter(
        models.FoodItem.is_deleted == False
    )

    if search:
        query = query.filter(
            models.FoodItem.name.like(f"%{search}%")
        )

    total = query.count()

    foods = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {"total": total, "food_items": foods}


@app.put("/food-items/{food_id}")
def update_food_item(
    food_id: int,
    food: schemas.FoodItemUpdate,
    db: Session = Depends(get_db)
):

    db_food = db.query(models.FoodItem).filter(
        models.FoodItem.food_id == food_id
    ).first()

    if not db_food:
        raise HTTPException(status_code=404, detail="Food item not found")

    for key, value in food.dict(exclude_unset=True).items():
        setattr(db_food, key, value)

    db.commit()

    return {"message": "Food item updated successfully"}


@app.delete("/food-items/{food_id}")
def delete_food_item(food_id: int, db: Session = Depends(get_db)):

    food = db.query(models.FoodItem).filter(
        models.FoodItem.food_id == food_id
    ).first()

    if not food:
        raise HTTPException(status_code=404, detail="Food item not found")

    food.is_deleted = True

    db.commit()

    return {"message": "Food item soft deleted"}


# ---------------- CUSTOMERS ----------------

@app.post("/customers")
def add_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db)
):

    new_customer = models.Customer(**customer.dict())

    db.add(new_customer)
    db.commit()

    return {"message": "Customer added successfully"}


@app.get("/customers")
def view_customers(db: Session = Depends(get_db)):
    return db.query(models.Customer).all()


# ---------------- ORDERS ----------------

@app.post("/orders")
def place_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db)
):

    customer = db.query(models.Customer).filter(
        models.Customer.customer_id == order.customer_id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    food = db.query(models.FoodItem).filter(
        models.FoodItem.food_id == order.food_id,
        models.FoodItem.is_deleted == False
    ).first()

    if not food:
        raise HTTPException(status_code=404, detail="Food item not found")

    total_amount = food.price * order.quantity

    new_order = models.Order(
        customer_id=order.customer_id,
        food_id=order.food_id,
        quantity=order.quantity,
        total_amount=total_amount
    )

    db.add(new_order)
    db.commit()

    return {
        "message": "Order placed successfully",
        "total_amount": total_amount
    }


@app.get("/orders")
def view_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()


@app.put("/orders/{order_id}")
def update_order_status(
    order_id: int,
    update: schemas.OrderStatusUpdate,
    db: Session = Depends(get_db)
):

    order = db.query(models.Order).filter(
        models.Order.order_id == order_id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status == "Cancelled":
        raise HTTPException(
            status_code=400,
            detail="Cancelled orders cannot be modified"
        )

    order.status = update.status

    db.commit()

    return {"message": "Order updated successfully"}


@app.delete("/orders/{order_id}")
def cancel_order(order_id: int, db: Session = Depends(get_db)):

    order = db.query(models.Order).filter(
        models.Order.order_id == order_id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = "Cancelled"

    db.commit()

    return {"message": "Order cancelled successfully"}
