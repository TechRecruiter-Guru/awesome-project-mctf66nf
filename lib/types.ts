export type TemplateType = 'humanoid' | 'amr' | 'cobot' | 'drone' | 'inspection' | 'construction' | 'healthcare' | 'forklift' | 'service';

export type OrderStatus = 'pending_payment' | 'code_generated' | 'pdf_uploaded' | 'completed';

export interface Order {
  orderId: string;
  templateType: TemplateType;
  email: string;
  companyName: string;
  createdAt: string;
  status: OrderStatus;
  confirmationCode: string | null;
  pdfUploaded: boolean;
  htmlGenerated: boolean;
}

export interface ConfirmationCode {
  code: string;
  orderId: string;
  generatedAt: string;
  used: boolean;
  usedAt: string | null;
}

export interface RiskAssessment {
  scenario: string;
  severity: string;
  likelihood: string;
  riskLevel: string;
  status: string;
}

export interface TestingResult {
  category: string;
  scenarios: number;
  cycles: number;
  passRate: number;
}

// Optional section interfaces
export interface CybersecuritySection {
  authentication?: string;
  encryption?: string;
  firmwareSecurity?: string;
  intrusionDetection?: string;
  vulnerabilityManagement?: string;
  [key: string]: any; // Allow any additional fields
}

export interface AIMachineLearningSection {
  trainingData?: string;
  modelArchitecture?: string;
  validationPerformance?: string;
  adversarialRobustness?: string;
  fieldMonitoring?: string;
  fallbackMechanisms?: string;
  [key: string]: any;
}

export interface MaintenanceSafetySection {
  technicianQualifications?: string;
  lotoProcedures?: string;
  batteryHandling?: string;
  postMaintenanceVerification?: string;
  sparePartsManagement?: string;
  incidentTracking?: string;
  [key: string]: any;
}

export interface SafetyCaseData {
  // Core required fields
  companyName: string;
  robotModel: string;

  // Optional dashboard metrics
  silRating?: string;
  operationalHours?: number;
  hazardsIdentified?: number;
  riskScore?: number;
  complianceRate?: number;
  testCoverage?: number;
  incidentRate?: number;
  certificationBody?: string;
  certificateNumber?: string;

  // Optional structured data
  riskAssessments?: RiskAssessment[];
  complianceStandards?: string[];
  testingResults?: TestingResult[];

  // Optional new sections (only included if present in PDF)
  cybersecurity?: CybersecuritySection;
  aiMachineLearning?: AIMachineLearningSection;
  maintenanceSafety?: MaintenanceSafetySection;

  // Catch-all for any other sections found in PDF
  additionalSections?: Record<string, any>;
}

export interface TemplateInfo {
  id: TemplateType;
  name: string;
  description: string;
  icon: string;
  price: number;
}

// CRM Types
export type LeadStatus = 'new' | 'contacted' | 'qualified' | 'nurturing' | 'customer' | 'lost';
export type LeadSource = 'csv_import' | 'manual' | 'website' | 'referral';
export type ActivityType = 'email' | 'call' | 'meeting' | 'demo' | 'note';

export interface Lead {
  id: string;
  name: string;
  company: string;
  email: string;
  website?: string;
  selectionReason?: string;
  status: LeadStatus;
  source: LeadSource;
  tags?: string[];
  assignedTo?: string;
  estimatedValue?: number;
  createdAt: string;
  updatedAt: string;
  lastContactedAt?: string;
  importedFrom?: string; // CSV filename or source identifier
  linkedOrderId?: string; // Link to Order if they became a customer
}

export interface Activity {
  id: string;
  leadId: string;
  type: ActivityType;
  subject: string;
  notes?: string;
  outcome?: string;
  followUpDate?: string;
  emailSent?: boolean;
  emailSubject?: string;
  emailBody?: string;
  createdAt: string;
  createdBy: string;
}

export interface EmailTemplate {
  id: string;
  name: string;
  subject: string;
  body: string;
  variables?: string[]; // e.g., ['name', 'company', 'robotModel']
  createdAt: string;
}

export interface CRMStats {
  totalLeads: number;
  newLeads: number;
  contactedLeads: number;
  qualifiedLeads: number;
  customers: number;
  lostLeads: number;
  conversionRate: number;
  averageDealValue: number;
}
