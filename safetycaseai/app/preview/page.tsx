'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import PreviewEditor from '@/components/PreviewEditor';
import { SafetyCaseData } from '@/lib/types';

export default function PreviewPage() {
  const [data, setData] = useState<SafetyCaseData | null>(null);
  const [templateHtml, setTemplateHtml] = useState('');
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const extractedData = sessionStorage.getItem('extractedData');
    const orderId = sessionStorage.getItem('orderId');

    if (!extractedData || !orderId) {
      router.push('/upload');
      return;
    }

    setData(JSON.parse(extractedData));
    generatePreview(JSON.parse(extractedData), orderId);
  }, []);

  const generatePreview = async (safetyCaseData: SafetyCaseData, orderId: string) => {
    try {
      const response = await fetch('/api/populate-template', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          orderId,
          data: safetyCaseData,
        }),
      });

      const result = await response.json();

      if (response.ok) {
        setTemplateHtml(result.html);
      }
    } catch (err) {
      console.error('Error generating preview:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDataChange = async (updatedData: SafetyCaseData) => {
    setData(updatedData);
    sessionStorage.setItem('extractedData', JSON.stringify(updatedData));

    const orderId = sessionStorage.getItem('orderId');
    if (orderId) {
      await generatePreview(updatedData, orderId);
    }
  };

  const handleDownload = async () => {
    if (!data) return;

    setDownloading(true);

    try {
      const orderId = sessionStorage.getItem('orderId');
      const response = await fetch('/api/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          orderId,
          data,
        }),
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `safety-case-${data.companyName.toLowerCase().replace(/\s+/g, '-')}-${new Date().toISOString().slice(0, 10)}.html`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (err) {
      console.error('Error downloading:', err);
      alert('Failed to download. Please try again.');
    } finally {
      setDownloading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">⏳</div>
          <p className="text-xl text-gray-600">Generating preview...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return null;
  }

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold mb-2">Preview & Edit</h1>
            <p className="text-gray-600">
              Review and edit your safety case data, then download your website
            </p>
          </div>
          <button
            onClick={handleDownload}
            disabled={downloading}
            className="btn-primary flex items-center gap-2"
          >
            <span>{downloading ? 'Downloading...' : 'Download HTML'}</span>
            <span>📥</span>
          </button>
        </div>

        <PreviewEditor
          initialData={data}
          templateHtml={templateHtml}
          onDataChange={handleDataChange}
        />

        <div className="mt-8 bg-green-50 border border-green-200 p-6 rounded-lg">
          <h3 className="font-bold text-lg mb-2">Ready to Download?</h3>
          <p className="text-gray-700 mb-4">
            Your safety case website will be downloaded as a single, self-contained
            HTML file. You can upload it to any web hosting service or share it
            directly.
          </p>
          <button
            onClick={handleDownload}
            disabled={downloading}
            className="btn-primary"
          >
            {downloading ? 'Downloading...' : 'Download Complete Website'}
          </button>
        </div>
      </div>
    </div>
  );
}
