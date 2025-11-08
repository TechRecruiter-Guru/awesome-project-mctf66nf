import { NextRequest, NextResponse } from 'next/server';
import { verifyCode, markCodeAsUsed } from '@/lib/codeGenerator';
import { getOrder, updateOrderStatus } from '@/lib/orderManager';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { code } = body;

    if (!code) {
      return NextResponse.json(
        { message: 'Confirmation code is required' },
        { status: 400 }
      );
    }

    const verification = verifyCode(code);

    if (!verification.valid) {
      return NextResponse.json(
        { valid: false, message: verification.message },
        { status: 400 }
      );
    }

    const orderId = verification.orderId!;
    const order = getOrder(orderId);

    if (!order) {
      return NextResponse.json(
        { valid: false, message: 'Order not found' },
        { status: 404 }
      );
    }

    // Mark code as used
    markCodeAsUsed(code);

    // Update order status
    updateOrderStatus(orderId, 'pdf_uploaded');

    return NextResponse.json({
      valid: true,
      orderId,
      message: verification.message,
    });
  } catch (error) {
    console.error('Error verifying code:', error);
    return NextResponse.json(
      { valid: false, message: 'Verification failed' },
      { status: 500 }
    );
  }
}
