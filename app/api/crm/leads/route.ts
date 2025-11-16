import { NextRequest, NextResponse } from 'next/server';
import {
  getAllLeads,
  createLead,
  updateLead,
  deleteLead,
  getCRMStats,
} from '@/lib/leadManager';
import { Lead } from '@/lib/types';

// GET - Fetch all leads
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const statsOnly = searchParams.get('stats');

    if (statsOnly === 'true') {
      const stats = await getCRMStats();
      return NextResponse.json(stats);
    }

    const leads = await getAllLeads();

    // Optional filtering
    const status = searchParams.get('status');
    const source = searchParams.get('source');
    const search = searchParams.get('search');

    let filteredLeads = leads;

    if (status) {
      filteredLeads = filteredLeads.filter(lead => lead.status === status);
    }

    if (source) {
      filteredLeads = filteredLeads.filter(lead => lead.source === source);
    }

    if (search) {
      const searchLower = search.toLowerCase();
      filteredLeads = filteredLeads.filter(
        lead =>
          lead.name.toLowerCase().includes(searchLower) ||
          lead.company.toLowerCase().includes(searchLower) ||
          lead.email.toLowerCase().includes(searchLower)
      );
    }

    // Sort by updatedAt (most recent first)
    filteredLeads.sort((a, b) =>
      new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()
    );

    return NextResponse.json(filteredLeads);
  } catch (error) {
    console.error('Error fetching leads:', error);
    return NextResponse.json(
      { error: 'Failed to fetch leads' },
      { status: 500 }
    );
  }
}

// POST - Create a new lead
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Validate required fields
    if (!body.name || !body.email || !body.company) {
      return NextResponse.json(
        { error: 'Name, email, and company are required' },
        { status: 400 }
      );
    }

    const leadData: Omit<Lead, 'id' | 'createdAt' | 'updatedAt'> = {
      name: body.name,
      company: body.company,
      email: body.email,
      website: body.website || '',
      selectionReason: body.selectionReason || '',
      status: body.status || 'new',
      source: body.source || 'manual',
      tags: body.tags || [],
      assignedTo: body.assignedTo,
      estimatedValue: body.estimatedValue,
      importedFrom: body.importedFrom,
      linkedOrderId: body.linkedOrderId,
    };

    const newLead = await createLead(leadData);

    return NextResponse.json(newLead, { status: 201 });
  } catch (error) {
    console.error('Error creating lead:', error);
    return NextResponse.json(
      { error: 'Failed to create lead' },
      { status: 500 }
    );
  }
}

// PUT - Update an existing lead
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json();

    if (!body.id) {
      return NextResponse.json(
        { error: 'Lead ID is required' },
        { status: 400 }
      );
    }

    const updates: Partial<Lead> = {};

    // Only update fields that are provided
    if (body.name !== undefined) updates.name = body.name;
    if (body.company !== undefined) updates.company = body.company;
    if (body.email !== undefined) updates.email = body.email;
    if (body.website !== undefined) updates.website = body.website;
    if (body.selectionReason !== undefined) updates.selectionReason = body.selectionReason;
    if (body.status !== undefined) updates.status = body.status;
    if (body.source !== undefined) updates.source = body.source;
    if (body.tags !== undefined) updates.tags = body.tags;
    if (body.assignedTo !== undefined) updates.assignedTo = body.assignedTo;
    if (body.estimatedValue !== undefined) updates.estimatedValue = body.estimatedValue;
    if (body.linkedOrderId !== undefined) updates.linkedOrderId = body.linkedOrderId;

    const updatedLead = await updateLead(body.id, updates);

    if (!updatedLead) {
      return NextResponse.json(
        { error: 'Lead not found' },
        { status: 404 }
      );
    }

    return NextResponse.json(updatedLead);
  } catch (error) {
    console.error('Error updating lead:', error);
    return NextResponse.json(
      { error: 'Failed to update lead' },
      { status: 500 }
    );
  }
}

// DELETE - Delete a lead
export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const id = searchParams.get('id');

    if (!id) {
      return NextResponse.json(
        { error: 'Lead ID is required' },
        { status: 400 }
      );
    }

    const deleted = await deleteLead(id);

    if (!deleted) {
      return NextResponse.json(
        { error: 'Lead not found' },
        { status: 404 }
      );
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Error deleting lead:', error);
    return NextResponse.json(
      { error: 'Failed to delete lead' },
      { status: 500 }
    );
  }
}
