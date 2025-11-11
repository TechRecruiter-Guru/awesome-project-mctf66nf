export type TemplateType = 'humanoid' | 'amr' | 'cobot' | 'drone' | 'inspection' | 'construction' | 'healthcare' | 'forklift';

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
