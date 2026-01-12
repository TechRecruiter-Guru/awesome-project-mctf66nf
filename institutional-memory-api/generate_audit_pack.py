"""
Generate Sample Audit Pack PDF - Defensible Hiring AI
Professional PDF generation for sample compliance documentation
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os

def generate_custom_audit_pack_pdf(company_name, ai_tools, jurisdiction, num_hires, industry="Technology"):
    """Generate a custom audit pack PDF with user-provided parameters"""

    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create unique filename based on timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    pdf_filename = f'demo-audit-pack-{timestamp}.pdf'
    pdf_path = os.path.join(script_dir, 'static', pdf_filename)

    # Create static directory if it doesn't exist
    os.makedirs(os.path.join(script_dir, 'static'), exist_ok=True)

    # Create PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CenterHeading', parent=styles['Heading1'], alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Subheading', parent=styles['Heading2'], textColor=colors.HexColor('#667eea')))

    # Title Page
    elements.append(Spacer(1, 1*inch))

    title = Paragraph(f"<b>DEMO AUDIT PACK</b>", styles['CenterHeading'])
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))

    subtitle = Paragraph(f"{jurisdiction} AI Hiring Compliance Documentation", styles['CenterHeading'])
    elements.append(subtitle)
    elements.append(Spacer(1, 0.5*inch))

    # Metadata
    metadata = [
        ["<b>Generated:</b>", datetime.now().strftime("%B %d, %Y at %H:%M UTC")],
        ["<b>Company:</b>", company_name],
        ["<b>Industry:</b>", industry],
        ["<b>Request ID:</b>", f"demo-{timestamp}"],
        ["<b>Sample Hires:</b>", str(num_hires)],
        ["<b>Jurisdiction:</b>", jurisdiction],
        ["<b>Status:</b>", "<b>⚠️ DEMO - Sample Data Only</b>"]
    ]

    metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
    metadata_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(metadata_table)
    elements.append(Spacer(1, 0.5*inch))

    # Important Demo Notice
    demo_notice = """<b>⚠️ IMPORTANT: THIS IS A DEMO USING SAMPLE DATA</b><br/><br/>
    This audit pack demonstrates the format and completeness of documentation you would receive
    with live ATS integration. In production, all data is automatically captured from your
    actual hiring decisions—no manual entry required.<br/><br/>
    <b>Production version captures:</b> Real timestamps, actual candidate IDs, live hiring decisions,
    automated disclosures, and real-time compliance tracking."""

    elements.append(Paragraph(demo_notice, styles['BodyText']))
    elements.append(Spacer(1, 0.3*inch))

    # AI Systems Registered
    ai_systems_heading = Paragraph("<b>📊 AI SYSTEMS IN USE</b>", styles['Subheading'])
    elements.append(ai_systems_heading)
    elements.append(Spacer(1, 0.2*inch))

    # Build AI systems table from selected tools
    ai_systems_data = [['<b>AI System</b>', '<b>Vendor</b>', '<b>Type</b>', '<b>Status</b>']]

    tool_mapping = {
        'greenhouse': ['Resume Screening AI', 'Greenhouse', 'Resume Screening', '✅ Active'],
        'hirevue': ['Video Interview Analyzer', 'HireVue', 'Video Analysis', '✅ Active'],
        'criteria': ['Skill Assessment Engine', 'Criteria Corp', 'Assessment', '✅ Active'],
        'lever': ['ATS Integration', 'Lever', 'Full ATS', '✅ Active'],
        'workday': ['Recruiting Platform', 'Workday', 'Full ATS', '✅ Active'],
        'bamboohr': ['Applicant Tracking', 'BambooHR', 'ATS', '✅ Active'],
    }

    for tool in ai_tools:
        if tool.lower() in tool_mapping:
            ai_systems_data.append(tool_mapping[tool.lower()])

    ai_systems_table = Table(ai_systems_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    ai_systems_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    elements.append(ai_systems_table)
    elements.append(Spacer(1, 0.3*inch))

    # Sample decisions based on num_hires
    decisions_heading = Paragraph("<b>📋 SAMPLE HIRING DECISIONS</b>", styles['Subheading'])
    elements.append(decisions_heading)
    elements.append(Spacer(1, 0.1*inch))

    decisions_subtitle = Paragraph(f"<i>Sample - Showing 5 of {num_hires} hiring decisions</i>", styles['BodyText'])
    elements.append(decisions_subtitle)
    elements.append(Spacer(1, 0.2*inch))

    # Generate sample decisions
    sample_decisions = [
        {
            'role': 'Software Engineer',
            'decision': 'REJECTED',
            'ai_score': 42,
            'human_override': 'NO',
            'justification': 'Resume did not meet minimum qualifications'
        },
        {
            'role': 'Product Manager',
            'decision': 'ADVANCED',
            'ai_score': 78,
            'human_override': 'NO',
            'justification': 'Strong interview performance'
        },
        {
            'role': 'Data Analyst',
            'decision': 'HIRED',
            'ai_score': 89,
            'human_override': 'NO',
            'justification': 'Excellent technical fit'
        },
        {
            'role': 'UX Designer',
            'decision': 'ADVANCED',
            'ai_score': 58,
            'human_override': 'YES',
            'justification': 'Portfolio demonstrated exceptional skills despite low AI score due to resume formatting'
        },
        {
            'role': 'Sales Representative',
            'decision': 'REJECTED',
            'ai_score': 51,
            'human_override': 'NO',
            'justification': 'Confirmed via human review'
        }
    ]

    for i, decision in enumerate(sample_decisions[:5], 1):
        decision_text = f"""<b>Decision #{i}</b><br/>
        <b>Timestamp:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}<br/>
        <b>Candidate ID:</b> hash-demo{i:04d} (SHA-256 hashed)<br/>
        <b>Role:</b> {decision['role']}<br/>
        <b>Decision:</b> {decision['decision']}<br/>
        <b>AI Score:</b> {decision['ai_score']}/100<br/>
        <b>Human Override:</b> {decision['human_override']}<br/>
        <b>Disclosure Sent:</b> ✅ Yes<br/>
        <b>Final Justification:</b> {decision['justification']}"""
        elements.append(Paragraph(decision_text, styles['BodyText']))
        elements.append(Spacer(1, 0.25*inch))

    elements.append(PageBreak())

    # Compliance Checklist
    checklist_heading = Paragraph("<b>✅ COMPLIANCE CHECKLIST</b>", styles['Subheading'])
    elements.append(checklist_heading)
    elements.append(Spacer(1, 0.2*inch))

    checklist = f"""☑ All AI systems registered with deployment dates<br/>
    ☑ Bias audits conducted annually by third party<br/>
    ☑ Bias audit results posted publicly<br/>
    ☑ Disclosures sent to 100% of candidates ({num_hires}/{num_hires})<br/>
    ☑ All hiring decisions logged with timestamps<br/>
    ☑ Human decision maker identified for each decision<br/>
    ☑ AI recommendations vs. final decisions tracked<br/>
    ☑ Human override justifications documented<br/>
    ☑ 7-year retention policy implemented<br/>
    ☑ Data security (AES-256 encryption)<br/>
    ☑ Audit pack generation capability functional<br/><br/>
    <b>DEMO STATUS: ✅ Format matches production court-ready documentation</b>"""
    elements.append(Paragraph(checklist, styles['BodyText']))

    elements.append(Spacer(1, 0.5*inch))

    # Footer
    footer = Paragraph(f"<i>Generated in 60 seconds for {company_name}</i>",
                      ParagraphStyle(name='Footer', parent=styles['BodyText'], alignment=TA_CENTER))
    elements.append(footer)
    elements.append(Spacer(1, 0.2*inch))

    cta = Paragraph("<b>Ready for live integration?</b><br/>Visit defensiblehiringai.com/request-demo",
                   ParagraphStyle(name='CTA', parent=styles['BodyText'], alignment=TA_CENTER))
    elements.append(cta)

    # Build PDF
    doc.build(elements)

    return pdf_path, pdf_filename


def generate_sample_audit_pack_pdf():
    """Generate a professional sample audit pack PDF"""

    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(script_dir, 'static', 'sample-audit-pack.pdf')

    # Create static directory if it doesn't exist
    os.makedirs(os.path.join(script_dir, 'static'), exist_ok=True)

    # Create PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CenterHeading', parent=styles['Heading1'], alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Subheading', parent=styles['Heading2'], textColor=colors.HexColor('#667eea')))

    # Title Page
    elements.append(Spacer(1, 1*inch))

    title = Paragraph("<b>SAMPLE AUDIT PACK</b>", styles['CenterHeading'])
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))

    subtitle = Paragraph("NYC Local Law 144 Compliance Documentation", styles['CenterHeading'])
    elements.append(subtitle)
    elements.append(Spacer(1, 0.5*inch))

    # Metadata
    metadata = [
        ["<b>Generated:</b>", "January 9, 2026 at 14:32 UTC"],
        ["<b>Company:</b>", "Acme Corporation (REDACTED)"],
        ["<b>Request ID:</b>", "audit-pack-20260109-1432"],
        ["<b>Audit Period:</b>", "January 1, 2025 - December 31, 2025"],
        ["<b>Compliance Status:</b>", "<b>✅ COMPLIANT</b>"]
    ]

    metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
    metadata_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(metadata_table)
    elements.append(Spacer(1, 0.5*inch))

    # Executive Summary
    exec_summary = Paragraph("<b>⚖️ EXECUTIVE SUMMARY</b>", styles['Subheading'])
    elements.append(exec_summary)
    elements.append(Spacer(1, 0.2*inch))

    summary_text = """This audit pack provides complete documentation of AI hiring system usage and
    decision-making processes for Acme Corporation during the audit period specified above.
    All records are <b>immutable, timestamped, and cryptographically signed</b> to ensure authenticity
    and prevent tampering."""
    elements.append(Paragraph(summary_text, styles['BodyText']))
    elements.append(Spacer(1, 0.3*inch))

    # AI Systems Registered
    ai_systems_heading = Paragraph("<b>📊 AI SYSTEMS REGISTERED</b>", styles['Subheading'])
    elements.append(ai_systems_heading)
    elements.append(Spacer(1, 0.2*inch))

    ai_systems_data = [
        ['<b>AI System</b>', '<b>Vendor</b>', '<b>Type</b>', '<b>Deployed</b>'],
        ['Resume Screening AI', 'Greenhouse', 'Resume Screening', '2024-03-15'],
        ['Video Interview Analyzer', 'HireVue', 'Video Analysis', '2024-06-01'],
        ['Skill Assessment Engine', 'Criteria Corp', 'Assessment', '2023-11-20']
    ]

    ai_systems_table = Table(ai_systems_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    ai_systems_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    elements.append(ai_systems_table)
    elements.append(Spacer(1, 0.2*inch))

    bias_audit_text = """<b>Bias Audit Status:</b><br/>
    • Resume Screening AI: Last audited 2025-10-15 (Pass - No disparate impact detected)<br/>
    • Video Interview Analyzer: Last audited 2025-09-22 (Pass - Within acceptable variance)<br/>
    • Skill Assessment Engine: Last audited 2025-11-30 (Pass - EEOC compliant)<br/><br/>
    <b>Public Disclosure:</b> ✅ Posted at acmecorp.com/ai-hiring-disclosure"""
    elements.append(Paragraph(bias_audit_text, styles['BodyText']))

    elements.append(PageBreak())

    # Hiring Decisions Log
    decisions_heading = Paragraph("<b>📋 HIRING DECISIONS LOG</b>", styles['Subheading'])
    elements.append(decisions_heading)
    elements.append(Spacer(1, 0.1*inch))

    decisions_subtitle = Paragraph("<i>Sample - 5 of 1,247 records</i>", styles['BodyText'])
    elements.append(decisions_subtitle)
    elements.append(Spacer(1, 0.2*inch))

    # Decision #1
    decision1 = f"""<b>Decision #1</b><br/>
    <b>Timestamp:</b> 2025-03-15 09:23:41 UTC<br/>
    <b>Candidate ID:</b> hash-a1b2c3d4 (SHA-256 hashed for privacy)<br/>
    <b>Role:</b> Software Engineer - Backend<br/>
    <b>Decision:</b> REJECTED<br/>
    <b>AI Systems Used:</b> Resume Screening AI<br/>
    <b>Human Decision Maker:</b> John D., Engineering Manager<br/>
    <b>Disclosure Sent:</b> ✅ 2025-03-10 14:22:01 UTC<br/>
    <b>AI Recommendation:</b> REJECT (Score: 42/100 - Below threshold)<br/>
    <b>Human Override:</b> NO<br/>
    <b>Final Decision:</b> REJECTED - Resume did not meet minimum qualifications"""
    elements.append(Paragraph(decision1, styles['BodyText']))
    elements.append(Spacer(1, 0.3*inch))

    # Decision #2
    decision2 = f"""<b>Decision #2</b><br/>
    <b>Timestamp:</b> 2025-04-22 16:45:12 UTC<br/>
    <b>Candidate ID:</b> hash-e5f6g7h8<br/>
    <b>Role:</b> Product Manager<br/>
    <b>Decision:</b> ADVANCED TO INTERVIEW<br/>
    <b>AI Systems Used:</b> Video Interview Analyzer<br/>
    <b>Human Decision Maker:</b> Sarah K., Product Director<br/>
    <b>Disclosure Sent:</b> ✅ 2025-04-18 10:15:33 UTC<br/>
    <b>AI Recommendation:</b> ADVANCE (Score: 78/100 - Strong communication)<br/>
    <b>Human Override:</b> NO<br/>
    <b>Final Decision:</b> ADVANCED - Strong video interview performance"""
    elements.append(Paragraph(decision2, styles['BodyText']))
    elements.append(Spacer(1, 0.3*inch))

    # Decision #3
    decision3 = f"""<b>Decision #3</b><br/>
    <b>Timestamp:</b> 2025-07-08 11:12:05 UTC<br/>
    <b>Candidate ID:</b> hash-i9j0k1l2<br/>
    <b>Role:</b> Data Analyst<br/>
    <b>Decision:</b> HIRED<br/>
    <b>AI Systems Used:</b> Resume Screening AI, Skill Assessment Engine<br/>
    <b>Human Decision Maker:</b> Michael R., Analytics Lead<br/>
    <b>Disclosure Sent:</b> ✅ 2025-06-30 08:44:19 UTC<br/>
    <b>AI Recommendation:</b> HIRE (Resume: 89/100, Skills: 92/100)<br/>
    <b>Human Override:</b> NO<br/>
    <b>Final Decision:</b> HIRED - Excellent technical fit"""
    elements.append(Paragraph(decision3, styles['BodyText']))
    elements.append(Spacer(1, 0.3*inch))

    # Decision #4 - Human Override Example
    decision4 = f"""<b>Decision #4 (Human Override Example)</b><br/>
    <b>Timestamp:</b> 2025-09-14 13:28:47 UTC<br/>
    <b>Candidate ID:</b> hash-m3n4o5p6<br/>
    <b>Role:</b> UX Designer<br/>
    <b>Decision:</b> ADVANCED TO INTERVIEW<br/>
    <b>AI Systems Used:</b> Resume Screening AI<br/>
    <b>Human Decision Maker:</b> Lisa T., Design Manager<br/>
    <b>Disclosure Sent:</b> ✅ 2025-09-10 09:12:44 UTC<br/>
    <b>AI Recommendation:</b> REJECT (Score: 58/100 - Below threshold)<br/>
    <b>Human Override:</b> ✅ YES<br/>
    <b>Override Justification:</b> "Candidate's portfolio shows 5+ years of enterprise UX work.
    AI scored low due to resume formatting, not actual qualifications. Advancing to interview."<br/>
    <b>Final Decision:</b> ADVANCED - Portfolio demonstrated exceptional skills"""
    elements.append(Paragraph(decision4, styles['BodyText']))
    elements.append(Spacer(1, 0.3*inch))

    # Decision #5
    decision5 = f"""<b>Decision #5</b><br/>
    <b>Timestamp:</b> 2025-11-02 10:05:33 UTC<br/>
    <b>Candidate ID:</b> hash-q7r8s9t0<br/>
    <b>Role:</b> Sales Representative<br/>
    <b>Decision:</b> REJECTED<br/>
    <b>AI Systems Used:</b> Video Interview Analyzer<br/>
    <b>Human Decision Maker:</b> David L., Sales Director<br/>
    <b>Disclosure Sent:</b> ✅ 2025-10-28 14:33:21 UTC<br/>
    <b>AI Recommendation:</b> REJECT (Score: 51/100 - Low enthusiasm detected)<br/>
    <b>Human Override:</b> NO<br/>
    <b>Final Decision:</b> REJECTED - Confirmed via human review"""
    elements.append(Paragraph(decision5, styles['BodyText']))

    elements.append(PageBreak())

    # Bias Audit Summary
    bias_heading = Paragraph("<b>🔍 BIAS AUDIT SUMMARY</b>", styles['Subheading'])
    elements.append(bias_heading)
    elements.append(Spacer(1, 0.2*inch))

    bias_info = """<b>Auditor:</b> Third-Party Compliance Group LLC<br/>
    <b>Audit Date:</b> December 1, 2025<br/>
    <b>Audit Method:</b> Impact Ratio Analysis per NYC DCWP Guidelines"""
    elements.append(Paragraph(bias_info, styles['BodyText']))
    elements.append(Spacer(1, 0.2*inch))

    bias_results_data = [
        ['<b>Protected Category</b>', '<b>Selection Rate Variance</b>', '<b>Result</b>'],
        ['Race/Ethnicity', '2.1%', '✅ PASS'],
        ['Gender', '1.8%', '✅ PASS'],
        ['Age (40+)', '3.2%', '✅ PASS']
    ]

    bias_table = Table(bias_results_data, colWidths=[2*inch, 2*inch, 2*inch])
    bias_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    elements.append(bias_table)
    elements.append(Spacer(1, 0.2*inch))

    conclusion = Paragraph("<b>Conclusion:</b> ✅ ALL AI SYSTEMS COMPLIANT with NYC Local Law 144", styles['BodyText'])
    elements.append(conclusion)
    elements.append(Spacer(1, 0.4*inch))

    # Compliance Checklist
    checklist_heading = Paragraph("<b>✅ COMPLIANCE CHECKLIST</b>", styles['Subheading'])
    elements.append(checklist_heading)
    elements.append(Spacer(1, 0.2*inch))

    checklist = """☑ All AI systems registered with deployment dates<br/>
    ☑ Bias audits conducted annually by third party<br/>
    ☑ Bias audit results posted publicly<br/>
    ☑ Disclosures sent to 100% of candidates (1,247/1,247)<br/>
    ☑ All hiring decisions logged with timestamps<br/>
    ☑ Human decision maker identified for each decision<br/>
    ☑ AI recommendations vs. final decisions tracked<br/>
    ☑ Human override justifications documented<br/>
    ☑ 7-year retention policy implemented<br/>
    ☑ Data security measures in place (AES-256 encryption)<br/>
    ☑ Audit pack generation capability tested and functional<br/><br/>
    <b>COMPLIANCE STATUS: ✅ FULLY COMPLIANT</b>"""
    elements.append(Paragraph(checklist, styles['BodyText']))

    elements.append(PageBreak())

    # Contact & Verification
    contact_heading = Paragraph("<b>📞 CONTACT INFORMATION</b>", styles['Subheading'])
    elements.append(contact_heading)
    elements.append(Spacer(1, 0.2*inch))

    contact_info = """<b>Generated by:</b> Defensible Hiring AI<br/>
    <b>Platform:</b> defensiblehiringai.com<br/>
    <b>Support:</b> support@defensiblehiringai.com<br/><br/>
    <b>Company Contact:</b><br/>
    Acme Corporation - Legal Department<br/>
    legal@acmecorp.com | (555) 123-4567"""
    elements.append(Paragraph(contact_info, styles['BodyText']))
    elements.append(Spacer(1, 0.4*inch))

    # Authenticity Verification
    verify_heading = Paragraph("<b>🔐 AUTHENTICITY VERIFICATION</b>", styles['Subheading'])
    elements.append(verify_heading)
    elements.append(Spacer(1, 0.2*inch))

    verify_info = """<b>Document Hash:</b> SHA-256: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6<br/>
    <b>Digital Signature:</b> RSA-2048 signed by Defensible Hiring AI<br/>
    <b>Verification:</b> Visit defensiblehiringai.com/verify<br/><br/>
    <b>This audit pack is admissible as evidence in legal proceedings.</b>"""
    elements.append(Paragraph(verify_info, styles['BodyText']))
    elements.append(Spacer(1, 0.5*inch))

    # Footer
    footer = Paragraph("<i>Generated in 47 seconds via Defensible Hiring AI API</i>",
                      ParagraphStyle(name='Footer', parent=styles['BodyText'], alignment=TA_CENTER))
    elements.append(footer)
    elements.append(Spacer(1, 0.2*inch))

    cta = Paragraph("<b>Need your own instant audit pack?</b><br/>Visit defensiblehiringai.com",
                   ParagraphStyle(name='CTA', parent=styles['BodyText'], alignment=TA_CENTER))
    elements.append(cta)

    # Build PDF
    doc.build(elements)

    return pdf_path

if __name__ == "__main__":
    pdf_path = generate_sample_audit_pack_pdf()
    print(f"✅ Sample audit pack PDF generated: {pdf_path}")
