"use client"

import { useState } from "react"
import axios from "axios"

export default function OrderForm() {
  const [poster, setPoster] = useState("")
  const [item, setItem] = useState("")
  const [quantity, setQuantity] = useState("")
  const [deliveryDate, setDeliveryDate] = useState("")

  const handleSubmit = async (e) => {
    e.preventDefault()

    const formData = new FormData()
    formData.append("poster", poster)
    formData.append("item", item)
    formData.append("quantity", quantity)
    formData.append("deliveryDate", deliveryDate)

    try {
      await axios.post(
        "https://shokuzai-order-api.onrender.com/orders",
        formData
      )
      alert("注文が送信されました！")
      setPoster("")
      setItem("")
      setQuantity("")
      setDeliveryDate("")
    } catch (error) {
      console.error(error)
      alert("送信に失敗しました")
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label>投稿者:</label>
        <input
          type="text"
          value={poster}
          onChange={(e) => setPoster(e.target.value)}
          required
        />
      </div>
      <div>
        <label>商品名:</label>
        <input
          type="text"
          value={item}
          onChange={(e) => setItem(e.target.value)}
          required
        />
      </div>
      <div>
        <label>数量:</label>
        <input
          type="number"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
          required
        />
      </div>
      <div>
        <label>配達日:</label>
        <input
          type="date"
          value={deliveryDate}
          onChange={(e) => setDeliveryDate(e.target.value)}
          required
        />
      </div>
      <button type="submit">送信</button>
    </form>
  )
}
