from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

# DB接続関数
async def connect_db():
    return await asyncpg.connect(DATABASE_URL)

# Pydanticモデル定義（JSON受信用）
class Order(BaseModel):
    投稿日時: str
    投稿者名: str
    食材名: str
    数量: str
    配達希望日: str

# POST: JSON形式で受信
@app.post("/orders")
async def create_order(order: Order):
    conn = await connect_db()
    try:
        await conn.execute(
            """
            INSERT INTO orders (poster, item, quantity, delivery_date)
            VALUES ($1, $2, $3, $4)
            """,
            order.投稿者名,
            order.食材名,
            order.数量,
            order.配達希望日
        )
    finally:
        await conn.close()
    return {"message": "Order created successfully"}

# GET: 全件取得（確認用）
@app.get("/orders")
async def read_orders():
    conn = await connect_db()
    try:
        rows = await conn.fetch("SELECT poster, item, quantity, delivery_date FROM orders")
        results = [
            {
                "poster": row["poster"],
                "item": row["item"],
                "quantity": row["quantity"],
                "deliveryDate": str(row["delivery_date"])
            }
            for row in rows
        ]
    finally:
        await conn.close()
    return results
