import Anthropic from '@anthropic-ai/sdk';

export const getClaudeClient = () => {
  const apiKey = process.env.ANTHROPIC_API_KEY;

  if (!apiKey) {
    throw new Error('ANTHROPIC_API_KEY is not configured');
  }

  return new Anthropic({
    apiKey: apiKey,
  });
};

export async function extractSafetyCaseData(pdfText: string): Promise<any> {
  const client = getClaudeClient();

  const systemPrompt = "You are a safety case data extraction specialist. Extract all relevant safety metrics, risk assessments, compliance standards, and testing results from the provided PDF. Return ONLY valid JSON with no additional text or markdown formatting.";

  const userPrompt = `Extract all safety case data from this PDF document and return as JSON with this exact structure:
{
  "companyName": "string",
  "robotModel": "string",
  "silRating": "string",
  "operationalHours": number,
  "hazardsIdentified": number,
  "riskScore": number,
  "complianceRate": number,
  "testCoverage": number,
  "incidentRate": number,
  "certificationBody": "string",
  "certificateNumber": "string",
  "riskAssessments": [
    {
      "scenario": "string",
      "severity": "string",
      "likelihood": "string",
      "riskLevel": "string",
      "status": "string"
    }
  ],
  "complianceStandards": ["string"],
  "testingResults": [
    {
      "category": "string",
      "scenarios": number,
      "cycles": number,
      "passRate": number
    }
  ]
}

PDF Content:
${pdfText}`;

  try {
    const message = await client.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 4096,
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

    return JSON.parse(jsonMatch[0]);
  } catch (error) {
    console.error('Error extracting safety case data:', error);
    throw error;
  }
}
