import { NextRequest, NextResponse } from 'next/server';
import { extractSafetyCaseData } from '@/lib/claude';
import pdfParse from 'pdf-parse';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { pdfData } = body;

    if (!pdfData) {
      return NextResponse.json(
        { message: 'PDF data is required' },
        { status: 400 }
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

    console.log('PDF text length:', pdfText.length);
    console.log('First 500 chars:', pdfText.substring(0, 500));

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
