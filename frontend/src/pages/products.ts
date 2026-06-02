import { getProducts, createProduct } from "../api/productApi";
import { mustGet, toNumber } from "../utils/dom";
import { sortById } from "../utils/sort";
import { type Product, type ProductCreateDTO } from "../types";
import { renderProduct } from "../renderers/productRenderer";

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

  private async loadProducts() {
    try {
      this.listEl.innerHTML = "Loading products...";
      const products: Product[] = sortById(await getProducts());

      if (!products.length) {
        this.listEl.innerHTML = "<p>No products found.</p>";
        return;
      }

      this.listEl.innerHTML = products.map(p => renderProduct(p)).join("");
    } catch (error: any) {
      console.error(error);
      this.listEl.innerHTML = `<p style="color: red;">Failed to load data: ${error.message}</p>`;
    }
  }

  private validateInput(name: string, sku: string, price: number, stock: number): boolean {
    if (!name || !sku || !price || !stock) {
      alert("All fields are required");
      return false;
    }
    if (price === null || price <= 0) {
      alert("Price must be greater than 0");
      return false;
    }
    if (!/^\d+(\.\d{1,2})?$/.test(price.toString())) {
      alert("Price can have a maximum of 2 decimal places");
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

      if (price === null || stock === null) {
        alert("Please enter valid numbers for Price and Stock");
        return;
      }

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