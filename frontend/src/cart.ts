import { mustGet } from "./utils/dom";

export interface CartItem {
  product_id: number;
  name: string;
  price: number;
  quantity: number;
}

export class CartManager {
  private items: CartItem[] = [];
  private container: HTMLDivElement;

  constructor(containerId: string) {
    this.container = mustGet<HTMLDivElement>(containerId);
    this.bindEvents();
  }

  public addItem(item: CartItem) {
    const existing = this.items.find(i => i.product_id === item.product_id);
    if (existing) {
      existing.quantity += item.quantity;
    } else {
      this.items.push(item);
    }
    this.render();
  }

  public getItems() {
    return this.items;
  }

  public clear() {
    this.items = [];
    this.render();
  }

  public isEmpty() {
    return this.items.length === 0;
  }

  private removeItem(index: number) {
    this.items.splice(index, 1);
    this.render();
  }

  private renderItem(item: CartItem, index: number): string {
    const total = (item.price * item.quantity).toFixed(2);
    return `
      <div style="margin-bottom: 5px; display: flex; align-items: center; gap: 10px;">
        <span>${item.name} | Qty: ${item.quantity} | Total: $${total}</span>
        <button data-index="${index}" class="remove-btn">X</button>
      </div>
    `;
  }

  private render() {
    if (this.isEmpty()) {
      this.container.innerHTML = "<p>Cart is empty.</p>";
      return;
    }
    this.container.innerHTML = this.items.map((item, i) => this.renderItem(item, i)).join("");
  }

  private bindEvents() {
    this.container.addEventListener("click", (e) => {
      const target = e.target as HTMLElement;
      if (target.classList.contains("remove-btn")) {
        const index = Number(target.getAttribute("data-index"));
        this.removeItem(index);
      }
    });
  }
}