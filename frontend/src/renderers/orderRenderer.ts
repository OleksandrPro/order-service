import { type Order, type Product } from "../types";

export function renderOrderCard(
  order: Order,
  productsMap: Map<number, Product>
): string {
  const itemsDetails = order.items
    .map((item) => {
      const productName = productsMap.get(item.product_id)?.name ?? "Unknown Product";
      const price = item.price_at_purchase ?? 0;
      const subtotal = (price * item.quantity).toFixed(2);

      return `
        <li class="order-item">
          <div class="order-item-name">${productName}</div>
          <div class="order-item-details">
            <span>Qty: ${item.quantity}</span>
            <span>Price: $${price.toFixed(2)}</span>
            <span class="order-item-subtotal">Subtotal: $${subtotal}</span>
          </div>
        </li>
      `;
    })
    .join("");

  return `
    <div class="order-card">
      <div class="order-card-header">
        <h4>Order #${order.id}</h4>
        <span class="order-total">Total: $${(order.total_amount ?? 0).toFixed(2)}</span>
      </div>
      <ul class="order-items">
        ${itemsDetails}
      </ul>
    </div>
  `;
}