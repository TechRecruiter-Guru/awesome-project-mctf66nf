'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function ConfirmationCodeInput() {
  const [code, setCode] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('/api/verify-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: code.toUpperCase() }),
      });

      const data = await response.json();

      if (response.ok && data.valid) {
        // Store the order ID in session storage
        sessionStorage.setItem('orderId', data.orderId);
        sessionStorage.setItem('confirmationCode', code.toUpperCase());
        // Redirect to upload interface
        router.push(`/upload?verified=true`);
      } else {
        setError(data.message || 'Invalid confirmation code');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card max-w-md mx-auto">
      <h2 className="text-2xl font-bold mb-4 text-center">
        Enter Confirmation Code
      </h2>
      <p className="text-gray-600 mb-6 text-center">
        Received your confirmation code via email? Enter it below to upload your
        PDF.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="code" className="label">
            Confirmation Code
          </label>
          <input
            type="text"
            id="code"
            value={code}
            onChange={e => setCode(e.target.value.toUpperCase())}
            placeholder="UNLOCK-XXX"
            className="input-field text-center text-lg font-mono tracking-wider"
            required
            maxLength={10}
          />
          <p className="text-sm text-gray-500 mt-1">
            Format: UNLOCK-XXX (e.g., UNLOCK-001)
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading || code.length < 6}
          className="w-full btn-primary"
        >
          {loading ? 'Verifying...' : 'Verify Code & Continue'}
        </button>
      </form>

      <div className="mt-6 pt-6 border-t">
        <p className="text-sm text-gray-600 text-center">
          Don't have a code yet?
        </p>
        <ul className="mt-3 space-y-2 text-sm text-gray-700">
          <li className="flex items-start">
            <span className="mr-2">•</span>
            <span>Check your email (including spam folder)</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">•</span>
            <span>Allow up to 1 hour for manual verification</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">•</span>
            <span>
              Email{' '}
              <a
                href="mailto:SafetyCaseAI@physicalAIPros.com"
                className="text-primary-600 hover:underline"
              >
                SafetyCaseAI@physicalAIPros.com
              </a>{' '}
              if delayed
            </span>
          </li>
        </ul>
      </div>
    </div>
  );
}
