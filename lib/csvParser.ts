/**
 * Simple CSV parser with zero dependencies
 * Parses CSV content and returns array of objects
 */

export interface CSVRow {
  Person?: string;
  Company?: string;
  Email?: string;
  Website?: string;
  'Why Selected'?: string;
  [key: string]: string | undefined;
}

export function parseCSV(csvContent: string): CSVRow[] {
  const lines = csvContent.split('\n').filter(line => line.trim());

  if (lines.length === 0) {
    return [];
  }

  // Parse header row
  const headers = parseCSVLine(lines[0]);

  // Parse data rows
  const rows: CSVRow[] = [];
  for (let i = 1; i < lines.length; i++) {
    const values = parseCSVLine(lines[i]);

    if (values.length === 0) continue;

    const row: CSVRow = {};
    headers.forEach((header, index) => {
      row[header] = values[index] || '';
    });

    // Only add row if it has at least an email or person name
    if (row.Email || row.Person) {
      rows.push(row);
    }
  }

  return rows;
}

/**
 * Parse a single CSV line handling quoted values and commas within quotes
 */
function parseCSVLine(line: string): string[] {
  const result: string[] = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    const nextChar = line[i + 1];

    if (char === '"') {
      if (inQuotes && nextChar === '"') {
        // Escaped quote
        current += '"';
        i++; // Skip next quote
      } else {
        // Toggle quote state
        inQuotes = !inQuotes;
      }
    } else if (char === ',' && !inQuotes) {
      // End of field
      result.push(current.trim());
      current = '';
    } else {
      current += char;
    }
  }

  // Add last field
  result.push(current.trim());

  return result;
}

/**
 * Convert array of objects back to CSV string
 */
export function toCSV(data: CSVRow[]): string {
  if (data.length === 0) return '';

  // Get headers from first object
  const headers = Object.keys(data[0]);

  // Create header row
  const headerRow = headers.map(escapeCSVField).join(',');

  // Create data rows
  const dataRows = data.map(row =>
    headers.map(header => escapeCSVField(row[header] || '')).join(',')
  );

  return [headerRow, ...dataRows].join('\n');
}

/**
 * Escape a CSV field value
 */
function escapeCSVField(value: string): string {
  // If value contains comma, quote, or newline, wrap in quotes
  if (value.includes(',') || value.includes('"') || value.includes('\n')) {
    // Escape quotes by doubling them
    return `"${value.replace(/"/g, '""')}"`;
  }
  return value;
}

/**
 * Read and parse CSV from a file URL (for public files)
 */
export async function fetchAndParseCSV(url: string): Promise<CSVRow[]> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch CSV: ${response.statusText}`);
    }
    const csvContent = await response.text();
    return parseCSV(csvContent);
  } catch (error) {
    console.error('Error fetching and parsing CSV:', error);
    throw error;
  }
}
