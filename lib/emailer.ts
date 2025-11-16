/**
 * Native Node.js SMTP Email Sender (Zero NPM Dependencies)
 * Configured for NameCheap SMTP
 */

import * as tls from 'tls';
import * as net from 'net';

export interface EmailOptions {
  to: string;
  subject: string;
  body: string;
  from?: string;
  replyTo?: string;
  cc?: string;
  bcc?: string;
  isHtml?: boolean;
}

export interface SMTPConfig {
  host: string;
  port: number;
  secure: boolean;
  auth: {
    user: string;
    pass: string;
  };
}

// Default NameCheap SMTP Configuration
const DEFAULT_SMTP_CONFIG: SMTPConfig = {
  host: process.env.SMTP_HOST || 'mail.privateemail.com', // NameCheap Private Email SMTP
  port: parseInt(process.env.SMTP_PORT || '465'), // 465 for SSL, 587 for TLS
  secure: process.env.SMTP_SECURE === 'true' || true, // Use SSL
  auth: {
    user: process.env.SMTP_USER || 'jp@physicalaipros.com',
    pass: process.env.SMTP_PASS || '', // Set in environment variables
  },
};

/**
 * Send email using native Node.js TLS/Net
 */
export async function sendEmail(options: EmailOptions, config?: Partial<SMTPConfig>): Promise<boolean> {
  const smtpConfig = { ...DEFAULT_SMTP_CONFIG, ...config };

  return new Promise((resolve, reject) => {
    const from = options.from || smtpConfig.auth.user;
    const replyTo = options.replyTo || from;

    // Create email message
    const boundary = `----=_Part_${Date.now()}_${Math.random()}`;
    const contentType = options.isHtml
      ? 'text/html; charset=utf-8'
      : 'text/plain; charset=utf-8';

    const emailMessage = [
      `From: ${from}`,
      `To: ${options.to}`,
      options.cc ? `Cc: ${options.cc}` : '',
      options.bcc ? `Bcc: ${options.bcc}` : '',
      `Reply-To: ${replyTo}`,
      `Subject: ${options.subject}`,
      `MIME-Version: 1.0`,
      `Content-Type: ${contentType}`,
      `Date: ${new Date().toUTCString()}`,
      '',
      options.body,
      '',
    ]
      .filter(line => line !== '')
      .join('\r\n');

    // Encode credentials
    const authUser = Buffer.from(smtpConfig.auth.user).toString('base64');
    const authPass = Buffer.from(smtpConfig.auth.pass).toString('base64');

    let socket: tls.TLSSocket | net.Socket;
    let responses: string[] = [];
    let currentStep = 0;

    const smtpSteps = [
      { send: '', expect: '220' }, // Initial connection
      { send: `EHLO ${smtpConfig.host}\r\n`, expect: '250' },
      { send: 'AUTH LOGIN\r\n', expect: '334' },
      { send: `${authUser}\r\n`, expect: '334' },
      { send: `${authPass}\r\n`, expect: '235' },
      { send: `MAIL FROM:<${from}>\r\n`, expect: '250' },
      { send: `RCPT TO:<${options.to}>\r\n`, expect: '250' },
      { send: 'DATA\r\n', expect: '354' },
      { send: `${emailMessage}\r\n.\r\n`, expect: '250' },
      { send: 'QUIT\r\n', expect: '221' },
    ];

    const handleData = (data: Buffer) => {
      const response = data.toString();
      console.log('SMTP Response:', response);
      responses.push(response);

      const expectedCode = smtpSteps[currentStep].expect;

      if (response.startsWith(expectedCode)) {
        currentStep++;

        if (currentStep < smtpSteps.length) {
          const nextCommand = smtpSteps[currentStep].send;
          if (nextCommand) {
            socket.write(nextCommand);
          }
        } else {
          // All steps completed successfully
          socket.end();
          resolve(true);
        }
      } else if (response.startsWith('4') || response.startsWith('5')) {
        // SMTP error
        socket.end();
        reject(new Error(`SMTP Error: ${response}`));
      }
    };

    const handleError = (error: Error) => {
      console.error('SMTP Error:', error);
      reject(error);
    };

    const handleClose = () => {
      if (currentStep < smtpSteps.length - 1) {
        reject(new Error('Connection closed before completion'));
      }
    };

    // Create connection
    if (smtpConfig.secure) {
      // SSL connection (port 465)
      socket = tls.connect(
        {
          host: smtpConfig.host,
          port: smtpConfig.port,
          rejectUnauthorized: false, // For self-signed certificates
        },
        () => {
          console.log('Secure connection established');
        }
      );
    } else {
      // TLS connection (port 587)
      socket = net.connect(
        {
          host: smtpConfig.host,
          port: smtpConfig.port,
        },
        () => {
          console.log('Connection established');
        }
      );
    }

    socket.on('data', handleData);
    socket.on('error', handleError);
    socket.on('close', handleClose);

    socket.setTimeout(30000, () => {
      socket.end();
      reject(new Error('Connection timeout'));
    });
  });
}

/**
 * Send email template with variable replacement
 */
export async function sendEmailTemplate(
  to: string,
  templateName: string,
  variables: Record<string, string>
): Promise<boolean> {
  // Load email templates (you can store these in a database or file)
  const templates = getEmailTemplates();
  const template = templates[templateName];

  if (!template) {
    throw new Error(`Template "${templateName}" not found`);
  }

  // Replace variables in subject and body
  let subject = template.subject;
  let body = template.body;

  Object.keys(variables).forEach(key => {
    const placeholder = `{{${key}}}`;
    subject = subject.replace(new RegExp(placeholder, 'g'), variables[key]);
    body = body.replace(new RegExp(placeholder, 'g'), variables[key]);
  });

  return sendEmail({
    to,
    subject,
    body,
    isHtml: template.isHtml,
  });
}

/**
 * Email templates (can be moved to database)
 */
function getEmailTemplates(): Record<string, { subject: string; body: string; isHtml: boolean }> {
  return {
    welcome: {
      subject: 'Welcome to SafetyCase AI - {{name}}',
      body: `Hi {{name}},

Thank you for your interest in SafetyCase AI!

We noticed you work at {{company}}, and we'd love to show you how our AI-powered robot safety documentation platform can help streamline your compliance process.

Would you be available for a quick 15-minute demo this week?

Best regards,
The SafetyCase AI Team
jp@physicalaipros.com`,
      isHtml: false,
    },
    followup: {
      subject: 'Following up - SafetyCase AI Demo',
      body: `Hi {{name}},

I wanted to follow up on my previous email about SafetyCase AI.

We're helping companies like {{company}} automate their robot safety documentation and compliance workflows.

Are you available for a brief call to discuss how we can help?

Best regards,
The SafetyCase AI Team
jp@physicalaipros.com`,
      isHtml: false,
    },
    demo_scheduled: {
      subject: 'SafetyCase AI Demo Scheduled - {{date}}',
      body: `Hi {{name}},

Great! Your demo is scheduled for {{date}} at {{time}}.

Meeting Link: {{meetingLink}}

Looking forward to showing you how SafetyCase AI can transform your safety documentation process.

Best regards,
The SafetyCase AI Team
jp@physicalaipros.com`,
      isHtml: false,
    },
  };
}

/**
 * Validate email address
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
