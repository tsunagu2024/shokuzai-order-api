from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncpg
import os

app = FastAPI()

DB_URL = "postgresql://postgres:tsunagu.2024@db.jnuspnuovbqshzghmvlh.supabase.co:5432/postgres"

class Order(BaseModel):
    poster: str
    item: str
    quantity: int
    deliveryDate: str

@app.post("/orders")
async def create_order(order: Order):
    conn = await asyncpg.connect(DB_URL)
    try:
        await conn.execute("""
            INSERT INTO orders (poster, item, quantity, delivery_date)
            VALUES ($1, $2, $3, $4)
        """, order.poster, order.item, order.quantity, order.deliveryDate)
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
    finally:
        await conn.close()

    return result
