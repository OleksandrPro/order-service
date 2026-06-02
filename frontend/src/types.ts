export interface Customer {
  id: number;
  name: string;
  email: string;
}

export interface CustomerCreateDTO {
  name: string;
  email: string;
}

export interface Product {
  id: number;
  name: string;
  sku: string;
  price: number;
  stock: number;
}

export interface ProductCreateDTO {
  name: string;
  sku: string;
  price: number;
  stock: number;
}

export interface OrderItem {
  product_id: number;
  quantity: number;
  price_at_purchase?: number; 
}

export interface Order {
  id: number;
  customer_id: number;
  total_amount: number;
  items: OrderItem[];
}

export interface OrderCreateDTO {
  customer_id: number;
  items: OrderItem[];
}