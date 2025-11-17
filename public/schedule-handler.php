<?php
/**
 * SafetyCaseAI - Strategy Call Form Handler
 *
 * Upload this file to your Namecheap shared hosting
 * PHP mail() function - No external dependencies
 *
 * SETUP:
 * 1. Upload this file to public_html/schedule-handler.php
 * 2. Make sure PHP mail() is enabled (it is by default on Namecheap)
 * 3. Update the form action URL to point to this file
 * 4. Test by submitting the form
 */

// Enable error reporting for debugging (disable in production)
error_reporting(E_ALL);
ini_set('display_errors', 0); // Don't show errors to user
ini_set('log_errors', 1);
ini_set('error_log', __DIR__ . '/php-errors.log');

// CORS Headers - Allow requests from your Vercel domain
header('Access-Control-Allow-Origin: *'); // Replace * with your Vercel domain for security
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

// Handle preflight OPTIONS request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Only accept POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

// Get JSON data from request body
$json = file_get_contents('php://input');
$data = json_decode($json, true);

// Validate required fields
$requiredFields = [
    'fullName', 'email', 'phone', 'companyName', 'role',
    'numberOfHires', 'hiringUrgency', 'complianceStatus',
    'fundingStage', 'timeline'
];

$missingFields = [];
foreach ($requiredFields as $field) {
    if (empty($data[$field])) {
        $missingFields[] = $field;
    }
}

if (!empty($missingFields)) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'message' => 'Missing required fields: ' . implode(', ', $missingFields)
    ]);
    exit;
}

// Sanitize inputs
$fullName = htmlspecialchars($data['fullName'], ENT_QUOTES, 'UTF-8');
$email = filter_var($data['email'], FILTER_SANITIZE_EMAIL);
$phone = htmlspecialchars($data['phone'], ENT_QUOTES, 'UTF-8');
$companyName = htmlspecialchars($data['companyName'], ENT_QUOTES, 'UTF-8');
$companyWebsite = !empty($data['companyWebsite']) ? htmlspecialchars($data['companyWebsite'], ENT_QUOTES, 'UTF-8') : '';
$role = htmlspecialchars($data['role'], ENT_QUOTES, 'UTF-8');

// Validate email
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Invalid email address']);
    exit;
}

// Process arrays
$hiringRoles = isset($data['hiringRoles']) && is_array($data['hiringRoles']) ? $data['hiringRoles'] : [];
$regulatoryFrameworks = isset($data['regulatoryFrameworks']) && is_array($data['regulatoryFrameworks']) ? $data['regulatoryFrameworks'] : [];
$currentChallenges = isset($data['currentChallenges']) && is_array($data['currentChallenges']) ? $data['currentChallenges'] : [];

// Additional notes
$additionalNotes = !empty($data['additionalNotes']) ? htmlspecialchars($data['additionalNotes'], ENT_QUOTES, 'UTF-8') : '';

// Format hiring roles for display
$hiringRolesDisplay = !empty($hiringRoles)
    ? array_map(function($role) {
        return '<span class="badge">' . strtoupper(str_replace('-', ' ', $role)) . '</span>';
      }, $hiringRoles)
    : ['<span class="field-value">Not specified</span>'];

// Format regulatory frameworks
$regulatoryFrameworksDisplay = !empty($regulatoryFrameworks)
    ? array_map(function($fw) {
        return '<span class="badge">' . strtoupper($fw) . '</span>';
      }, $regulatoryFrameworks)
    : ['<span class="field-value">Not specified</span>'];

// Format challenges
$challengesDisplay = !empty($currentChallenges)
    ? array_map(function($challenge) {
        return '<span class="badge">' . str_replace('-', ' ', $challenge) . '</span>';
      }, $currentChallenges)
    : ['<p>No specific challenges selected</p>'];

// Determine urgency badge class
$urgencyClass = ($data['hiringUrgency'] === 'immediate') ? 'urgent' : '';

