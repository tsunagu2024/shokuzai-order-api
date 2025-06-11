from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncpg
import os

app = FastAPI()

# CORS設定 (v0側との通信を許可)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番運用時は特定のドメインに制限するのが推奨
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 環境変数からDB接続情報を取得
DB_URL = os.getenv("DATABASE_URL")

# データモデル（v0と合わせて quantityはstr型に修正！）
class Order(BaseModel):
    poster: str
    item: str
    quantity: str  # ←ここが重要（自由入力の数量なのでstr型）
    deliveryDate: str  # ISO8601形式の日付 (例: "2025-06-12")

# 注文登録API（POST）
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

# 注文取得API（GET）
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
        return result
    finally:
        await conn.close()
