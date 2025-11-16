import { NextRequest, NextResponse } from 'next/server';
import { importLeadsFromCSV } from '@/lib/leadManager';
import { parseCSV } from '@/lib/csvParser';
import { readFile } from 'fs/promises';
import path from 'path';

// POST - Import leads from CSV
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { csvFiles } = body;

    if (!csvFiles || !Array.isArray(csvFiles)) {
      return NextResponse.json(
        { error: 'csvFiles array is required' },
        { status: 400 }
      );
    }

    const allImportedLeads = [];
    const results = [];

    for (const fileName of csvFiles) {
      try {
        // Read CSV file from public directory
        const filePath = path.join(process.cwd(), 'public', fileName);
        const csvContent = await readFile(filePath, 'utf-8');

        // Parse CSV
        const csvData = parseCSV(csvContent);

        // Import leads
        const importedLeads = await importLeadsFromCSV(csvData, fileName);

        allImportedLeads.push(...importedLeads);
        results.push({
          fileName,
          success: true,
          imported: importedLeads.length,
          total: csvData.length,
        });
      } catch (error) {
        console.error(`Error importing ${fileName}:`, error);
        results.push({
          fileName,
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error',
        });
      }
    }

    return NextResponse.json({
      success: true,
      totalImported: allImportedLeads.length,
      results,
      leads: allImportedLeads,
    });
  } catch (error) {
    console.error('Error during import:', error);
    return NextResponse.json(
      { error: 'Failed to import leads' },
      { status: 500 }
    );
  }
}

// GET - Get import status or available CSV files
export async function GET(request: NextRequest) {
  try {
    // Return the list of available CSV files to import
    const csvFiles = [
      '100 leads safety - Sheet1.csv',
      'new_100_leads_safety.csv',
    ];

    return NextResponse.json({
      availableFiles: csvFiles,
      totalFiles: csvFiles.length,
    });
  } catch (error) {
    console.error('Error fetching import info:', error);
    return NextResponse.json(
      { error: 'Failed to fetch import info' },
      { status: 500 }
    );
  }
}
