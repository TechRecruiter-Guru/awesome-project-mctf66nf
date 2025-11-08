import { NextRequest, NextResponse } from 'next/server';
import { getAllOrders } from '@/lib/orderManager';

export async function GET(request: NextRequest) {
  try {
    const orders = getAllOrders();

    return NextResponse.json({ success: true, orders });
  } catch (error) {
    console.error('Error fetching orders:', error);
    return NextResponse.json(
      { success: false, message: 'Failed to fetch orders' },
      { status: 500 }
    );
  }
}
