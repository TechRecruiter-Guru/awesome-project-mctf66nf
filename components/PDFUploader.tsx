'use client';

import { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';

export default function PDFUploader({ orderId }: { orderId: string }) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState('');
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const router = useRouter();

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    setError('');

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type === 'application/pdf') {
        setFile(droppedFile);
      } else {
        setError('Please upload a PDF file');
      }
    }
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setError('');
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (selectedFile.type === 'application/pdf') {
        setFile(selectedFile);
      } else {
        setError('Please upload a PDF file');
      }
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setError('');
    setProgress('Uploading PDF...');

    try {
      // Convert file to base64
      const reader = new FileReader();
      reader.onload = async () => {
        const base64 = reader.result as string;

        setProgress('Extracting data with Claude AI... This takes 30-60 seconds');

        const response = await fetch('/api/extract-pdf', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            pdfData: base64,
            orderId,
          }),
        });

        const data = await response.json();

        if (response.ok) {
          // Store extracted data in session storage
          sessionStorage.setItem('extractedData', JSON.stringify(data.extractedData));
          sessionStorage.setItem('orderId', orderId);

          setProgress('Data extracted! Redirecting to preview...');

          setTimeout(() => {
            router.push('/preview');
          }, 1000);
        } else {
          setError(data.message || 'Failed to extract data from PDF');
        }
      };

      reader.onerror = () => {
        setError('Failed to read PDF file');
        setUploading(false);
      };

      reader.readAsDataURL(file);
    } catch (err) {
      setError('An error occurred during upload. Please try again.');
      setUploading(false);
      setProgress('');
    }
  };

  return (
    <div className="card max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Upload Your Safety Case PDF</h2>
      <p className="text-gray-600 mb-6">
        Upload your safety case document and our AI will extract all relevant data to
        populate your template.
      </p>

      <div
        className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
          dragActive
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 bg-gray-50'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {!file ? (
          <>
            <div className="text-6xl mb-4">📄</div>
            <p className="text-lg mb-2">
              Drag and drop your PDF here, or click to browse
            </p>
            <input
              type="file"
              id="pdf-upload"
              accept="application/pdf"
              onChange={handleFileChange}
              className="hidden"
            />
            <label
              htmlFor="pdf-upload"
              className="inline-block mt-4 px-6 py-3 bg-primary-600 text-white rounded-lg cursor-pointer hover:bg-primary-700 transition-colors"
            >
              Choose PDF File
            </label>
          </>
        ) : (
          <div>
            <div className="text-6xl mb-4">✅</div>
            <p className="text-lg font-semibold mb-2">{file.name}</p>
            <p className="text-gray-600 mb-4">
              {(file.size / 1024 / 1024).toFixed(2)} MB
            </p>
            <button
              onClick={() => setFile(null)}
              className="text-red-600 hover:text-red-700 font-semibold"
            >
              Remove
            </button>
          </div>
        )}
      </div>

      {error && (
        <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {progress && (
        <div className="mt-4 bg-blue-50 border border-blue-200 text-blue-700 px-4 py-3 rounded">
          <div className="flex items-center">
            <svg
              className="animate-spin h-5 w-5 mr-3"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            {progress}
          </div>
        </div>
      )}

      <button
        onClick={handleUpload}
        disabled={!file || uploading}
        className="w-full mt-6 btn-primary"
      >
        {uploading ? 'Processing...' : 'Upload & Extract Data'}
      </button>

      <div className="mt-6 pt-6 border-t">
        <p className="text-sm text-gray-600">
          <strong>Note:</strong> The AI extraction process typically takes 30-60
          seconds. Please be patient while we analyze your document.
        </p>
      </div>
    </div>
  );
}
