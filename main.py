from datetime import date
from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
import os

app = FastAPI()

# CORS設定（v0との通信許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase(Postgres)に接続する
DATABASE_URL = os.environ.get("DATABASE_URL")

@app.post("/orders")
async def create_order(
    poster: str = Form(...),
    item: str = Form(...),
    quantity: int = Form(...),
    deliveryDate: str = Form(...)
):
    try:
        # deliveryDate（文字列）を日付型に変換
        delivery_date_obj = date.fromisoformat(deliveryDate)

        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute(
            """
            INSERT INTO orders (poster, item, quantity, delivery_date)
            VALUES ($1, $2, $3, $4)
            """,
            poster, item, quantity, delivery_date_obj
        )
        await conn.close()
        return {"message": "Order created successfully"}
    except Exception as e:
        print("DB Error:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
