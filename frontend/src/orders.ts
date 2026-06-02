import { createOrder, getOrdersByCustomer } from "./api/orderApi";
import { getCustomers } from "./api/customerApi";
import { getProducts } from "./api/productApi";
import { mustGet, toNumber } from "./utils/dom";
import { type Customer, type Product, type Order, type OrderCreateDTO } from "./types";
import { CartManager } from "./cart";

class OrdersPage {
  private customerSelect: HTMLSelectElement;
  private productSelect: HTMLSelectElement;
  private qtyInput: HTMLInputElement;
  private addItemBtn: HTMLButtonElement;
  private submitOrderBtn: HTMLButtonElement;
  
  private searchCustomer: HTMLSelectElement;
  private loadOrdersBtn: HTMLButtonElement;
  private ordersList: HTMLDivElement;

  private cart: CartManager;
  private productsMap = new Map<number, Product>();

  constructor() {
    this.customerSelect = mustGet<HTMLSelectElement>("order-customer");
    this.productSelect = mustGet<HTMLSelectElement>("order-product");
    this.qtyInput = mustGet<HTMLInputElement>("order-qty");
    this.addItemBtn = mustGet<HTMLButtonElement>("add-item-btn");
    this.submitOrderBtn = mustGet<HTMLButtonElement>("submit-order-btn");

    this.searchCustomer = mustGet<HTMLSelectElement>("search-customer");
    this.loadOrdersBtn = mustGet<HTMLButtonElement>("load-orders-btn");
    this.ordersList = mustGet<HTMLDivElement>("orders-list");

    this.cart = new CartManager("cart-list");

    this.bindEvents();
  }

  public async init() {
    await this.loadDependencies();
  }

  private async loadDependencies() {
    try {
      const [customers, products] = await Promise.all([
        getCustomers(),
        getProducts()
      ]);

      this.populateCustomers(customers);
      this.populateProducts(products);
    } catch (error: any) {
      alert(`Initialization failed: ${error.message}`);
    }
  }

  private populateCustomers(customers: Customer[]) {
    customers.forEach((c) => {
      this.customerSelect.appendChild(new Option(c.name, c.id.toString()));
      this.searchCustomer.appendChild(new Option(c.name, c.id.toString()));
    });
  }

  private populateProducts(products: Product[]) {
    products.forEach((p) => {
      this.productsMap.set(p.id, p);
      
      const option = new Option(`${p.name} ($${p.price})`, p.id.toString());
      this.productSelect.appendChild(option);
    });
  }

  private handleAddToCart() {
    const product_id = toNumber(this.productSelect.value);
    const quantity = toNumber(this.qtyInput.value);

    if (!product_id || !quantity || quantity <= 0) {
      return alert("Invalid selection");
    }

    const product = this.productsMap.get(product_id);
    if (!product) return alert("Product not found");

    this.cart.addItem({
      product_id,
      name: product.name,
      price: product.price,
      quantity
    });
  }

  private async handleSubmitOrder() {
    const customer_id = toNumber(this.customerSelect.value);

    if (!customer_id) return alert("Select a customer");
    if (this.cart.isEmpty()) return alert("Add at least one item to the cart");

    this.submitOrderBtn.disabled = true;

    const payload: OrderCreateDTO = {
      customer_id,
      items: this.cart.getItems().map(item => ({
        product_id: item.product_id,
        quantity: item.quantity
      }))
    };

    try {
      await createOrder(payload);
      alert("Order successfully created!");
      this.cart.clear();
      
      if (toNumber(this.searchCustomer.value) === customer_id) {
        await this.handleLoadOrders();
      }
    } catch (error: any) {
      alert(`Error creating order: ${error.message}`);
    } finally {
      this.submitOrderBtn.disabled = false;
    }
  }

  private renderOrderCard(order: Order): string {
    const itemsDetails = order.items.map((i) => {
      const productName = this.productsMap.get(i.product_id)?.name ?? "Unknown Product";
      return `
        <li style="margin-left: 20px;">
          ${productName} | Qty: ${i.quantity} | Price: $${i.price_at_purchase ?? 'N/A'}
        </li>
      `;
    }).join("");

    return `
      <div style="border: 1px solid #ccc; border-radius: 4px; padding: 10px; margin-top: 10px;">
        <h4 style="margin: 0 0 10px 0;">Order #${order.id} | Total: $${order.total_amount ?? 0}</h4>
        <ul style="margin: 0; padding: 0; list-style-type: none;">
          ${itemsDetails}
        </ul>
      </div>
    `;
  }

  private async handleLoadOrders() {
    const customerId = toNumber(this.searchCustomer.value);
    if (!customerId) return;

    this.ordersList.innerHTML = "Loading orders...";

    try {
      const orders = await getOrdersByCustomer(customerId);
      
      if (!orders.length) {
        this.ordersList.innerHTML = "<p>No orders found for this customer.</p>";
        return;
      }

      this.ordersList.innerHTML = orders.map(o => this.renderOrderCard(o)).join("");
    } catch (error: any) {
      this.ordersList.innerHTML = `<p style="color: red;">Failed to load orders: ${error.message}</p>`;
    }
  }

  private bindEvents() {
    this.addItemBtn.addEventListener("click", () => this.handleAddToCart());
    this.submitOrderBtn.addEventListener("click", () => this.handleSubmitOrder());
    this.loadOrdersBtn.addEventListener("click", () => this.handleLoadOrders());
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const page = new OrdersPage();
  page.init();
});