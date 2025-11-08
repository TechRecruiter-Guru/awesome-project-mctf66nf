import { NextRequest, NextResponse } from 'next/server';
import { extractSafetyCaseData } from '@/lib/claude';
import { getOrder } from '@/lib/orderManager';
import pdfParse from 'pdf-parse';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { pdfData, orderId } = body;

    if (!pdfData || !orderId) {
      return NextResponse.json(
        { message: 'PDF data and order ID are required' },
        { status: 400 }
      );
    }

    // Verify order exists
    const order = getOrder(orderId);
    if (!order) {
      return NextResponse.json(
        { message: 'Order not found' },
        { status: 404 }
      );
    }

    // Convert base64 to buffer
    const base64Data = pdfData.split(',')[1];
    const buffer = Buffer.from(base64Data, 'base64');

    // Extract text from PDF
    const pdfContent = await pdfParse(buffer);
    const pdfText = pdfContent.text;

    if (!pdfText || pdfText.trim().length === 0) {
      return NextResponse.json(
        { message: 'No text found in PDF. Please ensure the PDF contains readable text.' },
        { status: 400 }
      );
    }

    // Extract safety case data using Claude
    const extractedData = await extractSafetyCaseData(pdfText);

    return NextResponse.json({
      success: true,
      extractedData,
    });
  } catch (error: any) {
    console.error('Error extracting PDF:', error);
    return NextResponse.json(
      { message: error.message || 'Failed to extract data from PDF' },
      { status: 500 }
    );
  }
}
