import { NextRequest, NextResponse } from 'next/server';
import {
  getAllActivities,
  getActivitiesByLeadId,
  createActivity,
  updateActivity,
  deleteActivity,
} from '@/lib/leadManager';
import { Activity } from '@/lib/types';

// GET - Fetch activities (all or by leadId)
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const leadId = searchParams.get('leadId');

    if (leadId) {
      const activities = await getActivitiesByLeadId(leadId);
      return NextResponse.json(activities);
    }

    const activities = await getAllActivities();

    // Sort by createdAt (most recent first)
    activities.sort((a, b) =>
      new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    );

    return NextResponse.json(activities);
  } catch (error) {
    console.error('Error fetching activities:', error);
    return NextResponse.json(
      { error: 'Failed to fetch activities' },
      { status: 500 }
    );
  }
}

// POST - Create a new activity
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Validate required fields
    if (!body.leadId || !body.type || !body.subject) {
      return NextResponse.json(
        { error: 'leadId, type, and subject are required' },
        { status: 400 }
      );
    }

    const activityData: Omit<Activity, 'id' | 'createdAt'> = {
      leadId: body.leadId,
      type: body.type,
      subject: body.subject,
      notes: body.notes || '',
      outcome: body.outcome,
      followUpDate: body.followUpDate,
      emailSent: body.emailSent || false,
      emailSubject: body.emailSubject,
      emailBody: body.emailBody,
      createdBy: body.createdBy || 'admin',
    };

    const newActivity = await createActivity(activityData);

    return NextResponse.json(newActivity, { status: 201 });
  } catch (error) {
    console.error('Error creating activity:', error);
    return NextResponse.json(
      { error: 'Failed to create activity' },
      { status: 500 }
    );
  }
}

// PUT - Update an existing activity
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json();

    if (!body.id) {
      return NextResponse.json(
        { error: 'Activity ID is required' },
        { status: 400 }
      );
    }

    const updates: Partial<Activity> = {};

    // Only update fields that are provided
    if (body.type !== undefined) updates.type = body.type;
    if (body.subject !== undefined) updates.subject = body.subject;
    if (body.notes !== undefined) updates.notes = body.notes;
    if (body.outcome !== undefined) updates.outcome = body.outcome;
    if (body.followUpDate !== undefined) updates.followUpDate = body.followUpDate;
    if (body.emailSent !== undefined) updates.emailSent = body.emailSent;
    if (body.emailSubject !== undefined) updates.emailSubject = body.emailSubject;
    if (body.emailBody !== undefined) updates.emailBody = body.emailBody;

    const updatedActivity = await updateActivity(body.id, updates);

    if (!updatedActivity) {
      return NextResponse.json(
        { error: 'Activity not found' },
        { status: 404 }
      );
    }

    return NextResponse.json(updatedActivity);
  } catch (error) {
    console.error('Error updating activity:', error);
    return NextResponse.json(
      { error: 'Failed to update activity' },
      { status: 500 }
    );
  }
}

// DELETE - Delete an activity
export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const id = searchParams.get('id');

    if (!id) {
      return NextResponse.json(
        { error: 'Activity ID is required' },
        { status: 400 }
      );
    }

    const deleted = await deleteActivity(id);

    if (!deleted) {
      return NextResponse.json(
        { error: 'Activity not found' },
        { status: 404 }
      );
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Error deleting activity:', error);
    return NextResponse.json(
      { error: 'Failed to delete activity' },
      { status: 500 }
    );
  }
}
