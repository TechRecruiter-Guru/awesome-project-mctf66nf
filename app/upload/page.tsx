'use client';

import { Suspense, useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import ConfirmationCodeInput from '@/components/ConfirmationCodeInput';
import PDFUploader from '@/components/PDFUploader';

function UploadPageContent() {
  const searchParams = useSearchParams();
  const [verified, setVerified] = useState(false);
  const [orderId, setOrderId] = useState('');

  useEffect(() => {
    // Check if user is verified (coming from confirmation code verification)
    const verifiedParam = searchParams.get('verified');
    const storedOrderId = sessionStorage.getItem('orderId');

    if (verifiedParam === 'true' && storedOrderId) {
      setVerified(true);
      setOrderId(storedOrderId);
    }
  }, [searchParams]);

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">
            {verified ? 'Upload Your PDF' : 'Verify Your Code'}
          </h1>
          <p className="text-gray-600">
            {verified
              ? 'Upload your safety case PDF to extract data and populate your template'
              : 'Enter your confirmation code to proceed with PDF upload'}
          </p>
        </div>

        {verified ? (
          <PDFUploader orderId={orderId} />
        ) : (
          <ConfirmationCodeInput />
        )}
      </div>
    </div>
  );
}

export default function UploadPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">⏳</div>
          <p className="text-xl text-gray-600">Loading...</p>
        </div>
      </div>
    }>
      <UploadPageContent />
    </Suspense>
  );
}
