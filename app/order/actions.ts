"use server";

export async function submitOrder(formData: FormData) {
  const poster = formData.get("poster") as string;
  const item = formData.get("item") as string;
  const quantity = formData.get("quantity") as string;
  const deliveryDate = formData.get("deliveryDate") as string;

  const formPayload = new FormData();
  formPayload.append("poster", poster);
  formPayload.append("item", item);
  formPayload.append("quantity", quantity);
  formPayload.append("deliveryDate", deliveryDate);

  try {
    const response = await fetch("https://shokuzai-order-api.onrender.com/orders", {
      method: "POST",
      body: formPayload,  // ✅ ここがポイントです
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  } catch (error) {
    console.error("注文の送信に失敗しました:", error);
    throw error;
  }
}
