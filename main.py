from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import asyncpg

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 環境変数からDB URLを取得
DATABASE_URL = os.getenv("DATABASE_URL")

# Pydanticモデル (Supabaseのordersテーブルに合わせて修正)
class Order(BaseModel):
    poster: str
    item: str
    quantity: int
    delivery_date: str

# データベース接続用非同期関数
async def connect_db():
    return await asyncpg.connect(DATABASE_URL)

# POST: 新規注文登録API
@app.post("/orders")
async def create_order(order: Order):
    conn = await connect_db()
    try:
        await conn.execute(
            """
            INSERT INTO orders (poster, item, quantity, delivery_date)
            VALUES ($1, $2, $3, $4)
            """,
            order.poster,
            order.item,
            order.quantity,
            order.delivery_date
        )
    finally:
        await conn.close()
    return {"message": "Order created successfully"}

# GET: 確認用の全件取得API
@app.get("/orders", response_model=List[Order])
async def read_orders():
    conn = await connect_db()
    try:
        rows = await conn.fetch("SELECT poster, item, quantity, delivery_date FROM orders")
        orders = [Order(**dict(row)) for row in rows]
    finally:
        await conn.close()
    return orders
