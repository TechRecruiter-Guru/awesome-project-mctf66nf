import { kv } from '@vercel/kv';
import { ConfirmationCode } from './types';

const CODES_KEY = 'confirmationCodes';

export async function readCodes(): Promise<Record<string, ConfirmationCode>> {
  try {
    const codes = await kv.get<Record<string, ConfirmationCode>>(CODES_KEY);
    return codes || {};
  } catch (error) {
    console.error('Error reading codes from KV:', error);
    return {};
  }
}

export async function writeCodes(codes: Record<string, ConfirmationCode>): Promise<void> {
  try {
    await kv.set(CODES_KEY, codes);
  } catch (error) {
    console.error('Error writing codes to KV:', error);
    throw error;
  }
}

export async function generateConfirmationCode(): Promise<string> {
  const codes = await readCodes();
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

export async function createConfirmationCode(orderId: string): Promise<ConfirmationCode> {
  const code = await generateConfirmationCode();
  const confirmationCode: ConfirmationCode = {
    code,
    orderId,
    generatedAt: new Date().toISOString(),
    used: false,
    usedAt: null,
  };

  const codes = await readCodes();
  codes[code] = confirmationCode;
  await writeCodes(codes);

  return confirmationCode;
}

export async function getConfirmationCode(code: string): Promise<ConfirmationCode | null> {
  const codes = await readCodes();
  return codes[code] || null;
}

export async function markCodeAsUsed(code: string): Promise<ConfirmationCode | null> {
  const codes = await readCodes();
  const confirmationCode = codes[code];

  if (!confirmationCode) {
    return null;
  }

  confirmationCode.used = true;
  confirmationCode.usedAt = new Date().toISOString();
  codes[code] = confirmationCode;
  await writeCodes(codes);

  return confirmationCode;
}

export async function verifyCode(code: string): Promise<{
  valid: boolean;
  orderId?: string;
  message: string;
}> {
  const confirmationCode = await getConfirmationCode(code);

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
