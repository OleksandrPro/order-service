import { type Customer } from "../types";

export function renderCustomer(customer: Customer): string {
  return `
    <div class="customer-card">
      <div class="card-main">
        <span><strong>#${customer.id}</strong> ${customer.name}</span>
    </div>
      <a href="mailto:${customer.email}">
        ${customer.email}
      </a>
    </div>
  `;
}