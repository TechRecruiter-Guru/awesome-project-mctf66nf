export type TemplateType = 'humanoid' | 'amr' | 'cobot' | 'drone' | 'inspection';

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

export interface SafetyCaseData {
  companyName: string;
  robotModel: string;
  silRating: string;
  operationalHours: number;
  hazardsIdentified: number;
  riskScore: number;
  complianceRate: number;
  testCoverage: number;
  incidentRate: number;
  certificationBody: string;
  certificateNumber: string;
  riskAssessments: RiskAssessment[];
  complianceStandards: string[];
  testingResults: TestingResult[];
}

export interface TemplateInfo {
  id: TemplateType;
  name: string;
  description: string;
  icon: string;
  price: number;
}
