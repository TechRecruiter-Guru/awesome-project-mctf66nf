import { kv } from '@vercel/kv';
import { Lead, Activity, LeadStatus, LeadSource, ActivityType } from './types';

const LEADS_KEY = 'leads';
const ACTIVITIES_KEY = 'activities';

// Lead Management Functions
export async function getAllLeads(): Promise<Lead[]> {
  try {
    const leads = await kv.get<Lead[]>(LEADS_KEY);
    return leads || [];
  } catch (error) {
    console.error('Error fetching leads:', error);
    return [];
  }
}

export async function getLeadById(id: string): Promise<Lead | null> {
  try {
    const leads = await getAllLeads();
    return leads.find(lead => lead.id === id) || null;
  } catch (error) {
    console.error('Error fetching lead:', error);
    return null;
  }
}

export async function createLead(leadData: Omit<Lead, 'id' | 'createdAt' | 'updatedAt'>): Promise<Lead> {
  try {
    const leads = await getAllLeads();
    const newLead: Lead = {
      ...leadData,
      id: generateLeadId(),
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    leads.push(newLead);
    await kv.set(LEADS_KEY, leads);
    return newLead;
  } catch (error) {
    console.error('Error creating lead:', error);
    throw error;
  }
}

export async function updateLead(id: string, updates: Partial<Lead>): Promise<Lead | null> {
  try {
    const leads = await getAllLeads();
    const index = leads.findIndex(lead => lead.id === id);

    if (index === -1) {
      return null;
    }

    leads[index] = {
      ...leads[index],
      ...updates,
      id, // Ensure ID doesn't change
      updatedAt: new Date().toISOString(),
    };

    await kv.set(LEADS_KEY, leads);
    return leads[index];
  } catch (error) {
    console.error('Error updating lead:', error);
    throw error;
  }
}

export async function deleteLead(id: string): Promise<boolean> {
  try {
    const leads = await getAllLeads();
    const filteredLeads = leads.filter(lead => lead.id !== id);

    if (filteredLeads.length === leads.length) {
      return false; // Lead not found
    }

    await kv.set(LEADS_KEY, filteredLeads);

    // Also delete associated activities
    const activities = await getAllActivities();
    const filteredActivities = activities.filter(activity => activity.leadId !== id);
    await kv.set(ACTIVITIES_KEY, filteredActivities);

    return true;
  } catch (error) {
    console.error('Error deleting lead:', error);
    throw error;
  }
}

export async function importLeadsFromCSV(csvData: any[], source: string): Promise<Lead[]> {
  try {
    const existingLeads = await getAllLeads();
    const newLeads: Lead[] = [];

    for (const row of csvData) {
      // Check if lead already exists by email
      const existingLead = existingLeads.find(lead =>
        lead.email.toLowerCase() === row.Email?.toLowerCase()
      );

      if (!existingLead) {
        const newLead: Lead = {
          id: generateLeadId(),
          name: row.Person || '',
          company: row.Company || '',
          email: row.Email || '',
          website: row.Website || '',
          selectionReason: row['Why Selected'] || '',
          status: 'new',
          source: 'csv_import',
          importedFrom: source,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        };
        newLeads.push(newLead);
      }
    }

    const allLeads = [...existingLeads, ...newLeads];
    await kv.set(LEADS_KEY, allLeads);

    return newLeads;
  } catch (error) {
    console.error('Error importing leads from CSV:', error);
    throw error;
  }
}

// Activity Management Functions
export async function getAllActivities(): Promise<Activity[]> {
  try {
    const activities = await kv.get<Activity[]>(ACTIVITIES_KEY);
    return activities || [];
  } catch (error) {
    console.error('Error fetching activities:', error);
    return [];
  }
}

export async function getActivitiesByLeadId(leadId: string): Promise<Activity[]> {
  try {
    const activities = await getAllActivities();
    return activities
      .filter(activity => activity.leadId === leadId)
      .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
  } catch (error) {
    console.error('Error fetching activities for lead:', error);
    return [];
  }
}

export async function createActivity(activityData: Omit<Activity, 'id' | 'createdAt'>): Promise<Activity> {
  try {
    const activities = await getAllActivities();
    const newActivity: Activity = {
      ...activityData,
      id: generateActivityId(),
      createdAt: new Date().toISOString(),
    };

    activities.push(newActivity);
    await kv.set(ACTIVITIES_KEY, activities);

    // Update lead's lastContactedAt if this is a contact activity
    if (['email', 'call', 'meeting', 'demo'].includes(activityData.type)) {
      await updateLead(activityData.leadId, {
        lastContactedAt: new Date().toISOString(),
      });
    }

    return newActivity;
  } catch (error) {
    console.error('Error creating activity:', error);
    throw error;
  }
}

export async function updateActivity(id: string, updates: Partial<Activity>): Promise<Activity | null> {
  try {
    const activities = await getAllActivities();
    const index = activities.findIndex(activity => activity.id === id);

    if (index === -1) {
      return null;
    }

    activities[index] = {
      ...activities[index],
      ...updates,
      id, // Ensure ID doesn't change
    };

    await kv.set(ACTIVITIES_KEY, activities);
    return activities[index];
  } catch (error) {
    console.error('Error updating activity:', error);
    throw error;
  }
}

export async function deleteActivity(id: string): Promise<boolean> {
  try {
    const activities = await getAllActivities();
    const filteredActivities = activities.filter(activity => activity.id !== id);

    if (filteredActivities.length === activities.length) {
      return false; // Activity not found
    }

    await kv.set(ACTIVITIES_KEY, filteredActivities);
    return true;
  } catch (error) {
    console.error('Error deleting activity:', error);
    throw error;
  }
}

// Helper Functions
function generateLeadId(): string {
  const timestamp = Date.now();
  const random = Math.floor(Math.random() * 1000);
  return `LEAD-${timestamp}-${random}`;
}

function generateActivityId(): string {
  const timestamp = Date.now();
  const random = Math.floor(Math.random() * 1000);
  return `ACT-${timestamp}-${random}`;
}

// Stats and Analytics
export async function getCRMStats() {
  try {
    const leads = await getAllLeads();

    const statusCounts = leads.reduce((acc, lead) => {
      acc[lead.status] = (acc[lead.status] || 0) + 1;
      return acc;
    }, {} as Record<LeadStatus, number>);

    const totalLeads = leads.length;
    const customers = statusCounts.customer || 0;
    const conversionRate = totalLeads > 0 ? (customers / totalLeads) * 100 : 0;

    const totalValue = leads
      .filter(lead => lead.estimatedValue)
      .reduce((sum, lead) => sum + (lead.estimatedValue || 0), 0);

    const averageDealValue = customers > 0 ? totalValue / customers : 0;

    return {
      totalLeads,
      newLeads: statusCounts.new || 0,
      contactedLeads: statusCounts.contacted || 0,
      qualifiedLeads: statusCounts.qualified || 0,
      customers,
      lostLeads: statusCounts.lost || 0,
      conversionRate: Math.round(conversionRate * 100) / 100,
      averageDealValue: Math.round(averageDealValue),
    };
  } catch (error) {
    console.error('Error calculating CRM stats:', error);
    return {
      totalLeads: 0,
      newLeads: 0,
      contactedLeads: 0,
      qualifiedLeads: 0,
      customers: 0,
      lostLeads: 0,
      conversionRate: 0,
      averageDealValue: 0,
    };
  }
}
