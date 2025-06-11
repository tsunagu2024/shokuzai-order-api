from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncpg
import os
import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS設定：v0からアクセス可能に
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて制限可能
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 環境変数からDB接続情報を取得
DB_URL = os.getenv("DATABASE_URL")

class Order(BaseModel):
    poster: str
    item: str
    quantity: int
    deliveryDate: str  # ISO8601形式の文字列

@app.post("/orders")
async def create_order(order: Order):
    conn = await asyncpg.connect(DB_URL)
    try:
        # deliveryDateをdate型に変換
        delivery_date_obj = datetime.date.fromisoformat(order.deliveryDate)
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
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "created_at": row["created_at"].isoformat(),
                "poster": row["poster"],
                "item": row["item"],
                "quantity": row["quantity"],
                "delivery_date": row["delivery_date"].isoformat(),
            })
        return result
    finally:
        await conn.close()
