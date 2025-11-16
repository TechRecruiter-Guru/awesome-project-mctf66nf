'use client';

import { useEffect, useState } from 'react';
import { Order, OrderStatus } from '@/lib/types';

interface Lead {
  person: string;
  company: string;
  email: string;
  website: string;
  whySelected: string;
  status?: string;
  notes?: string;
}

export default function AdminPage() {
  const [authenticated, setAuthenticated] = useState(false);
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(false);
  const [filterStatus, setFilterStatus] = useState<OrderStatus | 'all'>('all');
  const [generatingCode, setGeneratingCode] = useState<string | null>(null);
  const [generatedCode, setGeneratedCode] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'orders' | 'leads'>('orders');
  const [leads, setLeads] = useState<Lead[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [leadStatusFilter, setLeadStatusFilter] = useState<string>('all');

  useEffect(() => {
    const auth = sessionStorage.getItem('adminAuthenticated');
    if (auth === 'true') {
      setAuthenticated(true);
      fetchOrders();
      fetchLeads();
    }
  }, []);

  const fetchLeads = async () => {
    try {
      const [response1, response2] = await Promise.all([
        fetch('/100 leads safety - Sheet1.csv'),
        fetch('/new_100_leads_safety.csv')
      ]);

      const [csv1, csv2] = await Promise.all([
        response1.text(),
        response2.text()
      ]);

      const parseCSV = (csvText: string): Lead[] => {
        const lines = csvText.split('\n').filter(line => line.trim());
        const headers = lines[0].split(',');

        return lines.slice(1).map(line => {
          const values = line.match(/(".*?"|[^,]+)(?=\s*,|\s*$)/g) || [];
          const cleanedValues = values.map(v => v.replace(/^"|"$/g, '').trim());

          return {
            person: cleanedValues[0] || '',
            company: cleanedValues[1] || '',
            email: cleanedValues[2] || '',
            website: cleanedValues[3] || '',
            whySelected: cleanedValues[4] || '',
            status: 'Not Contacted',
            notes: ''
          };
        });
      };

      const allLeads = [...parseCSV(csv1), ...parseCSV(csv2)];
      setLeads(allLeads);
    } catch (error) {
      console.error('Error fetching leads:', error);
    }
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('/api/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        sessionStorage.setItem('adminAuthenticated', 'true');
        setAuthenticated(true);
        fetchOrders();
      } else {
        setError('Invalid password');
      }
    } catch (err) {
      setError('Authentication failed');
    }
  };

  const fetchOrders = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/admin/get-orders');
      const data = await response.json();

      if (response.ok) {
        setOrders(data.orders);
      }
    } catch (err) {
      console.error('Error fetching orders:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateCode = async (orderId: string) => {
    setGeneratingCode(orderId);
    setGeneratedCode(null);

    try {
      const response = await fetch('/api/admin/activate-order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ orderId }),
      });

      const data = await response.json();

      if (response.ok) {
        setGeneratedCode(data.confirmationCode);
        fetchOrders(); // Refresh orders
      } else {
        alert(data.message || 'Failed to generate code');
      }
    } catch (err) {
      alert('Error generating confirmation code');
    } finally {
      setGeneratingCode(null);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  const handleLogout = () => {
    sessionStorage.removeItem('adminAuthenticated');
    setAuthenticated(false);
    setPassword('');
  };

  const filteredOrders = filterStatus === 'all'
    ? orders
    : orders.filter(order => order.status === filterStatus);

  const filteredLeads = leads.filter(lead => {
    const matchesSearch =
      lead.person.toLowerCase().includes(searchTerm.toLowerCase()) ||
      lead.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
      lead.email.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesStatus = leadStatusFilter === 'all' || lead.status === leadStatusFilter;

    return matchesSearch && matchesStatus;
  });

  const updateLeadStatus = (email: string, newStatus: string) => {
    setLeads(prev => prev.map(lead =>
      lead.email === email ? { ...lead, status: newStatus } : lead
    ));
  };

  const getStatusBadge = (status: OrderStatus) => {
    const colors = {
      pending_payment: 'bg-yellow-100 text-yellow-800',
      code_generated: 'bg-blue-100 text-blue-800',
      pdf_uploaded: 'bg-purple-100 text-purple-800',
      completed: 'bg-green-100 text-green-800',
    };

    return (
      <span className={`px-3 py-1 rounded-full text-sm font-semibold ${colors[status]}`}>
        {status.replace('_', ' ').toUpperCase()}
      </span>
    );
  };

  if (!authenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="card max-w-md w-full">
          <h1 className="text-3xl font-bold mb-6 text-center">Admin Login</h1>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label htmlFor="password" className="label">
                Password
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                className="input-field"
                placeholder="Enter admin password"
                required
              />
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            <button type="submit" className="w-full btn-primary">
              Login
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-12 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold mb-2">Admin Dashboard</h1>
            <p className="text-gray-600">Manage orders and lead outreach</p>
          </div>
          <button
            onClick={handleLogout}
            className="btn-secondary"
          >
            Logout
          </button>
        </div>

        {/* Tabs */}
        <div className="flex gap-4 mb-8 border-b border-gray-200">
          <button
            onClick={() => setActiveTab('orders')}
            className={`px-6 py-3 font-semibold transition-colors ${
              activeTab === 'orders'
                ? 'border-b-4 border-primary-600 text-primary-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            📦 Orders ({orders.length})
          </button>
          <button
            onClick={() => setActiveTab('leads')}
            className={`px-6 py-3 font-semibold transition-colors ${
              activeTab === 'leads'
                ? 'border-b-4 border-primary-600 text-primary-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            👥 Leads CRM ({leads.length})
          </button>
        </div>

        {generatedCode && activeTab === 'orders' && (
          <div className="card mb-8 bg-green-50 border-2 border-green-500">
            <h3 className="text-xl font-bold mb-4 text-green-800">
              ✅ Confirmation Code Generated
            </h3>
            <div className="flex items-center gap-4">
              <span className="text-3xl font-mono font-bold text-green-900">
                {generatedCode}
              </span>
              <button
                onClick={() => copyToClipboard(generatedCode)}
                className="btn-primary"
              >
                Copy Code
              </button>
            </div>
            <p className="mt-4 text-green-800">
              Send this code to the customer via email to SafetyCaseAI@physicalAIPros.com
            </p>
          </div>
        )}

        {/* ORDERS TAB */}
        {activeTab === 'orders' && (
          <>
        <div className="card mb-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">Orders</h2>
            <div className="flex gap-2">
              <button
                onClick={() => setFilterStatus('all')}
                className={`px-4 py-2 rounded ${filterStatus === 'all' ? 'bg-primary-600 text-white' : 'bg-gray-200'}`}
              >
                All ({orders.length})
              </button>
              <button
                onClick={() => setFilterStatus('pending_payment')}
                className={`px-4 py-2 rounded ${filterStatus === 'pending_payment' ? 'bg-primary-600 text-white' : 'bg-gray-200'}`}
              >
                Pending
              </button>
              <button
                onClick={() => setFilterStatus('code_generated')}
                className={`px-4 py-2 rounded ${filterStatus === 'code_generated' ? 'bg-primary-600 text-white' : 'bg-gray-200'}`}
              >
                Active
              </button>
              <button
                onClick={() => setFilterStatus('completed')}
                className={`px-4 py-2 rounded ${filterStatus === 'completed' ? 'bg-primary-600 text-white' : 'bg-gray-200'}`}
              >
                Completed
              </button>
            </div>
          </div>

          <button
            onClick={fetchOrders}
            disabled={loading}
            className="btn-secondary mb-4"
          >
            {loading ? 'Refreshing...' : 'Refresh Orders'}
          </button>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Order ID</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Company</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Email</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Template</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Created</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Status</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Code</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {filteredOrders.length === 0 ? (
                  <tr>
                    <td colSpan={8} className="px-4 py-8 text-center text-gray-500">
                      No orders found
                    </td>
                  </tr>
                ) : (
                  filteredOrders.map(order => (
                    <tr key={order.orderId} className="hover:bg-gray-50">
                      <td className="px-4 py-3">
                        <span className="font-mono text-sm">{order.orderId}</span>
                      </td>
                      <td className="px-4 py-3">
                        <span className="font-semibold">{order.companyName || '—'}</span>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600">
                        {order.email || '—'}
                      </td>
                      <td className="px-4 py-3 capitalize">{order.templateType}</td>
                      <td className="px-4 py-3 text-sm">
                        {new Date(order.createdAt).toLocaleDateString()}
                      </td>
                      <td className="px-4 py-3">{getStatusBadge(order.status)}</td>
                      <td className="px-4 py-3">
                        {order.confirmationCode ? (
                          <span className="font-mono text-sm font-bold">
                            {order.confirmationCode}
                          </span>
                        ) : (
                          <span className="text-gray-400">—</span>
                        )}
                      </td>
                      <td className="px-4 py-3">
                        {order.status === 'pending_payment' && (
                          <button
                            onClick={() => handleGenerateCode(order.orderId)}
                            disabled={generatingCode === order.orderId}
                            className="bg-primary-600 text-white px-4 py-2 rounded text-sm hover:bg-primary-700 disabled:opacity-50"
                          >
                            {generatingCode === order.orderId
                              ? 'Generating...'
                              : 'Generate Code'}
                          </button>
                        )}
                        {order.confirmationCode && (
                          <button
                            onClick={() => copyToClipboard(order.confirmationCode!)}
                            className="bg-gray-600 text-white px-4 py-2 rounded text-sm hover:bg-gray-700"
                          >
                            Copy Code
                          </button>
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          <div className="card bg-yellow-50">
            <h3 className="font-bold text-lg mb-2">Pending Payment</h3>
            <p className="text-4xl font-bold text-yellow-600">
              {orders.filter(o => o.status === 'pending_payment').length}
            </p>
          </div>
          <div className="card bg-blue-50">
            <h3 className="font-bold text-lg mb-2">Active Orders</h3>
            <p className="text-4xl font-bold text-blue-600">
              {orders.filter(o => o.status === 'code_generated' || o.status === 'pdf_uploaded').length}
            </p>
          </div>
          <div className="card bg-green-50">
            <h3 className="font-bold text-lg mb-2">Completed</h3>
            <p className="text-4xl font-bold text-green-600">
              {orders.filter(o => o.status === 'completed').length}
            </p>
          </div>
        </div>
        </>
        )}

        {/* LEADS CRM TAB */}
        {activeTab === 'leads' && (
          <>
        <div className="card mb-8">
          <div className="mb-6">
            <h2 className="text-2xl font-bold mb-4">Lead Management CRM</h2>

            {/* Search and Filters */}
            <div className="flex gap-4 mb-6">
              <input
                type="text"
                placeholder="🔍 Search by name, company, or email..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
              <select
                value={leadStatusFilter}
                onChange={(e) => setLeadStatusFilter(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              >
                <option value="all">All Status</option>
                <option value="Not Contacted">Not Contacted</option>
                <option value="Contacted">Contacted</option>
                <option value="Follow Up">Follow Up</option>
                <option value="Qualified">Qualified</option>
                <option value="Closed">Closed</option>
              </select>
            </div>
          </div>

          {/* Leads Table */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Person</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Company</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Email</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Website</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Why Selected</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Status</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {filteredLeads.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="px-4 py-8 text-center text-gray-500">
                      No leads found
                    </td>
                  </tr>
                ) : (
                  filteredLeads.map((lead, idx) => (
                    <tr key={idx} className="hover:bg-gray-50">
                      <td className="px-4 py-3">
                        <span className="font-semibold">{lead.person}</span>
                      </td>
                      <td className="px-4 py-3">
                        <span className="text-sm">{lead.company}</span>
                      </td>
                      <td className="px-4 py-3">
                        <a href={`mailto:${lead.email}`} className="text-primary-600 hover:underline text-sm">
                          {lead.email}
                        </a>
                      </td>
                      <td className="px-4 py-3">
                        <a href={lead.website} target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline text-sm">
                          {lead.website.replace('https://', '')}
                        </a>
                      </td>
                      <td className="px-4 py-3 max-w-md">
                        <p className="text-sm text-gray-600 line-clamp-2">{lead.whySelected}</p>
                      </td>
                      <td className="px-4 py-3">
                        <select
                          value={lead.status}
                          onChange={(e) => updateLeadStatus(lead.email, e.target.value)}
                          className="text-sm px-3 py-1 rounded-full border border-gray-300 focus:ring-2 focus:ring-primary-500"
                        >
                          <option value="Not Contacted">Not Contacted</option>
                          <option value="Contacted">Contacted</option>
                          <option value="Follow Up">Follow Up</option>
                          <option value="Qualified">Qualified</option>
                          <option value="Closed">Closed</option>
                        </select>
                      </td>
                      <td className="px-4 py-3">
                        <a
                          href={`mailto:${lead.email}?subject=Compliance%20%2B%20recruiting%20bundle%20for%20${lead.company}?&body=Hi%20${lead.person.split(' ')[0]},%0A%0ASaw%20${lead.company}%20...`}
                          className="bg-primary-600 text-white px-4 py-2 rounded text-sm hover:bg-primary-700"
                        >
                          📧 Email
                        </a>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Lead Stats */}
        <div className="grid md:grid-cols-5 gap-6">
          <div className="card bg-gray-50">
            <h3 className="font-bold text-lg mb-2">Total Leads</h3>
            <p className="text-4xl font-bold text-gray-600">{leads.length}</p>
          </div>
          <div className="card bg-yellow-50">
            <h3 className="font-bold text-lg mb-2">Not Contacted</h3>
            <p className="text-4xl font-bold text-yellow-600">
              {leads.filter(l => l.status === 'Not Contacted').length}
            </p>
          </div>
          <div className="card bg-blue-50">
            <h3 className="font-bold text-lg mb-2">Contacted</h3>
            <p className="text-4xl font-bold text-blue-600">
              {leads.filter(l => l.status === 'Contacted').length}
            </p>
          </div>
          <div className="card bg-purple-50">
            <h3 className="font-bold text-lg mb-2">Qualified</h3>
            <p className="text-4xl font-bold text-purple-600">
              {leads.filter(l => l.status === 'Qualified').length}
            </p>
          </div>
          <div className="card bg-green-50">
            <h3 className="font-bold text-lg mb-2">Closed</h3>
            <p className="text-4xl font-bold text-green-600">
              {leads.filter(l => l.status === 'Closed').length}
            </p>
          </div>
        </div>
        </>
        )}
      </div>
    </div>
  );
}
