import { NextRequest, NextResponse } from 'next/server';
import { getOrder, updateOrderStatus } from '@/lib/orderManager';
import { populateTemplate, makeSelfContained } from '@/lib/templateParser';
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
    let populatedHtml = populateTemplate(order.templateType, safetyCaseData);

    // Make sure the HTML is self-contained
    populatedHtml = makeSelfContained(populatedHtml);

    // Update order status to completed
    updateOrderStatus(orderId, 'completed');

    // Return the HTML as a blob
    return new NextResponse(populatedHtml, {
      headers: {
        'Content-Type': 'text/html',
        'Content-Disposition': `attachment; filename="safety-case-${safetyCaseData.companyName.toLowerCase().replace(/\s+/g, '-')}.html"`,
      },
    });
  } catch (error: any) {
    console.error('Error generating download:', error);
    return NextResponse.json(
      { message: error.message || 'Failed to generate download' },
      { status: 500 }
    );
  }
}
