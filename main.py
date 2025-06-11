from fastapi import FastAPI
from pydantic import BaseModel
import asyncpg
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_URL = os.getenv("DATABASE_URL")

class Order(BaseModel):
    poster: str
    item: str
    quantity: str
    deliveryDate: str  # ここはAPI受け取り時は文字列のままでOK

@app.post("/orders")
async def create_order(order: Order):
    conn = await asyncpg.connect(DB_URL)
    try:
        # ここで文字列→日付変換を追加
        delivery_date_obj = datetime.strptime(order.deliveryDate, "%Y-%m-%d").date()

        await conn.execute("""
            INSERT INTO orders (poster, item, quantity, delivery_date)
            VALUES ($1, $2, $3, $4)
        """, order.poster, order.item, order.quantity, delivery_date_obj)
    finally:
        await conn.close()

    return {"message": "Order created successfully"}

@app.get("/orders")
async def get_orders():
    conn = await asyncpg.connect(DB_URL)
    try:
        rows = await conn.fetch("""
            SELECT id, created_at, poster, item, quantity, delivery_date
            FROM orders
            ORDER BY created_at DESC
        """)
    finally:
        await conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row["id"],
            "created_at": row["created_at"].isoformat(),
            "poster": row["poster"],
            "item": row["item"],
            "quantity": row["quantity"],
            "delivery_date": row["delivery_date"].isoformat()
        })
    return result
