import { NextRequest, NextResponse } from 'next/server';
import { createOrder } from '@/lib/orderManager';
import { TemplateType } from '@/lib/types';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { templateType, email, companyName } = body;

    if (!templateType) {
      return NextResponse.json(
        { message: 'Template type is required' },
        { status: 400 }
      );
    }

    if (!email || !companyName) {
      return NextResponse.json(
        { message: 'Email and company name are required' },
        { status: 400 }
      );
    }

    const validTemplates: TemplateType[] = ['humanoid', 'amr', 'cobot', 'drone', 'inspection'];
    if (!validTemplates.includes(templateType)) {
      return NextResponse.json(
        { message: 'Invalid template type' },
        { status: 400 }
      );
    }

    const order = await createOrder(templateType, email, companyName);

    return NextResponse.json({ success: true, order }, { status: 201 });
  } catch (error) {
    console.error('Error creating order:', error);
    return NextResponse.json(
      { message: 'Failed to create order' },
      { status: 500 }
    );
  }
}
