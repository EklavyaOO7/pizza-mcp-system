from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import uuid

app = FastAPI(
    title="Pizza API",
    description="Pizza ordering backend for AI agents",
    version="1.0.0"
)

# ----------------------------
# In-memory storage (mock DB)
# ----------------------------
ORDERS: Dict[str, dict] = {}

MENU = [
    {"pizza": "Margherita", "sizes": ["Small", "Medium", "Large"], "price": 299},
    {"pizza": "Pepperoni", "sizes": ["Medium", "Large"], "price": 399},
    {"pizza": "Veggie Delight", "sizes": ["Small", "Medium"], "price": 349}
]

# ----------------------------
# Schemas
# ----------------------------
class OrderRequest(BaseModel):
    pizza: str
    size: str

class OrderResponse(BaseModel):
    order_id: str
    eta: str
    status: str

# ----------------------------
# Endpoints
# ----------------------------

@app.get("/menu")
def get_menu():
    return {"menu": MENU}

@app.post("/order", response_model=OrderResponse)
def place_order(order: OrderRequest):
    if not any(item["pizza"] == order.pizza for item in MENU):
        raise HTTPException(status_code=400, detail="Pizza not available")

    order_id = str(uuid.uuid4())[:8]

    ORDERS[order_id] = {
        "pizza": order.pizza,
        "size": order.size,
        "status": "Preparing",
        "eta": "30 minutes"
    }

    return {
        "order_id": order_id,
        "eta": "30 minutes",
        "status": "Preparing"
    }

@app.get("/order/{order_id}")
def track_order(order_id: str):
    if order_id not in ORDERS:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "order_id": order_id,
        **ORDERS[order_id]
    }
