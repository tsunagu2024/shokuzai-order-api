from fastapi import FastAPI
from pydantic import BaseModel
import asyncpg
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # v0からのアクセス許可
    allow_methods=["*"],
    allow_headers=["*"],
)

# 環境変数からDB接続情報を取得
DB_URL = os.getenv("DATABASE_URL")

class Order(BaseModel):
    poster: str
    item: str
    quantity: str   # ← ここをstrに修正！（今回の本質部分）
    deliveryDate: str  # ISO8601形式の日付文字列

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
