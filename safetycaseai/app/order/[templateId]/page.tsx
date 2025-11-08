'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import PaymentInstructions from '@/components/PaymentInstructions';
import { Order, TemplateType } from '@/lib/types';

const templateNames: Record<TemplateType, string> = {
  humanoid: 'Humanoid Robot Safety Case',
  amr: 'Autonomous Mobile Robot Safety Case',
  cobot: 'Collaborative Robot Arm Safety Case',
  drone: 'Delivery Drone Safety Case',
  inspection: 'Inspection Robot Safety Case',
};

export default function OrderPage() {
  const params = useParams();
  const templateId = params.templateId as TemplateType;
  const [order, setOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    createOrder();
  }, [templateId]);

  const createOrder = async () => {
    try {
      const response = await fetch('/api/create-order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ templateType: templateId }),
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

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">⏳</div>
          <p className="text-xl text-gray-600">Creating your order...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="card max-w-md text-center">
          <div className="text-6xl mb-4">❌</div>
          <h2 className="text-2xl font-bold mb-2">Error</h2>
          <p className="text-gray-600">{error}</p>
          <a href="/" className="btn-primary mt-6 inline-block">
            Back to Home
          </a>
        </div>
      </div>
    );
  }

  if (!order) {
    return null;
  }

  const templateName = templateNames[templateId] || 'Safety Case';

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
