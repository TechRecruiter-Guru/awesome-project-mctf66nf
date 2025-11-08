import { NextRequest, NextResponse } from 'next/server';
import { getOrder } from '@/lib/orderManager';
import { populateTemplate } from '@/lib/templateParser';
import { SafetyCaseData } from '@/lib/types';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { orderId, data } = body;

    if (!orderId || !data) {
      return NextResponse.json(
        { message: 'Order ID and data are required' },
        { status: 400 }
      );
    }

    const order = getOrder(orderId);
    if (!order) {
      return NextResponse.json(
        { message: 'Order not found' },
        { status: 404 }
      );
    }

    const safetyCaseData: SafetyCaseData = data;
    const populatedHtml = populateTemplate(order.templateType, safetyCaseData);

    return NextResponse.json({
      success: true,
      html: populatedHtml,
    });
  } catch (error: any) {
    console.error('Error populating template:', error);
    return NextResponse.json(
      { message: error.message || 'Failed to populate template' },
      { status: 500 }
    );
  }
}
