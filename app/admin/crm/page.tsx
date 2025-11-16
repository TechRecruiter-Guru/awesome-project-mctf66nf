'use client';

import { useState, useEffect } from 'react';
import { Lead, Activity, LeadStatus, CRMStats } from '@/lib/types';

export default function CRMDashboard() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [stats, setStats] = useState<CRMStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [importing, setImporting] = useState(false);
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);
  const [filter, setFilter] = useState<LeadStatus | 'all'>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [view, setView] = useState<'list' | 'pipeline'>('list');

  useEffect(() => {
    fetchLeads();
    fetchStats();
  }, [filter, searchTerm]);

  const fetchLeads = async () => {
    try {
      const params = new URLSearchParams();
      if (filter !== 'all') params.append('status', filter);
      if (searchTerm) params.append('search', searchTerm);

      const response = await fetch(`/api/crm/leads?${params}`);
      const data = await response.json();
      setLeads(data);
    } catch (error) {
      console.error('Error fetching leads:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/crm/leads?stats=true');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const importLeads = async () => {
    if (!confirm('Import 197 leads from CSV files? This will skip duplicates.')) return;

    setImporting(true);
    try {
      const response = await fetch('/api/crm/import', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          csvFiles: ['100 leads safety - Sheet1.csv', 'new_100_leads_safety.csv'],
        }),
      });

      const result = await response.json();
      alert(`Successfully imported ${result.totalImported} new leads!`);
      fetchLeads();
      fetchStats();
    } catch (error) {
      console.error('Error importing leads:', error);
      alert('Failed to import leads');
    } finally {
      setImporting(false);
    }
  };

  const updateLeadStatus = async (leadId: string, newStatus: LeadStatus) => {
    try {
      const response = await fetch('/api/crm/leads', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: leadId, status: newStatus }),
      });

      if (response.ok) {
        fetchLeads();
        fetchStats();
      }
    } catch (error) {
      console.error('Error updating lead:', error);
    }
  };

  const getStatusColor = (status: LeadStatus) => {
    const colors = {
      new: 'bg-blue-100 text-blue-800',
      contacted: 'bg-yellow-100 text-yellow-800',
      qualified: 'bg-purple-100 text-purple-800',
      nurturing: 'bg-orange-100 text-orange-800',
      customer: 'bg-green-100 text-green-800',
      lost: 'bg-gray-100 text-gray-800',
    };
    return colors[status];
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-7xl mx-auto">
          <p className="text-gray-600">Loading CRM...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">CRM Dashboard</h1>
              <p className="text-gray-600">Manage your SafetyCase AI leads</p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={importLeads}
                disabled={importing}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
              >
                {importing ? 'Importing...' : 'Import 197 Leads'}
              </button>
              <a
                href="/admin"
                className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
              >
                Back to Admin
              </a>
            </div>
          </div>

          {/* Stats Cards */}
          {stats && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-white p-4 rounded-lg shadow">
                <p className="text-gray-600 text-sm">Total Leads</p>
                <p className="text-2xl font-bold">{stats.totalLeads}</p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow">
                <p className="text-gray-600 text-sm">New Leads</p>
                <p className="text-2xl font-bold text-blue-600">{stats.newLeads}</p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow">
                <p className="text-gray-600 text-sm">Customers</p>
                <p className="text-2xl font-bold text-green-600">{stats.customers}</p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow">
                <p className="text-gray-600 text-sm">Conversion Rate</p>
                <p className="text-2xl font-bold text-purple-600">{stats.conversionRate}%</p>
              </div>
            </div>
          )}
        </div>

        {/* Filters and Search */}
        <div className="bg-white rounded-lg shadow p-4 mb-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <input
                type="text"
                placeholder="Search leads by name, company, or email..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-2 border rounded-lg"
              />
            </div>
            <div className="flex gap-2">
              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value as LeadStatus | 'all')}
                className="px-4 py-2 border rounded-lg"
              >
                <option value="all">All Status</option>
                <option value="new">New</option>
                <option value="contacted">Contacted</option>
                <option value="qualified">Qualified</option>
                <option value="nurturing">Nurturing</option>
                <option value="customer">Customer</option>
                <option value="lost">Lost</option>
              </select>
              <button
                onClick={() => setView(view === 'list' ? 'pipeline' : 'list')}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
              >
                {view === 'list' ? 'Pipeline View' : 'List View'}
              </button>
            </div>
          </div>
        </div>

        {/* List View */}
        {view === 'list' && (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Company</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Source</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {leads.map((lead) => (
                  <tr key={lead.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{lead.name}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{lead.company}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-600">{lead.email}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <select
                        value={lead.status}
                        onChange={(e) => updateLeadStatus(lead.id, e.target.value as LeadStatus)}
                        className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(lead.status)}`}
                      >
                        <option value="new">New</option>
                        <option value="contacted">Contacted</option>
                        <option value="qualified">Qualified</option>
                        <option value="nurturing">Nurturing</option>
                        <option value="customer">Customer</option>
                        <option value="lost">Lost</option>
                      </select>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-600">{lead.source}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <a
                        href={`/admin/crm/leads/${lead.id}`}
                        className="text-blue-600 hover:text-blue-800 mr-3"
                      >
                        View
                      </a>
                      <a
                        href={`mailto:${lead.email}`}
                        className="text-green-600 hover:text-green-800"
                      >
                        Email
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {leads.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-600">No leads found. Import leads to get started!</p>
              </div>
            )}
          </div>
        )}

        {/* Pipeline View */}
        {view === 'pipeline' && (
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {(['new', 'contacted', 'qualified', 'nurturing', 'customer', 'lost'] as LeadStatus[]).map((status) => {
              const statusLeads = leads.filter(lead => lead.status === status);
              return (
                <div key={status} className="bg-white rounded-lg shadow p-4">
                  <h3 className="font-bold text-sm uppercase text-gray-700 mb-3">
                    {status} ({statusLeads.length})
                  </h3>
                  <div className="space-y-2">
                    {statusLeads.map(lead => (
                      <div key={lead.id} className="p-3 bg-gray-50 rounded border hover:shadow-md cursor-pointer">
                        <p className="font-medium text-sm">{lead.name}</p>
                        <p className="text-xs text-gray-600">{lead.company}</p>
                        <a
                          href={`/admin/crm/leads/${lead.id}`}
                          className="text-xs text-blue-600 hover:underline"
                        >
                          View →
                        </a>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
