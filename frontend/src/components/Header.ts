class AppHeader extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <header>
        <h1>Order Service</h1>
        <nav>
          <a href="/">Main page</a> |
          <a href="/customers.html">Customers</a> |
          <a href="/products.html">Products</a> |
          <a href="/orders.html">Orders</a>
        </nav>
        <hr />
      </header>
    `;
  }
}

customElements.define("app-header", AppHeader);