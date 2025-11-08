'use client';

import { Order } from '@/lib/types';

interface PaymentInstructionsProps {
  order: Order;
  templateName: string;
}

export default function PaymentInstructions({
  order,
  templateName,
}: PaymentInstructionsProps) {
  return (
    <div className="card max-w-3xl mx-auto">
      <div className="border-b pb-4 mb-6">
        <h2 className="text-2xl font-bold mb-2">Order Confirmation</h2>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-600">Order ID:</span>
            <span className="font-mono font-bold ml-2">{order.orderId}</span>
          </div>
          <div>
            <span className="text-gray-600">Template:</span>
            <span className="font-semibold ml-2">{templateName}</span>
          </div>
          <div>
            <span className="text-gray-600">Amount:</span>
            <span className="font-bold text-2xl ml-2 text-primary-600">
              $2,000
            </span>
          </div>
        </div>
      </div>

      <div className="space-y-6">
        <div>
          <h3 className="text-xl font-bold mb-4">Payment Options</h3>
          <p className="text-gray-600 mb-4">
            Choose one of the following payment methods. Make sure to include your
            Order ID in the payment note.
          </p>
        </div>

        <div className="bg-blue-50 p-6 rounded-lg">
          <div className="flex items-start">
            <span className="text-3xl mr-4">💳</span>
            <div className="flex-1">
              <h4 className="font-bold text-lg mb-2">Option 1: PayPal</h4>
              <div className="space-y-2">
                <div>
                  <span className="text-gray-600">Send to:</span>
                  <span className="font-mono font-bold ml-2">
                    cgtpa.jp@gmail.com
                  </span>
                </div>
                <div>
                  <span className="text-gray-600">Amount:</span>
                  <span className="font-bold ml-2">$2,000 USD</span>
                </div>
                <div>
                  <span className="text-gray-600">Note:</span>
                  <span className="font-mono font-bold ml-2">
                    Order #{order.orderId}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-purple-50 p-6 rounded-lg">
          <div className="flex items-start">
            <span className="text-3xl mr-4">📱</span>
            <div className="flex-1">
              <h4 className="font-bold text-lg mb-2">Option 2: Venmo</h4>
              <div className="space-y-2">
                <div>
                  <span className="text-gray-600">Send to:</span>
                  <span className="font-mono font-bold ml-2">
                    @mastertechnicalrecruiting
                  </span>
                </div>
                <div>
                  <span className="text-gray-600">Amount:</span>
                  <span className="font-bold ml-2">$2,000 USD</span>
                </div>
                <div>
                  <span className="text-gray-600">Note:</span>
                  <span className="font-mono font-bold ml-2">
                    Order #{order.orderId}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t pt-6">
          <h4 className="font-bold text-lg mb-3">After Payment:</h4>
          <ol className="list-decimal list-inside space-y-2 text-gray-700">
            <li>
              Email your payment receipt to{' '}
              <a
                href="mailto:contact@safetycaseai.com"
                className="text-primary-600 font-semibold hover:underline"
              >
                contact@safetycaseai.com
              </a>
            </li>
            <li>
              Include your Order ID:{' '}
              <span className="font-mono font-bold">{order.orderId}</span> in the
              email subject
            </li>
            <li>
              You will receive a confirmation code via email within 1 hour during
              business hours
            </li>
            <li>
              Use the confirmation code on the{' '}
              <a href="/upload" className="text-primary-600 font-semibold hover:underline">
                Upload page
              </a>{' '}
              to proceed
            </li>
          </ol>
        </div>

        <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
          <p className="text-sm text-gray-700">
            <strong>Important:</strong> Keep your Order ID safe. You will need it to
            track your order status and access your confirmation code.
          </p>
        </div>
      </div>
    </div>
  );
}
