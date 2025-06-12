import OrderForm from "./order-form";

export default function OrderPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center">
      <h1 className="text-3xl font-bold mb-6">食材のご注文</h1>
      <OrderForm />
    </main>
  );
}
