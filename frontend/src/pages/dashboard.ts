import { getCustomers } from "../api/customerApi";
import { getProducts } from "../api/productApi";
import { getOrdersByCustomer } from "../api/orderApi";
import { mustGet } from "../utils/dom";

class DashboardPage {
  private customersStat: HTMLElement;
  private productsStat: HTMLElement;
  private ordersStat: HTMLElement;

  constructor() {
    this.customersStat = mustGet<HTMLElement>("stat-customers");
    this.productsStat = mustGet<HTMLElement>("stat-products");
    this.ordersStat = mustGet<HTMLElement>("stat-orders");
  }

  public async init() {
    try {
      const [customers, products] = await Promise.all([
        getCustomers(),
        getProducts()
      ]);

      this.customersStat.textContent = customers.length.toString();
      this.productsStat.textContent = products.length.toString();

      const ordersPromises = customers.map(c => getOrdersByCustomer(c.id));
      const allOrdersArrays = await Promise.all(ordersPromises);
      
      const totalOrders = allOrdersArrays.reduce((sum, orders) => sum + orders.length, 0);
      this.ordersStat.textContent = totalOrders.toString();

    } catch (error: any) {
      console.error("Failed to load dashboard stats:", error);
      this.customersStat.textContent = "Err";
      this.productsStat.textContent = "Err";
      this.ordersStat.textContent = "Err";
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const page = new DashboardPage();
  page.init();
});