// Build HTML email
$htmlEmail = '
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
      <div class="field"><span class="field-label">Name:</span><span class="field-value">' . $fullName . '</span></div>
      <div class="field"><span class="field-label">Email:</span><span class="field-value"><a href="mailto:' . $email . '">' . $email . '</a></span></div>
      <div class="field"><span class="field-label">Phone:</span><span class="field-value"><a href="tel:' . $phone . '">' . $phone . '</a></span></div>
      <div class="field"><span class="field-label">Role:</span><span class="field-value">' . $role . '</span></div>
      <div class="field"><span class="field-label">Company:</span><span class="field-value">' . $companyName . '</span></div>
      ' . ($companyWebsite ? '<div class="field"><span class="field-label">Website:</span><span class="field-value"><a href="' . $companyWebsite . '" target="_blank">' . $companyWebsite . '</a></span></div>' : '') . '
    </div>

    <div class="section">
      <div class="section-title">💼 Recruiting Needs</div>
      <div class="field">
        <span class="field-label">Hiring Roles:</span><br>
        ' . implode('', $hiringRolesDisplay) . '
      </div>
      <div class="field"><span class="field-label">Number of Hires:</span><span class="field-value">' . htmlspecialchars($data['numberOfHires']) . '</span></div>
      <div class="field">
        <span class="field-label">Urgency:</span>
        <span class="badge ' . $urgencyClass . '">' . strtoupper(str_replace('-', ' ', $data['hiringUrgency'])) . '</span>
      </div>
    </div>

    <div class="section">
      <div class="section-title">📋 Compliance Needs</div>
      <div class="field"><span class="field-label">Status:</span><span class="field-value">' . str_replace('-', ' ', $data['complianceStatus']) . '</span></div>
      <div class="field">
        <span class="field-label">Regulatory Frameworks:</span><br>
        ' . implode('', $regulatoryFrameworksDisplay) . '
      </div>
    </div>

    <div class="section">
      <div class="section-title">⚠️ Current Challenges</div>
      ' . implode('', $challengesDisplay) . '
    </div>

    <div class="section">
      <div class="section-title">📊 Business Context</div>
      <div class="field"><span class="field-label">Funding Stage:</span><span class="field-value">' . strtoupper(str_replace('-', ' ', $data['fundingStage'])) . '</span></div>
      <div class="field"><span class="field-label">Timeline to Start:</span><span class="field-value">' . str_replace('-', ' ', $data['timeline']) . '</span></div>
    </div>

    ' . ($additionalNotes ? '
    <div class="section">
      <div class="section-title">💬 Additional Notes</div>
      <p>' . nl2br($additionalNotes) . '</p>
    </div>
    ' : '') . '

    <div class="footer">
      <p><strong>Next Steps:</strong> Review this request and schedule a call within 24 hours</p>
      <p style="font-size: 12px; color: #999;">Submitted at ' . date('Y-m-d H:i:s T') . '</p>
    </div>
  </div>
</body>
</html>
';

// Plain text version
$textEmail = "
NEW STRATEGY CALL REQUEST - SafetyCaseAI
========================================

CONTACT INFORMATION
-------------------
Name: $fullName
Email: $email
Phone: $phone
Role: $role
Company: $companyName
" . ($companyWebsite ? "Website: $companyWebsite\n" : "") . "

RECRUITING NEEDS
----------------
Hiring Roles: " . (!empty($hiringRoles) ? implode(', ', $hiringRoles) : 'Not specified') . "
Number of Hires: " . $data['numberOfHires'] . "
Urgency: " . $data['hiringUrgency'] . "

COMPLIANCE NEEDS
----------------
Status: " . $data['complianceStatus'] . "
Regulatory Frameworks: " . (!empty($regulatoryFrameworks) ? implode(', ', $regulatoryFrameworks) : 'Not specified') . "

CURRENT CHALLENGES
------------------
" . (!empty($currentChallenges) ? implode(', ', $currentChallenges) : 'None selected') . "

BUSINESS CONTEXT
----------------
Funding Stage: " . $data['fundingStage'] . "
Timeline to Start: " . $data['timeline'] . "

" . ($additionalNotes ? "ADDITIONAL NOTES\n----------------\n$additionalNotes\n" : "") . "

---
Submitted at " . date('Y-m-d H:i:s T') . "
";

// Email configuration
$to = 'jp@physicalaipros.com';
$subject = '🚀 New Strategy Call: ' . $companyName . ' (' . $data['fundingStage'] . ')';

// Headers for HTML email
$headers = [
    'From: SafetyCaseAI <noreply@' . $_SERVER['HTTP_HOST'] . '>',
    'Reply-To: ' . $email,
    'MIME-Version: 1.0',
    'Content-Type: text/html; charset=UTF-8',
    'X-Mailer: PHP/' . phpversion()
];

$headersString = implode("\r\n", $headers);

// Send email using PHP mail()
$mailSent = mail($to, $subject, $htmlEmail, $headersString);

// Also send a plain text copy as backup
if ($mailSent) {
    $textHeaders = [
        'From: SafetyCaseAI <noreply@' . $_SERVER['HTTP_HOST'] . '>',
        'Reply-To: ' . $email,
        'Content-Type: text/plain; charset=UTF-8'
    ];
    mail($to, $subject . ' [TEXT]', $textEmail, implode("\r\n", $textHeaders));
}

// Log the submission (optional)
$logEntry = date('Y-m-d H:i:s') . " - $companyName ($email) - Mail sent: " . ($mailSent ? 'YES' : 'NO') . "\n";
@file_put_contents(__DIR__ . '/form-submissions.log', $logEntry, FILE_APPEND);

// Return JSON response
if ($mailSent) {
    http_response_code(200);
    echo json_encode([
        'success' => true,
        'message' => 'Strategy call request submitted successfully',
        'emailSent' => true
    ]);
} else {
    http_response_code(500);
    error_log('Mail function failed for: ' . $email);
    echo json_encode([
        'success' => false,
        'message' => 'Failed to send email. Please email jp@physicalaipros.com directly.'
    ]);
}
