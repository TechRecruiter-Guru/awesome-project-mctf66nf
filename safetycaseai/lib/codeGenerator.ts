import fs from 'fs';
import path from 'path';
import { ConfirmationCode } from './types';

const CODES_FILE = path.join(process.cwd(), 'data', 'confirmationCodes.json');

export function readCodes(): Record<string, ConfirmationCode> {
  try {
    const data = fs.readFileSync(CODES_FILE, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    return {};
  }
}

export function writeCodes(codes: Record<string, ConfirmationCode>): void {
  fs.writeFileSync(CODES_FILE, JSON.stringify(codes, null, 2), 'utf-8');
}

export function generateConfirmationCode(): string {
  const codes = readCodes();
  const existingCodes = Object.keys(codes);

  // Extract numbers from existing codes
  const numbers = existingCodes
    .map(code => {
      const match = code.match(/UNLOCK-(\d+)/);
      return match ? parseInt(match[1], 10) : 0;
    })
    .filter(num => num > 0);

  const nextNumber = numbers.length > 0 ? Math.max(...numbers) + 1 : 1;
  return `UNLOCK-${nextNumber.toString().padStart(3, '0')}`;
}

export function createConfirmationCode(orderId: string): ConfirmationCode {
  const code = generateConfirmationCode();
  const confirmationCode: ConfirmationCode = {
    code,
    orderId,
    generatedAt: new Date().toISOString(),
    used: false,
    usedAt: null,
  };

  const codes = readCodes();
  codes[code] = confirmationCode;
  writeCodes(codes);

  return confirmationCode;
}

export function getConfirmationCode(code: string): ConfirmationCode | null {
  const codes = readCodes();
  return codes[code] || null;
}

export function markCodeAsUsed(code: string): ConfirmationCode | null {
  const codes = readCodes();
  const confirmationCode = codes[code];

  if (!confirmationCode) {
    return null;
  }

  confirmationCode.used = true;
  confirmationCode.usedAt = new Date().toISOString();
  codes[code] = confirmationCode;
  writeCodes(codes);

  return confirmationCode;
}

export function verifyCode(code: string): {
  valid: boolean;
  orderId?: string;
  message: string;
} {
  const confirmationCode = getConfirmationCode(code);

  if (!confirmationCode) {
    return {
      valid: false,
      message: 'Invalid confirmation code. Please check and try again.',
    };
  }

  if (confirmationCode.used) {
    return {
      valid: false,
      message: 'This confirmation code has already been used.',
    };
  }

  return {
    valid: true,
    orderId: confirmationCode.orderId,
    message: 'Confirmation code verified successfully.',
  };
}
