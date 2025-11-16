'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { Lead, Activity, ActivityType } from '@/lib/types';

export default function LeadDetailPage() {
  const params = useParams();
  const leadId = params.id as string;

  const [lead, setLead] = useState<Lead | null>(null);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);
  const [showActivityForm, setShowActivityForm] = useState(false);
  const [showEmailForm, setShowEmailForm] = useState(false);

  // Activity form state
  const [activityType, setActivityType] = useState<ActivityType>('note');
  const [activitySubject, setActivitySubject] = useState('');
  const [activityNotes, setActivityNotes] = useState('');
  const [activityOutcome, setActivityOutcome] = useState('');
  const [followUpDate, setFollowUpDate] = useState('');

  // Email form state
  const [emailSubject, setEmailSubject] = useState('');
  const [emailBody, setEmailBody] = useState('');
  const [emailTemplate, setEmailTemplate] = useState('');

  useEffect(() => {
    fetchLead();
    fetchActivities();
  }, [leadId]);

  const fetchLead = async () => {
    try {
      const response = await fetch(`/api/crm/leads`);
      const allLeads = await response.json();
      const foundLead = allLeads.find((l: Lead) => l.id === leadId);
      setLead(foundLead || null);
    } catch (error) {
      console.error('Error fetching lead:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchActivities = async () => {
    try {
      const response = await fetch(`/api/crm/activities?leadId=${leadId}`);
      const data = await response.json();
      setActivities(data);
    } catch (error) {
      console.error('Error fetching activities:', error);
    }
  };

  const addActivity = async () => {
    if (!activitySubject) {
      alert('Please enter a subject');
      return;
    }

    try {
      const response = await fetch('/api/crm/activities', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          leadId,
          type: activityType,
          subject: activitySubject,
          notes: activityNotes,
          outcome: activityOutcome,
          followUpDate: followUpDate || undefined,
          createdBy: 'admin',
        }),
      });

      if (response.ok) {
        setActivitySubject('');
        setActivityNotes('');
        setActivityOutcome('');
        setFollowUpDate('');
        setShowActivityForm(false);
        fetchActivities();
      }
    } catch (error) {
      console.error('Error adding activity:', error);
      alert('Failed to add activity');
    }
  };

  const sendEmail = async () => {
    if (!emailSubject || !emailBody) {
      alert('Please enter subject and message');
      return;
    }

    if (!lead) return;

    try {
      const response = await fetch('/api/crm/send-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          to: lead.email,
          subject: emailSubject,
          message: emailBody,
          leadId,
        }),
      });

      const result = await response.json();

      if (result.success) {
        alert('Email sent successfully!');
        setEmailSubject('');
        setEmailBody('');
        setShowEmailForm(false);
        fetchActivities();
      } else {
        alert(`Failed to send email: ${result.details || result.message}`);
      }
    } catch (error) {
      console.error('Error sending email:', error);
      alert('Failed to send email');
    }
  };

  const loadEmailTemplate = async (templateName: string) => {
    if (!lead || !templateName) return;

    const templates: Record<string, { subject: string; body: string }> = {
      welcome: {
        subject: `Welcome to SafetyCase AI - ${lead.name}`,
        body: `Hi ${lead.name},\n\nThank you for your interest in SafetyCase AI!\n\nWe noticed you work at ${lead.company}, and we'd love to show you how our AI-powered robot safety documentation platform can help streamline your compliance process.\n\nWould you be available for a quick 15-minute demo this week?\n\nBest regards,\nThe SafetyCase AI Team\njp@physicalaipros.com`,
      },
      followup: {
        subject: 'Following up - SafetyCase AI Demo',
        body: `Hi ${lead.name},\n\nI wanted to follow up on my previous email about SafetyCase AI.\n\nWe're helping companies like ${lead.company} automate their robot safety documentation and compliance workflows.\n\nAre you available for a brief call to discuss how we can help?\n\nBest regards,\nThe SafetyCase AI Team\njp@physicalaipros.com`,
      },
    };

    const template = templates[templateName];
    if (template) {
      setEmailSubject(template.subject);
      setEmailBody(template.body);
    }
  };

  const getActivityIcon = (type: ActivityType) => {
    const icons = {
      email: '📧',
      call: '📞',
      meeting: '🤝',
      demo: '🖥️',
      note: '📝',
    };
    return icons[type];
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-4xl mx-auto">
          <p className="text-gray-600">Loading lead...</p>
        </div>
      </div>
    );
  }

  if (!lead) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-4xl mx-auto">
          <p className="text-red-600">Lead not found</p>
          <a href="/admin/crm" className="text-blue-600 hover:underline">
            Back to CRM
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <a href="/admin/crm" className="text-blue-600 hover:underline mb-2 inline-block">
            ← Back to CRM
          </a>
          <h1 className="text-3xl font-bold text-gray-900">{lead.name}</h1>
          <p className="text-gray-600">{lead.company}</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Lead Info */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow p-6 mb-6">
              <h2 className="text-lg font-bold mb-4">Contact Information</h2>
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-gray-600">Email</p>
                  <a href={`mailto:${lead.email}`} className="text-blue-600 hover:underline">
                    {lead.email}
                  </a>
                </div>
                {lead.website && (
                  <div>
                    <p className="text-sm text-gray-600">Website</p>
                    <a
                      href={lead.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      {lead.website}
                    </a>
                  </div>
                )}
                <div>
                  <p className="text-sm text-gray-600">Status</p>
                  <p className="font-medium capitalize">{lead.status}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Source</p>
                  <p className="font-medium capitalize">{lead.source.replace('_', ' ')}</p>
                </div>
                {lead.selectionReason && (
                  <div>
                    <p className="text-sm text-gray-600">Why Selected</p>
                    <p className="text-sm">{lead.selectionReason}</p>
                  </div>
                )}
              </div>

              <div className="mt-6 space-y-2">
                <button
                  onClick={() => setShowEmailForm(!showEmailForm)}
                  className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  📧 Send Email
                </button>
                <button
                  onClick={() => setShowActivityForm(!showActivityForm)}
                  className="w-full px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
                >
                  ➕ Log Activity
                </button>
              </div>
            </div>
          </div>

          {/* Activities Timeline */}
          <div className="lg:col-span-2">
            {/* Email Form */}
            {showEmailForm && (
              <div className="bg-white rounded-lg shadow p-6 mb-6">
                <h3 className="text-lg font-bold mb-4">Send Email</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Template</label>
                    <select
                      value={emailTemplate}
                      onChange={(e) => {
                        setEmailTemplate(e.target.value);
                        loadEmailTemplate(e.target.value);
                      }}
                      className="w-full px-3 py-2 border rounded-lg"
                    >
                      <option value="">Custom Email</option>
                      <option value="welcome">Welcome Email</option>
                      <option value="followup">Follow-up Email</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Subject</label>
                    <input
                      type="text"
                      value={emailSubject}
                      onChange={(e) => setEmailSubject(e.target.value)}
                      className="w-full px-3 py-2 border rounded-lg"
                      placeholder="Email subject"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Message</label>
                    <textarea
                      value={emailBody}
                      onChange={(e) => setEmailBody(e.target.value)}
                      rows={8}
                      className="w-full px-3 py-2 border rounded-lg"
                      placeholder="Email message"
                    />
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={sendEmail}
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                    >
                      Send Email
                    </button>
                    <button
                      onClick={() => setShowEmailForm(false)}
                      className="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Activity Form */}
            {showActivityForm && (
              <div className="bg-white rounded-lg shadow p-6 mb-6">
                <h3 className="text-lg font-bold mb-4">Log Activity</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Type</label>
                    <select
                      value={activityType}
                      onChange={(e) => setActivityType(e.target.value as ActivityType)}
                      className="w-full px-3 py-2 border rounded-lg"
                    >
                      <option value="note">Note</option>
                      <option value="call">Call</option>
                      <option value="meeting">Meeting</option>
                      <option value="demo">Demo</option>
                      <option value="email">Email</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Subject</label>
                    <input
                      type="text"
                      value={activitySubject}
                      onChange={(e) => setActivitySubject(e.target.value)}
                      className="w-full px-3 py-2 border rounded-lg"
                      placeholder="Activity subject"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Notes</label>
                    <textarea
                      value={activityNotes}
                      onChange={(e) => setActivityNotes(e.target.value)}
                      rows={3}
                      className="w-full px-3 py-2 border rounded-lg"
                      placeholder="Activity notes"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Outcome</label>
                    <input
                      type="text"
                      value={activityOutcome}
                      onChange={(e) => setActivityOutcome(e.target.value)}
                      className="w-full px-3 py-2 border rounded-lg"
                      placeholder="Activity outcome"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Follow-up Date</label>
                    <input
                      type="date"
                      value={followUpDate}
                      onChange={(e) => setFollowUpDate(e.target.value)}
                      className="w-full px-3 py-2 border rounded-lg"
                    />
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={addActivity}
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                    >
                      Log Activity
                    </button>
                    <button
                      onClick={() => setShowActivityForm(false)}
                      className="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Activities List */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-bold mb-4">Activity Timeline</h3>
              <div className="space-y-4">
                {activities.map((activity) => (
                  <div key={activity.id} className="border-l-4 border-blue-500 pl-4 py-2">
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-xl">{getActivityIcon(activity.type)}</span>
                          <h4 className="font-semibold">{activity.subject}</h4>
                        </div>
                        {activity.notes && <p className="text-sm text-gray-600 mt-1">{activity.notes}</p>}
                        {activity.outcome && (
                          <p className="text-sm text-gray-800 mt-1">
                            <strong>Outcome:</strong> {activity.outcome}
                          </p>
                        )}
                        {activity.followUpDate && (
                          <p className="text-sm text-orange-600 mt-1">
                            <strong>Follow-up:</strong> {new Date(activity.followUpDate).toLocaleDateString()}
                          </p>
                        )}
                      </div>
                      <span className="text-xs text-gray-500">
                        {new Date(activity.createdAt).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                ))}
                {activities.length === 0 && (
                  <p className="text-gray-600 text-center py-8">
                    No activities yet. Log your first activity to get started!
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
