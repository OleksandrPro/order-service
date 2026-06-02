import { CONFIG } from "../config";
import { type Product, type ProductCreateDTO } from "../types";
import { handleResponse } from "./apiClient";

export async function getProducts(): Promise<Product[]> {
  const res = await fetch(`${CONFIG.API_BASE_URL}/products/`);
  return handleResponse<Product[]>(res);
}

export async function createProduct(data: ProductCreateDTO): Promise<Product> {
  const res = await fetch(`${CONFIG.API_BASE_URL}/products/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse<Product>(res);
}