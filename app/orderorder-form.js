"use client";

import React, { useState } from "react";
import axios from "axios";

function OrderForm() {
  const [poster, setPoster] = useState("");
  const [item, setItem] = useState("");
  const [quantity, setQuantity] = useState("");
  const [deliveryDate, setDeliveryDate] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("https://shokuzai-order-api.onrender.com/orders", {
        poster,
        item,
        quantity: parseInt(quantity),
        deliveryDate,
      });
      alert("注文が送信されました！");
      setPoster("");
      setItem("");
      setQuantity("");
      setDeliveryDate("");
    } catch (error) {
      console.error("注文送信中にエラーが発生しました", error);
      alert("送信に失敗しました。");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        type="text"
        placeholder="依頼者名"
        value={poster}
        onChange={(e) => setPoster(e.target.value)}
        className="border p-2"
      />
      <input
        type="text"
        placeholder="商品名"
        value={item}
        onChange={(e) => setItem(e.target.value)}
        className="border p-2"
      />
      <input
        type="number"
        placeholder="数量"
        value={quantity}
        onChange={(e) => setQuantity(e.target.value)}
        className="border p-2"
      />
      <input
        type="date"
        value={deliveryDate}
        onChange={(e) => setDeliveryDate(e.target.value)}
        className="border p-2"
      />
      <button type="submit" className="bg-blue-500 text-white px-4 py-2">
        送信
      </button>
    </form>
  );
}

export default OrderForm;
