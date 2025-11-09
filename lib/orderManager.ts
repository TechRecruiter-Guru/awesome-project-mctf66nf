import fs from 'fs';
import path from 'path';
import { Order, TemplateType, OrderStatus } from './types';

// Use /tmp directory on serverless environments like Vercel
const isServerless = process.env.VERCEL || process.env.AWS_LAMBDA_FUNCTION_NAME;
const DATA_DIR = isServerless ? '/tmp' : path.join(process.cwd(), 'data');
const ORDERS_FILE = path.join(DATA_DIR, 'orders.json');

export function readOrders(): Record<string, Order> {
  try {
    const data = fs.readFileSync(ORDERS_FILE, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    return {};
  }
}

export function writeOrders(orders: Record<string, Order>): void {
  fs.writeFileSync(ORDERS_FILE, JSON.stringify(orders, null, 2), 'utf-8');
}

export function generateOrderId(): string {
  const now = new Date();
  const datePart = now.toISOString().slice(0, 10).replace(/-/g, '');
  const timePart = now.toISOString().slice(11, 16).replace(':', '');

  const orders = readOrders();
  const existingOrders = Object.keys(orders).filter(id =>
    id.startsWith(`${datePart}-${timePart}`)
  );

  const counter = existingOrders.length + 1;
  const counterStr = counter.toString().padStart(3, '0');

  return `${datePart}-${timePart}-${counterStr}`;
}

export function createOrder(templateType: TemplateType, email: string, companyName: string): Order {
  const orderId = generateOrderId();
  const order: Order = {
    orderId,
    templateType,
    email,
    companyName,
    createdAt: new Date().toISOString(),
    status: 'pending_payment',
    confirmationCode: null,
    pdfUploaded: false,
    htmlGenerated: false,
  };

  const orders = readOrders();
  orders[orderId] = order;
  writeOrders(orders);

  return order;
}

export function getOrder(orderId: string): Order | null {
  const orders = readOrders();
  return orders[orderId] || null;
}

export function updateOrder(orderId: string, updates: Partial<Order>): Order | null {
  const orders = readOrders();
  const order = orders[orderId];

  if (!order) {
    return null;
  }

  const updatedOrder = { ...order, ...updates };
  orders[orderId] = updatedOrder;
  writeOrders(orders);

  return updatedOrder;
}

export function updateOrderStatus(orderId: string, status: OrderStatus): Order | null {
  return updateOrder(orderId, { status });
}

export function getAllOrders(): Order[] {
  const orders = readOrders();
  return Object.values(orders).sort((a, b) =>
    new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
  );
}

export function getOrdersByStatus(status: OrderStatus): Order[] {
  return getAllOrders().filter(order => order.status === status);
}
