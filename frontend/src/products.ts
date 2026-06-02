import { getProducts, createProduct } from "./api/productApi";
import { mustGet, toNumber } from "./utils/dom";
import { type Product, type ProductCreateDTO } from "./types";

class ProductsPage {
  private listEl: HTMLDivElement;
  private formEl: HTMLFormElement;
  private nameInput: HTMLInputElement;
  private skuInput: HTMLInputElement;
  private priceInput: HTMLInputElement;
  private stockInput: HTMLInputElement;
  private submitBtn: HTMLButtonElement;

  constructor() {
    this.listEl = mustGet<HTMLDivElement>("list");
    this.formEl = mustGet<HTMLFormElement>("form");
    this.nameInput = mustGet<HTMLInputElement>("name");
    this.skuInput = mustGet<HTMLInputElement>("sku");
    this.priceInput = mustGet<HTMLInputElement>("price");
    this.stockInput = mustGet<HTMLInputElement>("stock");
    this.submitBtn = this.formEl.querySelector("button") as HTMLButtonElement;

    this.bindEvents();
  }

  public async init() {
    await this.loadProducts();
  }

  private renderProduct(p: Product): string {
    return `
      <div style="padding: 8px 0; border-bottom: 1px solid #eee; display: flex; justify-content: space-between;">
        <span><strong>#${p.id}</strong> | ${p.name} <small>(SKU: ${p.sku})</small></span>
        <span>$${p.price} | Stock: ${p.stock}</span>
      </div>
    `;
  }

  private async loadProducts() {
    try {
      this.listEl.innerHTML = "Loading products...";
      const products: Product[] = await getProducts();

      if (!products.length) {
        this.listEl.innerHTML = "<p>No products found.</p>";
        return;
      }

      this.listEl.innerHTML = products.map(p => this.renderProduct(p)).join("");
    } catch (error: any) {
      console.error(error);
      this.listEl.innerHTML = `<p style="color: red;">Failed to load data: ${error.message}</p>`;
    }
  }

  private validateInput(name: string, sku: string, price: number | null, stock: number | null): boolean {
    if (!name || !sku) {
      alert("Name and SKU are required");
      return false;
    }
    if (price === null || price <= 0) {
      alert("Price must be greater than 0");
      return false;
    }
    if (stock === null || stock < 0) {
      alert("Stock cannot be negative");
      return false;
    }
    return true;
  }

  private bindEvents() {
    this.formEl.addEventListener("submit", async (e) => {
      e.preventDefault();

      const name = this.nameInput.value.trim();
      const sku = this.skuInput.value.trim();
      const price = toNumber(this.priceInput.value);
      const stock = toNumber(this.stockInput.value);

      if (!this.validateInput(name, sku, price, stock)) return;

      this.submitBtn.disabled = true;

      try {
        const newProduct: ProductCreateDTO = { name, sku, price: price as number, stock: stock as number };
        await createProduct(newProduct);
        this.formEl.reset();
        await this.loadProducts();
      } catch (error: any) {
        alert(`Failed to create product: ${error.message}`);
      } finally {
        this.submitBtn.disabled = false;
      }
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const page = new ProductsPage();
  page.init();
});