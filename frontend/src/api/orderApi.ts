import { CONFIG } from "../config";
import { type Order, type OrderCreateDTO } from "../types";
import { handleResponse } from "./apiClient";

export async function getOrdersByCustomer(customerId: number): Promise<Order[]> {
  const res = await fetch(`${CONFIG.API_BASE_URL}/customers/${customerId}/orders`);
  return handleResponse<Order[]>(res);
}

export async function createOrder(data: OrderCreateDTO): Promise<Order> {
  const res = await fetch(`${CONFIG.API_BASE_URL}/orders/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse<Order>(res);
}