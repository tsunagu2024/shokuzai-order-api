"use client";

import { useState } from "react";
import { submitOrder } from "./actions";

export function OrderForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(formData: FormData) {
    setIsSubmitting(true);
    try {
      await submitOrder(formData);
      alert("注文を送信しました！");
    } catch (error) {
      console.error("注文の送信に失敗しました:", error);
      alert("注文の送信に失敗しました。もう一度お試しください。");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form action={handleSubmit} className="space-y-4">
      <div>
        <label>投稿者名</label>
        <input name="poster" type="text" required className="border w-full p-2 rounded" />
      </div>
      <div>
        <label>食材名</label>
        <input name="item" type="text" required className="border w-full p-2 rounded" />
      </div>
      <div>
        <label>数量</label>
        <input name="quantity" type="text" required className="border w-full p-2 rounded" />
      </div>
      <div>
        <label>配達希望日</label>
        <input name="deliveryDate" type="date" required className="border w-full p-2 rounded" />
      </div>
      <button
        type="submit"
        disabled={isSubmitting}
        className="bg-green-500 text-white py-2 px-4 rounded disabled:opacity-50"
      >
        {isSubmitting ? "送信中..." : "注文を送信"}
      </button>
    </form>
  );
}
