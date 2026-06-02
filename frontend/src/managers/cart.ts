import { mustGet } from "../utils/dom";
import { renderCartItem } from "../renderers/cartItemRenderer";
import { type CartItem } from "../types";

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

  private render() {
    if (this.isEmpty()) {
      this.container.innerHTML = "<p>Cart is empty.</p>";
      return;
    }
    this.container.innerHTML = this.items.map((item, i) => renderCartItem(item, i)).join("");
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