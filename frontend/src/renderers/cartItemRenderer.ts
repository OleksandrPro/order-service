import type { CartItem } from "../types";

export function renderCartItem(item: CartItem, index: number): string {
    const total = (item.price * item.quantity).toFixed(2);
    
    return `
      <div class="cart-card">
        <div class="card-main">
          <strong>${item.name}</strong>
          <span class="card-subtext">Qty: ${item.quantity} × $${item.price}</span>
        </div>
        <div class="cart-actions">
          <span class="cart-total">$${total}</span>
          <button data-index="${index}" class="remove-btn">X</button>
        </div>
      </div>
    `;
  }