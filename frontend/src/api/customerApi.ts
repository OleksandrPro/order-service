import { CONFIG } from "../config";
import { type Customer, type CustomerCreateDTO } from "../types";
import { handleResponse } from "./apiClient";

export async function getCustomers(): Promise<Customer[]> {
  const res = await fetch(`${CONFIG.API_BASE_URL}/customers/`);
  return handleResponse<Customer[]>(res);
}

export async function createCustomer(data: CustomerCreateDTO): Promise<Customer> {
  const res = await fetch(`${CONFIG.API_BASE_URL}/customers/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse<Customer>(res);
}