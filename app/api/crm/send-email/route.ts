import { NextRequest, NextResponse } from 'next/server';
import { sendEmail, sendEmailTemplate, isValidEmail } from '@/lib/emailer';
import { createActivity } from '@/lib/leadManager';

// POST - Send email to lead
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { to, subject, message, leadId, templateName, variables, isHtml } = body;

    // Validate inputs
    if (!to || !isValidEmail(to)) {
      return NextResponse.json(
        { error: 'Valid email address is required' },
        { status: 400 }
      );
    }

    let emailSent = false;

    // Send using template or direct message
    if (templateName && variables) {
      emailSent = await sendEmailTemplate(to, templateName, variables);
    } else if (subject && message) {
      emailSent = await sendEmail({
        to,
        subject,
        body: message,
        isHtml: isHtml || false,
      });
    } else {
      return NextResponse.json(
        { error: 'Either (subject and message) or (templateName and variables) required' },
        { status: 400 }
      );
    }

    // Log activity if leadId provided
    if (leadId && emailSent) {
      await createActivity({
        leadId,
        type: 'email',
        subject: subject || `Email sent using template: ${templateName}`,
        notes: `Email sent to ${to}`,
        emailSent: true,
        emailSubject: subject,
        emailBody: message,
        createdBy: 'admin',
      });
    }

    return NextResponse.json({
      success: emailSent,
      message: emailSent ? 'Email sent successfully' : 'Failed to send email',
    });
  } catch (error) {
    console.error('Error sending email:', error);
    return NextResponse.json(
      {
        error: 'Failed to send email',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}

// GET - Get available email templates
export async function GET() {
  try {
    const templates = [
      { id: 'welcome', name: 'Welcome Email', description: 'Initial outreach email' },
      { id: 'followup', name: 'Follow-up Email', description: 'Follow up on previous contact' },
      { id: 'demo_scheduled', name: 'Demo Scheduled', description: 'Confirm demo appointment' },
    ];

    return NextResponse.json({ templates });
  } catch (error) {
    console.error('Error fetching templates:', error);
    return NextResponse.json(
      { error: 'Failed to fetch templates' },
      { status: 500 }
    );
  }
}
