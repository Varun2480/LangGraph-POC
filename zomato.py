import uuid
import random
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

# Provided restaurant data (from your notebook)
restaurants_data = {
    "Pizza": ["Dominos", "Pizza Hut", "Luigi's Pizzeria"],
    "Burger": ["McDonald's", "Burger King", "Shake Shack"],
    "Sushi": ["Nobu", "Sushi Samba", "Kura Sushi"], # Assuming "obu" was a typo for "Nobu"
    "Pasta": ["Olive Garden", "Carrabba's", "Maggiano's"],
    "Salad": ["Sweetgreen", "Chopt", "Saladworks"],
    "Ice Cream": ["Baskin Robbins", "Ben & Jerry's", "Cold Stone Creamery"]
}

# Create a flat set of all unique restaurant names for efficient lookup
ALL_RESTAURANTS = set()
for dish_restaurants in restaurants_data.values():
    for restaurant in dish_restaurants:
        ALL_RESTAURANTS.add(restaurant)

app = FastAPI(
    title="Restaurant Order API",
    description="An API to get dummy order details for a specific dish from a restaurant.",
    version="1.1.0"
)

# Pydantic model for the response
class OrderDetails(BaseModel):
    order_id: str
    restaurant_name: str
    items: List[str] # This will now contain the dish_name you pass
    total_amount: float
    currency: str = "USD"
    ordered_at: datetime
    estimated_arrival_time: datetime
    payment_mode: str
    status: str
    delivery_address: str
    customer_notes: Optional[str] = None

# Dummy data generators (excluding items)
def generate_dummy_payment_mode():
    return random.choice(["Credit Card", "Debit Card", "Net Banking", "Cash on Delivery", "UPI"])

def generate_dummy_status():
    return random.choice(["Order Placed", "Preparing", "Out for Delivery", "Delivered"])


@app.get("/orders/{restaurant_name}", response_model=OrderDetails)
async def get_order_details(
    restaurant_name: str,
    dish_name: str = Query(..., description="The name of the dish ordered.")
):
    """
    Retrieves dummy order details for a specific dish from a given restaurant.
    - **restaurant_name**: The name of the restaurant (must be one of the known restaurants).
    - **dish_name**: The specific dish you want in the order details.
    """
    if restaurant_name not in ALL_RESTAURANTS:
        raise HTTPException(status_code=404, detail=f"Restaurant '{restaurant_name}' not found.")

    # You could add validation here to check if the dish_name is typically served
    # by that category of restaurant, but for now, we'll accept any dish_name.
    # For example:
    # category_found = False
    # for category, names in restaurants_data.items():
    #     if restaurant_name in names:
    #         # A simple check, could be more sophisticated
    #         if dish_name.lower().startswith(category.lower()[:3]):
    #             category_found = True
    #         break
    # if not category_found:
    #     print(f"Warning: Dish '{dish_name}' might not typically be from a '{category}' type restaurant like '{restaurant_name}'.")


    current_time = datetime.now()
    order_details = OrderDetails(
        order_id=str(uuid.uuid4()),
        restaurant_name=restaurant_name,
        items=[dish_name], # Use the provided dish_name
        total_amount=round(random.uniform(5.0, 50.0), 2), # Adjusted range for a single item
        ordered_at=current_time,
        estimated_arrival_time=current_time + timedelta(minutes=random.randint(20, 60)),
        payment_mode=generate_dummy_payment_mode(),
        status=generate_dummy_status(),
        delivery_address="123 Main St, Anytown, USA",
        customer_notes=random.choice([None, f"Please ensure the {dish_name} is fresh!", "Call upon arrival."])
    )
    return order_details

# To run this app:
# 1. Save it as main.py
# 2. Install FastAPI and Uvicorn: pip install fastapi uvicorn[standard]
# 3. Run from your terminal: uvicorn main:app --reload
