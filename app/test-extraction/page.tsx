'use client';

import { useState } from 'react';

export default function TestExtractionPage() {
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [extractedData, setExtractedData] = useState<any>(null);
  const [error, setError] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setPdfFile(e.target.files[0]);
      setError('');
      setExtractedData(null);
    }
  };

  const handleExtract = async () => {
    if (!pdfFile) {
      setError('Please select a PDF file');
      return;
    }

    setLoading(true);
    setError('');
    setExtractedData(null);

    try {
      // Convert PDF to base64
      const reader = new FileReader();
      reader.onload = async (e) => {
        const base64Data = e.target?.result as string;

        // Call extraction API
        const response = await fetch('/api/test-extract', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ pdfData: base64Data }),
        });

        const data = await response.json();

        if (response.ok) {
          setExtractedData(data.extractedData);
        } else {
          setError(data.message || 'Extraction failed');
        }
        setLoading(false);
      };

      reader.onerror = () => {
        setError('Failed to read PDF file');
        setLoading(false);
      };

      reader.readAsDataURL(pdfFile);
    } catch (err: any) {
      setError(err.message || 'An error occurred');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-12 bg-gray-50">
      <div className="max-w-4xl mx-auto px-4">
        <div className="card mb-8">
          <h1 className="text-3xl font-bold mb-4">🧪 Test PDF Extraction</h1>
          <p className="text-gray-600 mb-6">
            Upload a safety case PDF to test AI extraction (no order required)
          </p>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select PDF File
              </label>
              <input
                type="file"
                accept="application/pdf"
                onChange={handleFileChange}
                className="block w-full text-sm text-gray-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-full file:border-0
                  file:text-sm file:font-semibold
                  file:bg-blue-50 file:text-blue-700
                  hover:file:bg-blue-100"
              />
            </div>

            {pdfFile && (
              <div className="text-sm text-gray-600">
                Selected: {pdfFile.name} ({Math.round(pdfFile.size / 1024)} KB)
              </div>
            )}

            <button
              onClick={handleExtract}
              disabled={loading || !pdfFile}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <span className="inline-block animate-spin mr-2">⏳</span>
                  Extracting safety data...
                </>
              ) : (
                'Extract Safety Case Data'
              )}
            </button>

            {error && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-600">{error}</p>
              </div>
            )}
          </div>
        </div>

        {extractedData && (
          <div className="card">
            <h2 className="text-2xl font-bold mb-4">✅ Extracted Data</h2>

            <div className="space-y-6">
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Company Name</label>
                  <p className="mt-1 text-lg font-semibold">{extractedData.companyName || 'N/A'}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Robot Model</label>
                  <p className="mt-1 text-lg font-semibold">{extractedData.robotModel || 'N/A'}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">SIL Rating</label>
                  <p className="mt-1 text-lg font-semibold">{extractedData.silRating || 'N/A'}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Certification Body</label>
                  <p className="mt-1 text-lg font-semibold">{extractedData.certificationBody || 'N/A'}</p>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Compliance Standards</label>
                <div className="flex flex-wrap gap-2">
                  {extractedData.complianceStandards?.map((std: string, i: number) => (
                    <span key={i} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                      {std}
                    </span>
                  ))}
                </div>
              </div>

              {extractedData.riskAssessments && extractedData.riskAssessments.length > 0 && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Risk Assessments ({extractedData.riskAssessments.length})
                  </label>
                  <div className="space-y-2">
                    {extractedData.riskAssessments.map((risk: any, i: number) => (
                      <div key={i} className="p-3 bg-gray-50 rounded-lg border border-gray-200">
                        <p className="font-medium">{risk.scenario}</p>
                        <div className="mt-1 text-sm text-gray-600">
                          Severity: {risk.severity} | Likelihood: {risk.likelihood} | Risk: {risk.riskLevel}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Full Extracted Data (JSON)</label>
                <pre className="p-4 bg-gray-900 text-green-400 rounded-lg overflow-auto text-xs">
                  {JSON.stringify(extractedData, null, 2)}
                </pre>
              </div>
            </div>
          </div>
        )}

        <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h3 className="font-bold text-blue-900 mb-2">📄 Need a Test PDF?</h3>
          <p className="text-blue-800 text-sm mb-2">
            Use the sample safety case document from the repository:
          </p>
          <a
            href="https://github.com/TechRecruiter-Guru/awesome-project-mctf66nf/blob/claude/safetycaseai-deploy-011CUvaPTZHjAztWizeDSpUV/SAMPLE_SAFETY_CASE_FOR_TESTING.md"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 underline text-sm"
          >
            View SAMPLE_SAFETY_CASE_FOR_TESTING.md →
          </a>
          <p className="text-blue-800 text-sm mt-2">
            Copy the content, paste into Google Docs or Word, and export as PDF.
          </p>
        </div>
      </div>
    </div>
  );
}
