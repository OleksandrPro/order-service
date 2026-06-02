class AppHeader extends HTMLElement {
  connectedCallback() {
    const currentPath = window.location.pathname;
    const isActive = (path: string) => currentPath === path ? 'class="active"' : '';

    this.innerHTML = `
      <header class="main-header">
        <div class="logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/>
            <path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/>
          </svg>
          <h1>Order Service</h1>
        </div>
        <nav>
          <a href="/" ${isActive('/')}>Dashboard</a>
          <a href="/customers.html" ${isActive('/customers.html')}>Customers</a>
          <a href="/products.html" ${isActive('/products.html')}>Products</a>
          <a href="/orders.html" ${isActive('/orders.html')}>Orders</a>
        </nav>
      </header>
    `;
  }
}

customElements.define("app-header", AppHeader);