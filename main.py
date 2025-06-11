from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import asyncpg
import os
from fastapi.middleware.cors import CORSMiddleware

# CORS設定（v0 と繋ぐために必要）
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要なら特定のURLに絞ってOK
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase接続情報
DATABASE_URL = os.environ.get("DATABASE_URL")

# 注文データの入力スキーマ
class OrderCreate(BaseModel):
    poster: str
    item: str
    quantity: int
    delivery_date: str  # ここが今回の修正ポイント！（strに変更）

# 注文データの出力スキーマ
class Order(BaseModel):
    id: int
    created_at: str
    poster: str
    item: str
    quantity: int
    delivery_date: str

# 注文登録エンドポイント
@app.post("/orders", response_model=Order)
async def create_order(order: OrderCreate):
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        row = await conn.fetchrow("""
            INSERT INTO orders (poster, item, quantity, delivery_date)
            VALUES ($1, $2, $3, $4)
            RETURNING id, created_at, poster, item, quantity, delivery_date
        """, order.poster, order.item, order.quantity, order.delivery_date)
        await conn.close()
        return dict(row)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="注文の登録に失敗しました")

# 全件取得エンドポイント（確認用）
@app.get("/orders", response_model=List[Order])
async def get_orders():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        rows = await conn.fetch("SELECT id, created_at, poster, item, quantity, delivery_date FROM orders ORDER BY id DESC")
        await conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="注文の取得に失敗しました")
