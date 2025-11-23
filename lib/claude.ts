import Anthropic from '@anthropic-ai/sdk';

export const getClaudeClient = () => {
  const apiKey = process.env.ANTHROPIC_API_KEY;

  if (!apiKey) {
    throw new Error('ANTHROPIC_API_KEY is not configured');
  }

  // Create client configuration
  // Note: The Anthropic SDK does NOT support a 'proxies' parameter.
  // Proxy configuration should be done through environment variables or httpAgent if needed.
  const clientConfig: Anthropic.ClientOptions = {
    apiKey: apiKey,
  };

  return new Anthropic(clientConfig);
};

export async function extractSafetyCaseData(pdfText: string): Promise<any> {
  const client = getClaudeClient();

  const systemPrompt = `You are a comprehensive safety documentation extraction specialist. Your job is to extract ALL safety-related content from the provided PDF, not just predefined fields.

IMPORTANT PRINCIPLES:
1. Extract ONLY information that is explicitly stated in the PDF
2. If a field or section is not present in the PDF, omit it entirely from the JSON (do NOT include it with null/empty values)
3. Extract ALL sections you find, even if they're not in the example schema
4. For unknown sections, use a descriptive key name and extract the full content
5. Return ONLY valid JSON with no additional text or markdown formatting`;

  const userPrompt = `Extract all safety case data from this PDF document. Return as JSON following these guidelines:

REQUIRED FIELDS (only if present in PDF):
- companyName: Company/organization name
- robotModel: Robot model name or designation

OPTIONAL CORE METRICS (only include if found):
- silRating: Safety Integrity Level (e.g., "SIL 3")
- operationalHours: Total operational/test hours
- hazardsIdentified: Number of hazards identified
- riskScore: Overall risk score
- complianceRate: Compliance percentage
- testCoverage: Test coverage hours/percentage
- incidentRate: Incident rate percentage
- certificationBody: Certification organization name
- certificateNumber: Certificate number

OPTIONAL STRUCTURED ARRAYS (only if data exists):
- riskAssessments: Array of {scenario, severity, likelihood, riskLevel, status}
- complianceStandards: Array of standard names (e.g., ["ISO 61508", "UL 4600"])
- testingResults: Array of {category, scenarios, cycles, passRate}

OPTIONAL MAJOR SECTIONS (only if content exists):
- cybersecurity: {authentication, encryption, firmwareSecurity, intrusionDetection, vulnerabilityManagement, ...any other cyber content}
- aiMachineLearning: {trainingData, modelArchitecture, validationPerformance, adversarialRobustness, fieldMonitoring, fallbackMechanisms, ...any other AI/ML content}
- maintenanceSafety: {technicianQualifications, lotoProcedures, batteryHandling, postMaintenanceVerification, sparePartsManagement, incidentTracking, ...any other maintenance content}

ADDITIONAL SECTIONS:
- additionalSections: Object containing ANY OTHER safety-related sections you find in the PDF that don't fit above categories. Use descriptive keys like:
  - "supplyChainSecurity": {...content...}
  - "environmentalTesting": {...content...}
  - "degradedModeOperations": {...content...}
  - etc.

CRITICAL RULES:
- Do NOT include fields that aren't in the PDF
- Do NOT use placeholder or example data
- Extract complete information from each section
- If a section exists but is sparse, extract what's there
- Use the exact values from the PDF, don't interpret or modify

PDF Content:
${pdfText}`;

  try {
    const message = await client.messages.create({
      model: 'claude-sonnet-4-5-20250929',
      max_tokens: 8192, // Increased for more comprehensive extraction
      system: systemPrompt,
      messages: [
        {
          role: 'user',
          content: userPrompt,
        },
      ],
    });

    const responseText = message.content[0].type === 'text'
      ? message.content[0].text
      : '';

    // Parse the JSON response
    const jsonMatch = responseText.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('No valid JSON found in Claude response');
    }

    const extractedData = JSON.parse(jsonMatch[0]);

    // Validate that we have at minimum company name and robot model
    if (!extractedData.companyName || !extractedData.robotModel) {
      console.warn('PDF missing core required fields (companyName or robotModel)');
    }

    return extractedData;
  } catch (error) {
    console.error('Error extracting safety case data:', error);
    throw error;
  }
}
