import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.json();

    // Validate required fields
    const requiredFields = ['fullName', 'email', 'phone', 'companyName', 'role', 'numberOfHires', 'hiringUrgency', 'complianceStatus', 'fundingStage', 'timeline'];
    const missingFields = requiredFields.filter(field => !formData[field]);

    if (missingFields.length > 0) {
      return NextResponse.json(
        { message: `Missing required fields: ${missingFields.join(', ')}` },
        { status: 400 }
      );
    }

    // Format the email body
    const emailBody = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
    .container { max-width: 800px; margin: 0 auto; padding: 20px; }
    .header { background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
    .header h1 { margin: 0; font-size: 28px; }
    .section { background: #f9fafb; border-left: 4px solid #7c3aed; padding: 20px; margin-bottom: 20px; border-radius: 5px; }
    .section-title { color: #7c3aed; font-size: 20px; font-weight: bold; margin-bottom: 15px; }
    .field { margin-bottom: 12px; }
    .field-label { font-weight: bold; color: #555; }
    .field-value { color: #333; margin-left: 10px; }
    .badge { display: inline-block; background: #7c3aed; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; margin: 4px; }
    .urgent { background: #ef4444; }
    .footer { text-align: center; color: #666; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🚀 New Strategy Call Request</h1>
      <p style="margin: 5px 0 0 0; opacity: 0.9;">From SafetyCaseAI Landing Page</p>
    </div>

    <div class="section">
      <div class="section-title">👤 Contact Information</div>
      <div class="field"><span class="field-label">Name:</span><span class="field-value">${formData.fullName}</span></div>
      <div class="field"><span class="field-label">Email:</span><span class="field-value"><a href="mailto:${formData.email}">${formData.email}</a></span></div>
      <div class="field"><span class="field-label">Phone:</span><span class="field-value"><a href="tel:${formData.phone}">${formData.phone}</a></span></div>
      <div class="field"><span class="field-label">Role:</span><span class="field-value">${formData.role}</span></div>
      <div class="field"><span class="field-label">Company:</span><span class="field-value">${formData.companyName}</span></div>
      ${formData.companyWebsite ? `<div class="field"><span class="field-label">Website:</span><span class="field-value"><a href="${formData.companyWebsite}" target="_blank">${formData.companyWebsite}</a></span></div>` : ''}
    </div>

    <div class="section">
      <div class="section-title">💼 Recruiting Needs</div>
      <div class="field">
        <span class="field-label">Hiring Roles:</span><br>
        ${formData.hiringRoles.length > 0 ? formData.hiringRoles.map((role: string) => `<span class="badge">${role.replace(/-/g, ' ').toUpperCase()}</span>`).join('') : '<span class="field-value">Not specified</span>'}
      </div>
      <div class="field"><span class="field-label">Number of Hires:</span><span class="field-value">${formData.numberOfHires}</span></div>
      <div class="field">
        <span class="field-label">Urgency:</span>
        <span class="badge ${formData.hiringUrgency === 'immediate' ? 'urgent' : ''}">${formData.hiringUrgency.replace(/-/g, ' ').toUpperCase()}</span>
      </div>
    </div>

    <div class="section">
      <div class="section-title">📋 Compliance Needs</div>
      <div class="field"><span class="field-label">Status:</span><span class="field-value">${formData.complianceStatus.replace(/-/g, ' ')}</span></div>
      <div class="field">
        <span class="field-label">Regulatory Frameworks:</span><br>
        ${formData.regulatoryFrameworks.length > 0 ? formData.regulatoryFrameworks.map((fw: string) => `<span class="badge">${fw.toUpperCase()}</span>`).join('') : '<span class="field-value">Not specified</span>'}
      </div>
    </div>

    <div class="section">
      <div class="section-title">⚠️ Current Challenges</div>
      ${formData.currentChallenges.length > 0 ? formData.currentChallenges.map((challenge: string) => `<span class="badge">${challenge.replace(/-/g, ' ')}</span>`).join('') : '<p>No specific challenges selected</p>'}
    </div>

    <div class="section">
      <div class="section-title">📊 Business Context</div>
      <div class="field"><span class="field-label">Funding Stage:</span><span class="field-value">${formData.fundingStage.replace(/-/g, ' ').toUpperCase()}</span></div>
      <div class="field"><span class="field-label">Timeline to Start:</span><span class="field-value">${formData.timeline.replace(/-/g, ' ')}</span></div>
    </div>

    ${formData.additionalNotes ? `
    <div class="section">
      <div class="section-title">💬 Additional Notes</div>
      <p>${formData.additionalNotes.replace(/\n/g, '<br>')}</p>
    </div>
    ` : ''}

    <div class="footer">
      <p><strong>Next Steps:</strong> Review this request and schedule a call within 24 hours</p>
      <p style="font-size: 12px; color: #999;">Submitted at ${new Date().toLocaleString('en-US', { timeZone: 'America/New_York' })} EST</p>
    </div>
  </div>
</body>
</html>
    `.trim();

    // Plain text version for email clients that don't support HTML
    const plainTextBody = `
NEW STRATEGY CALL REQUEST - SafetyCaseAI
========================================

CONTACT INFORMATION
-------------------
Name: ${formData.fullName}
Email: ${formData.email}
Phone: ${formData.phone}
Role: ${formData.role}
Company: ${formData.companyName}
${formData.companyWebsite ? `Website: ${formData.companyWebsite}` : ''}

RECRUITING NEEDS
----------------
Hiring Roles: ${formData.hiringRoles.join(', ') || 'Not specified'}
Number of Hires: ${formData.numberOfHires}
Urgency: ${formData.hiringUrgency}

COMPLIANCE NEEDS
----------------
Status: ${formData.complianceStatus}
Regulatory Frameworks: ${formData.regulatoryFrameworks.join(', ') || 'Not specified'}

CURRENT CHALLENGES
------------------
${formData.currentChallenges.join(', ') || 'None selected'}

BUSINESS CONTEXT
----------------
Funding Stage: ${formData.fundingStage}
Timeline to Start: ${formData.timeline}

${formData.additionalNotes ? `ADDITIONAL NOTES\n----------------\n${formData.additionalNotes}` : ''}

---
Submitted at ${new Date().toLocaleString('en-US', { timeZone: 'America/New_York' })} EST
    `.trim();

    // Try to send via Resend if API key is available
    const resendApiKey = process.env.RESEND_API_KEY;

    if (resendApiKey) {
      try {
        const resendResponse = await fetch('https://api.resend.com/emails', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${resendApiKey}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            from: 'SafetyCaseAI <noreply@safetycaseai.com>',
            to: ['jp@physicalaipros.com'],
            subject: `🚀 New Strategy Call: ${formData.companyName} (${formData.fundingStage})`,
            html: emailBody,
            text: plainTextBody,
            reply_to: formData.email,
          }),
        });

        if (!resendResponse.ok) {
          const errorData = await resendResponse.json();
          console.error('Resend API error:', errorData);
          throw new Error('Email delivery failed');
        }

        console.log('Email sent successfully via Resend');
      } catch (emailError) {
        console.error('Failed to send email via Resend:', emailError);
        // Continue anyway - we'll log it
      }
    } else {
      // No email service configured - just log it
      console.log('=== NEW STRATEGY CALL REQUEST ===');
      console.log(plainTextBody);
      console.log('=== END REQUEST ===');
      console.warn('⚠️  RESEND_API_KEY not configured. Email not sent. Add RESEND_API_KEY to environment variables.');
    }

    // Also store in a simple log file or database if needed
    // For now, just return success

    return NextResponse.json({
      success: true,
      message: 'Strategy call request submitted successfully',
      emailSent: !!resendApiKey
    }, { status: 200 });

  } catch (error) {
    console.error('Error processing strategy call request:', error);
    return NextResponse.json(
      { message: 'Failed to submit request. Please try again or email jp@physicalaipros.com directly.' },
      { status: 500 }
    );
  }
}
