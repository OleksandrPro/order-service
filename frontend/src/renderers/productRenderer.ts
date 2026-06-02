import { type Product } from "../types";

export function renderProduct(p: Product): string {
  return `
    <div class="product-card">
      <div class="product-main">
        <span><strong>#${p.id}</strong> ${p.name}</span>
        <span class="product-sku">SKU: ${p.sku}</span>
      </div>
      <div class="product-stats">
        <span class="product-price">$${p.price}</span>
        <span class="product-stock">Stock: ${p.stock}</span>
      </div>
    </div>
  `;
}