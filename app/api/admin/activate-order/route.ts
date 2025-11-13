import { NextRequest, NextResponse } from 'next/server';
import { getOrder, updateOrder } from '@/lib/orderManager';
import { createConfirmationCode } from '@/lib/codeGenerator';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { orderId } = body;

    if (!orderId) {
      return NextResponse.json(
        { message: 'Order ID is required' },
        { status: 400 }
      );
    }

    const order = await getOrder(orderId);
    if (!order) {
      return NextResponse.json(
        { message: 'Order not found' },
        { status: 404 }
      );
    }

    if (order.confirmationCode) {
      return NextResponse.json(
        {
          message: 'Order already has a confirmation code',
          confirmationCode: order.confirmationCode,
        },
        { status: 400 }
      );
    }

    // Generate confirmation code
    const confirmationCode = await createConfirmationCode(orderId);

    // Update order
    await updateOrder(orderId, {
      confirmationCode: confirmationCode.code,
      status: 'code_generated',
    });

    return NextResponse.json({
      success: true,
      confirmationCode: confirmationCode.code,
      orderId,
    });
  } catch (error) {
    console.error('Error activating order:', error);
    return NextResponse.json(
      { message: 'Failed to activate order' },
      { status: 500 }
    );
  }
}
