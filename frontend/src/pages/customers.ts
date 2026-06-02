import { getCustomers, createCustomer } from "../api/customerApi";
import { mustGet } from "../utils/dom";
import { sortById } from "../utils/sort";
import { type Customer, type CustomerCreateDTO } from "../types";
import { renderCustomer } from "../renderers/customerRenderer";

class CustomerPage {
  private listEl: HTMLDivElement;
  private formEl: HTMLFormElement;
  private nameInput: HTMLInputElement;
  private emailInput: HTMLInputElement;
  private submitBtn: HTMLButtonElement;

  constructor() {
    this.listEl = mustGet<HTMLDivElement>("customer-list");
    this.formEl = mustGet<HTMLFormElement>("customer-form");
    this.nameInput = mustGet<HTMLInputElement>("customer-name");
    this.emailInput = mustGet<HTMLInputElement>("customer-email");
    this.submitBtn = this.formEl.querySelector("button") as HTMLButtonElement;

    this.bindEvents();
  }

  public async init() {
    await this.loadCustomers();
  }

  private async loadCustomers() {
    try {
      this.listEl.innerHTML = "Loading customers...";
      const customers: Customer[] = sortById(await getCustomers());

      if (!customers.length) {
        this.listEl.innerHTML = "<p>No customers found.</p>";
        return;
      }

      this.listEl.innerHTML = customers.map(c => renderCustomer(c)).join("");
    } catch (error: any) {
      console.error(error);
      this.listEl.innerHTML = `
        <p class="error-message">
          Failed to load data: ${error.message}
        </p>
      `;
    }
  }

  private validateInput(name: string, email: string): boolean {
    if (!name || !email) {
      alert("Name and email are required");
      return false;
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      alert("Invalid email format");
      return false;
    }
    return true;
  }

  private bindEvents() {
    this.formEl.addEventListener("submit", async (e) => {
      e.preventDefault();

      const name = this.nameInput.value.trim();
      const email = this.emailInput.value.trim();

      if (!this.validateInput(name, email)) return;

      this.submitBtn.disabled = true;

      try {
        const newCustomer: CustomerCreateDTO = { name, email };
        await createCustomer(newCustomer);
        this.formEl.reset();
        await this.loadCustomers();
      } catch (error: any) {
        alert(`Failed to create customer: ${error.message}`);
      } finally {
        this.submitBtn.disabled = false;
      }
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const page = new CustomerPage();
  page.init();
});