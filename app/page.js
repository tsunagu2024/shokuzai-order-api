import { OrderForm } from "./order/order-form";

export default function Home() {
  return (
    <main className="flex items-center justify-center min-h-screen bg-gradient-to-br from-green-50 to-white">
      <div className="p-6 rounded-xl shadow-xl bg-white border border-gray-200 w-full max-w-lg">
        <h1 className="text-3xl font-bold mb-6 text-center">食材オーダーフォーム</h1>
        <OrderForm />
      </div>
    </main>
  );
}
