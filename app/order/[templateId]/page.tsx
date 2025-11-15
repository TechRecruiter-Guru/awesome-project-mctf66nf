'use client';

import { useState } from 'react';
import { useParams } from 'next/navigation';
import PaymentInstructions from '@/components/PaymentInstructions';
import { Order, TemplateType } from '@/lib/types';

const templateNames: Record<TemplateType, string> = {
  humanoid: 'Humanoid Robot Safety Case',
  amr: 'Autonomous Mobile Robot Safety Case',
  cobot: 'Collaborative Robot Arm Safety Case',
  drone: 'Delivery Drone Safety Case',
  inspection: 'Inspection Robot Safety Case',
  construction: 'Construction Robot Safety Case',
  healthcare: 'Healthcare/Medical Robot Safety Case',
  forklift: 'Autonomous Forklift Safety Case',
  service: 'Service Robot Safety Case',
};

export default function OrderPage() {
  const params = useParams();
  const templateId = params.templateId as TemplateType;
  const [order, setOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [email, setEmail] = useState('');
  const [companyName, setCompanyName] = useState('');

  const createOrder = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!email || !companyName) {
      setError('Please fill in all fields');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/create-order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          templateType: templateId,
          email,
          companyName
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setOrder(data.order);
      } else {
        setError(data.message || 'Failed to create order');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const templateName = templateNames[templateId] || 'Safety Case';

  // Show payment instructions after order is created
  if (order) {
    return (
      <div className="min-h-screen py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold mb-4">Complete Your Order</h1>
            <p className="text-gray-600">
              Follow the payment instructions below to proceed with your order
            </p>
          </div>
          <PaymentInstructions order={order} templateName={templateName} />
        </div>
      </div>
    );
  }

  // Show order form before creating order
  return (
    <div className="min-h-screen py-12">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-4">Start Your Order</h1>
          <p className="text-xl text-gray-600 mb-2">{templateName}</p>
          <p className="text-gray-600">
            Enter your details to begin. We'll send your confirmation code to this email after payment.
          </p>
        </div>

        <div className="card max-w-xl mx-auto">
          <form onSubmit={createOrder} className="space-y-6">
            <div>
              <label htmlFor="companyName" className="block text-sm font-medium text-gray-700 mb-2">
                Company Name *
              </label>
              <input
                type="text"
                id="companyName"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Acme Robotics Inc."
                required
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                Email Address *
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="you@company.com"
                required
              />
              <p className="mt-2 text-sm text-gray-500">
                We'll send your confirmation code and website download link to this email.
              </p>
            </div>

            {error && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-600">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary py-4 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <span className="inline-block animate-spin mr-2">⏳</span>
                  Creating Order...
                </>
              ) : (
                'Continue to Payment →'
              )}
            </button>

            <p className="text-sm text-gray-500 text-center">
              Price: $499 • No recurring fees • 48-hour delivery
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}
