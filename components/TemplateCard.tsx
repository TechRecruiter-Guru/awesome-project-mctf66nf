'use client';

import Link from 'next/link';
import { TemplateInfo } from '@/lib/types';

interface TemplateCardProps {
  template: TemplateInfo;
}

export default function TemplateCard({ template }: TemplateCardProps) {
  return (
    <div className="card hover:shadow-xl transition-shadow">
      <div className="text-6xl mb-4">{template.icon}</div>
      <h3 className="text-2xl font-bold mb-2">{template.name}</h3>
      <p className="text-gray-600 mb-4 min-h-[60px]">{template.description}</p>
      <div className="border-t pt-4 mt-4">
        <div className="flex items-baseline justify-between mb-4">
          <span className="text-3xl font-bold text-primary-600">
            ${template.price.toLocaleString()}
          </span>
          <span className="text-gray-500 text-sm">one-time</span>
        </div>
        <Link
          href={`/order/${template.id}`}
          className="block w-full text-center btn-primary"
        >
          Select Template
        </Link>
      </div>
    </div>
  );
}
