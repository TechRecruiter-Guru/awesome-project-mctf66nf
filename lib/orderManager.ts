import { kv } from '@vercel/kv';
import { Order, TemplateType, OrderStatus } from './types';

const ORDERS_KEY = 'orders';

export async function readOrders(): Promise<Record<string, Order>> {
  try {
    const orders = await kv.get<Record<string, Order>>(ORDERS_KEY);
    return orders || {};
  } catch (error) {
    console.error('Error reading orders from KV:', error);
    return {};
  }
}

export async function writeOrders(orders: Record<string, Order>): Promise<void> {
  try {
    await kv.set(ORDERS_KEY, orders);
  } catch (error) {
    console.error('Error writing orders to KV:', error);
    throw error;
  }
}

export function generateOrderId(): string {
  const now = new Date();
  const datePart = now.toISOString().slice(0, 10).replace(/-/g, '');
  const timePart = now.toISOString().slice(11, 16).replace(':', '');
  const randomPart = Math.floor(Math.random() * 1000).toString().padStart(3, '0');

  return `${datePart}-${timePart}-${randomPart}`;
}

export async function createOrder(templateType: TemplateType, email: string, companyName: string): Promise<Order> {
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

  const orders = await readOrders();
  orders[orderId] = order;
  await writeOrders(orders);

  return order;
}

export async function getOrder(orderId: string): Promise<Order | null> {
  const orders = await readOrders();
  return orders[orderId] || null;
}

export async function updateOrder(orderId: string, updates: Partial<Order>): Promise<Order | null> {
  const orders = await readOrders();
  const order = orders[orderId];

  if (!order) {
    return null;
  }

  const updatedOrder = { ...order, ...updates };
  orders[orderId] = updatedOrder;
  await writeOrders(orders);

  return updatedOrder;
}

export async function updateOrderStatus(orderId: string, status: OrderStatus): Promise<Order | null> {
  return updateOrder(orderId, { status });
}

export async function getAllOrders(): Promise<Order[]> {
  const orders = await readOrders();
  return Object.values(orders).sort((a, b) =>
    new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
  );
}

export async function getOrdersByStatus(status: OrderStatus): Promise<Order[]> {
  const allOrders = await getAllOrders();
  return allOrders.filter(order => order.status === status);
}
