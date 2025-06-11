"use client"

import { useState } from "react"

export default function OrderForm() {
  const [formData, setFormData] = useState({
    poster: "",
    item: "",
    quantity: "",
    deliveryDate: "",
  })

  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    try {
      const response = await fetch("https://shokuzai-order-api.onrender.com/orders", {
        method: "POST",
        body: new URLSearchParams(formData as any),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      alert("注文が送信されました！")
    } catch (error) {
      console.error("注文の送信に失敗しました:", error)
      alert("注文の送信に失敗しました。もう一度お試しください。")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 w-full max-w-md">
      <input
        type="text"
        name="poster"
        placeholder="投稿者名"
        value={formData.poster}
        onChange={handleChange}
        required
        className="border p-2 rounded w-full"
      />
      <input
        type="text"
        name="item"
        placeholder="食材名"
        value={formData.item}
        onChange={handleChange}
        required
        className="border p-2 rounded w-full"
      />
      <input
        type="text"
        name="quantity"
        placeholder="数量"
        value={formData.quantity}
        onChange={handleChange}
        required
        className="border p-2 rounded w-full"
      />
      <input
        type="date"
        name="deliveryDate"
        value={formData.deliveryDate}
        onChange={handleChange}
        required
        className="border p-2 rounded w-full"
      />
      <button type="submit" disabled={isSubmitting} className="bg-green-500 text-white py-2 px-4 rounded">
        {isSubmitting ? "送信中..." : "注文する"}
      </button>
    </form>
  )
}
