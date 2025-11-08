import fs from 'fs';
import path from 'path';
import { SafetyCaseData, TemplateType } from './types';

export function getTemplateHtml(templateType: TemplateType): string {
  const templatePath = path.join(
    process.cwd(),
    'templates',
    `${templateType}.html`
  );

  try {
    return fs.readFileSync(templatePath, 'utf-8');
  } catch (error) {
    throw new Error(`Template not found: ${templateType}`);
  }
}

export function populateTemplate(
  templateType: TemplateType,
  data: SafetyCaseData
): string {
  let html = getTemplateHtml(templateType);

  // Replace scalar placeholders
  html = html.replace(/\[COMPANY_NAME\]/g, escapeHtml(data.companyName));
  html = html.replace(/\[ROBOT_MODEL\]/g, escapeHtml(data.robotModel));
  html = html.replace(/\[SIL_RATING\]/g, escapeHtml(data.silRating));
  html = html.replace(/\[OPERATIONAL_HOURS\]/g, data.operationalHours.toString());
  html = html.replace(/\[HAZARDS_IDENTIFIED\]/g, data.hazardsIdentified.toString());
  html = html.replace(/\[RISK_SCORE\]/g, data.riskScore.toString());
  html = html.replace(/\[COMPLIANCE_RATE\]/g, data.complianceRate.toString());
  html = html.replace(/\[TEST_COVERAGE\]/g, data.testCoverage.toString());
  html = html.replace(/\[INCIDENT_RATE\]/g, data.incidentRate.toString());
  html = html.replace(/\[CERTIFICATION_BODY\]/g, escapeHtml(data.certificationBody));
  html = html.replace(/\[CERTIFICATE_NUMBER\]/g, escapeHtml(data.certificateNumber));

  // Replace risk assessments table
  html = populateRiskAssessments(html, data.riskAssessments);

  // Replace compliance standards list
  html = populateComplianceStandards(html, data.complianceStandards);

  // Replace testing results table
  html = populateTestingResults(html, data.testingResults);

  return html;
}

function populateRiskAssessments(html: string, assessments: any[]): string {
  // Find the template row for risk assessments
  const rowRegex = /<tr[^>]*data-template="risk-row"[^>]*>[\s\S]*?<\/tr>/;
  const match = html.match(rowRegex);

  if (!match || assessments.length === 0) {
    return html;
  }

  const templateRow = match[0];
  const rows = assessments.map(assessment => {
    let row = templateRow;
    row = row.replace(/\[SCENARIO\]/g, escapeHtml(assessment.scenario));
    row = row.replace(/\[SEVERITY\]/g, escapeHtml(assessment.severity));
    row = row.replace(/\[LIKELIHOOD\]/g, escapeHtml(assessment.likelihood));
    row = row.replace(/\[RISK_LEVEL\]/g, escapeHtml(assessment.riskLevel));
    row = row.replace(/\[STATUS\]/g, escapeHtml(assessment.status));
    row = row.replace(/data-template="risk-row"/, '');
    return row;
  }).join('\n');

  return html.replace(rowRegex, rows);
}

function populateComplianceStandards(html: string, standards: string[]): string {
  // Find the template list item
  const itemRegex = /<li[^>]*data-template="standard-item"[^>]*>[\s\S]*?<\/li>/;
  const match = html.match(itemRegex);

  if (!match || standards.length === 0) {
    return html;
  }

  const templateItem = match[0];
  const items = standards.map(standard => {
    let item = templateItem;
    item = item.replace(/\[STANDARD\]/g, escapeHtml(standard));
    item = item.replace(/data-template="standard-item"/, '');
    return item;
  }).join('\n');

  return html.replace(itemRegex, items);
}

function populateTestingResults(html: string, results: any[]): string {
  // Find the template row for testing results
  const rowRegex = /<tr[^>]*data-template="test-row"[^>]*>[\s\S]*?<\/tr>/;
  const match = html.match(rowRegex);

  if (!match || results.length === 0) {
    return html;
  }

  const templateRow = match[0];
  const rows = results.map(result => {
    let row = templateRow;
    row = row.replace(/\[TEST_CATEGORY\]/g, escapeHtml(result.category));
    row = row.replace(/\[SCENARIOS\]/g, result.scenarios.toString());
    row = row.replace(/\[CYCLES\]/g, result.cycles.toString());
    row = row.replace(/\[PASS_RATE\]/g, result.passRate.toString());
    row = row.replace(/data-template="test-row"/, '');
    return row;
  }).join('\n');

  return html.replace(rowRegex, rows);
}

function escapeHtml(text: string): string {
  const map: Record<string, string> = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;',
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}

export function makeSelfContained(html: string): string {
  // The templates are already self-contained with inline CSS and JS
  // This function can be extended to inline any external resources if needed
  return html;
}
