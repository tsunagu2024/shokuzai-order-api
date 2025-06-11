from fastapi import FastAPI, Form
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

# DB接続関数
async def connect_db():
    return await asyncpg.connect(DATABASE_URL)

# POST: 注文受付（Form対応／quantityはstrで受取→int変換）
@app.post("/orders")
async def create_order(
    poster: str = Form(...),
    item: str = Form(...),
    quantity: str = Form(...),
    deliveryDate: str = Form(...)
):
    conn = await connect_db()
    try:
        await conn.execute(
            """
            INSERT INTO orders (poster, item, quantity, delivery_date)
            VALUES ($1, $2, $3, $4)
            """,
            poster,
            item,
            int(quantity),
            deliveryDate
        )
    finally:
        await conn.close()
    return {"message": "Order created successfully"}

# GET: 全件取得
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
