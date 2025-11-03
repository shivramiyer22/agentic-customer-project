#!/usr/bin/env python3
"""
Generate User Training Guide PDF with latest application features.

This script generates the User-Training-Guide.pdf file with all current
features including token count and cost tracking.

Requirements:
    pip install reportlab

Usage:
    python scripts/generate_user_training_guide.py
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, black, darkblue
import os
from pathlib import Path


def create_guide():
    """Create the User Training Guide PDF."""
    
    # Output file path
    output_dir = Path(__file__).parent.parent / "frontend" / "public"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "User-Training-Guide.pdf"
    
    # Create PDF document
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Container for content
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=darkblue,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=darkblue,
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=black,
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_LEFT,
        fontName='Helvetica'
    )
    
    # Page 1: Title and Introduction
    story.append(Paragraph("THE AEROSPACE COMPANY", title_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Customer Service Agent", title_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("USER TRAINING GUIDE", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Version 1.0 | November 2025", normal_style))
    story.append(Spacer(1, 0.4*inch))
    
    story.append(Paragraph("1. INTRODUCTION", heading_style))
    story.append(Paragraph(
        "Welcome to The Aerospace Company Customer Service Agent, an advanced multi-agent "
        "AI system designed to assist internal customer service representatives in efficiently "
        "handling customer inquiries.",
        normal_style
    ))
    story.append(Paragraph(
        "This system uses specialized AI agents to route queries to the appropriate knowledge "
        "domain: Billing, Technical Support, or Policy & Compliance.",
        normal_style
    ))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("2. SYSTEM ARCHITECTURE", heading_style))
    story.append(Paragraph(
        "The system employs a supervisor-worker pattern with four core agents:",
        normal_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("2.1 Supervisor Agent", subheading_style))
    story.append(Paragraph("• Powered by AWS Bedrock Claude 3 Haiku", normal_style))
    story.append(Paragraph("• Analyzes queries and routes to appropriate worker agents", normal_style))
    story.append(Paragraph("• Detects emergency situations and escalates", normal_style))
    story.append(Paragraph("• Synthesizes responses from multiple agents", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("2.2 Policy & Compliance Agent", subheading_style))
    story.append(Paragraph("• Handles FAA/EASA regulations and company policies", normal_style))
    story.append(Paragraph("• Uses Pure CAG (Cached Augmented Generation)", normal_style))
    story.append(Paragraph("• Fast, consistent responses from static policy documents", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("2.3 Technical Support Agent", subheading_style))
    story.append(Paragraph("• Handles technical documentation and bug reports", normal_style))
    story.append(Paragraph("• Uses Pure RAG (Retrieval Augmented Generation)", normal_style))
    story.append(Paragraph("• Dynamic knowledge base retrieval", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("2.4 Billing Support Agent", subheading_style))
    story.append(Paragraph("• Handles invoices, pricing, and contracts", normal_style))
    story.append(Paragraph("• Uses Hybrid RAG/CAG strategy", normal_style))
    story.append(Paragraph("• Combines dynamic billing data with cached policy info", normal_style))
    
    story.append(PageBreak())
    
    # Page 2: Getting Started and Chat Interface
    story.append(Paragraph("3. GETTING STARTED", heading_style))
    story.append(Paragraph(
        "The application has two main pages accessible via the top navigation:",
        normal_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("3.1 Chat Page (Main Interface)", subheading_style))
    story.append(Paragraph("• Type customer queries in the input box at the bottom", normal_style))
    story.append(Paragraph("• Press Enter to send (Shift+Enter for new line)", normal_style))
    story.append(Paragraph("• AI responds in real-time with streaming", normal_style))
    story.append(Paragraph("• View conversation history in the main area", normal_style))
    story.append(Paragraph("• See which agents contributed to each response", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("3.2 Upload Documents Page", subheading_style))
    story.append(Paragraph("• Upload PDF, TXT, Markdown, or JSON files", normal_style))
    story.append(Paragraph("• Maximum file size: 20 MB per file", normal_style))
    story.append(Paragraph("• Choose target knowledge base or use Auto-Map", normal_style))
    story.append(Paragraph("• Track upload progress in real-time", normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("4. USING THE CHAT INTERFACE", heading_style))
    
    story.append(Paragraph("4.1 Sending Messages", subheading_style))
    story.append(Paragraph("1. Type your query in the text box at the bottom", normal_style))
    story.append(Paragraph("2. Press Enter to send (or click the Send button)", normal_style))
    story.append(Paragraph("3. AI will process and respond in real-time", normal_style))
    story.append(Paragraph("4. Character count displays below the input box", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("4.2 Understanding Responses", subheading_style))
    story.append(Paragraph("Each AI response includes:", normal_style))
    story.append(Paragraph("• Main answer content", normal_style))
    story.append(Paragraph("• Contributing Agent Calls: Which worker agents were invoked", normal_style))
    story.append(Paragraph("• Contributing Model Calls: Which AI models processed the query", normal_style))
    story.append(Paragraph("• Source citations: References to knowledge base documents", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("4.3 Token Count and Cost Tracking", subheading_style))
    story.append(Paragraph(
        "The system tracks token usage and calculates costs in real-time for each chat session:",
        normal_style
    ))
    story.append(Paragraph("• Token count for this chat: Cumulative total of input and output tokens", normal_style))
    story.append(Paragraph("• Breakdown shows input tokens (in:) and output tokens (out:)", normal_style))
    story.append(Paragraph("• Total cost for this chat: Calculated cost in dollars", normal_style))
    story.append(Paragraph("• Cost breakdown shows input cost and output cost separately", normal_style))
    story.append(Paragraph("• Pricing based on Claude 3 Haiku (AWS Bedrock):", normal_style))
    story.append(Paragraph("  - Input: $0.00025 per 1,000 tokens", normal_style))
    story.append(Paragraph("  - Output: $0.00125 per 1,000 tokens", normal_style))
    story.append(Paragraph("• Hover over the info icon (?) to see detailed breakdown", normal_style))
    story.append(Paragraph("• Token count and cost reset to 0 when starting a new chat", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("4.4 Starting New Conversations", subheading_style))
    story.append(Paragraph("• Click the \"New Chat\" button (icon with lines and arrow)", normal_style))
    story.append(Paragraph("• Conversation history persists across page navigation", normal_style))
    story.append(Paragraph("• Token count and cost reset to 0 for new chat", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("4.5 Providing Feedback", subheading_style))
    story.append(Paragraph("After each AI response:", normal_style))
    story.append(Paragraph("1. Rate with thumbs up or thumbs down", normal_style))
    story.append(Paragraph("2. Optionally add detailed feedback comments", normal_style))
    story.append(Paragraph("3. Click Submit to record your feedback", normal_style))
    
    story.append(PageBreak())
    
    # Page 3: Query Examples and Uploading Documents
    story.append(Paragraph("5. QUERY EXAMPLES", heading_style))
    story.append(Paragraph(
        "The system can handle single or multi-part queries:",
        normal_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("5.1 Billing Queries", subheading_style))
    story.append(Paragraph("• \"What is the highest valued invoice amount?\"", normal_style))
    story.append(Paragraph("• \"Show me the billing policy for aerospace contracts\"", normal_style))
    story.append(Paragraph("• \"What are the payment terms for enterprise customers?\"", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("5.2 Technical Support Queries", subheading_style))
    story.append(Paragraph("• \"How many high priority bugs were resolved this year?\"", normal_style))
    story.append(Paragraph("• \"What is the troubleshooting guide for system failures?\"", normal_style))
    story.append(Paragraph("• \"Show me the technical specifications for component X\"", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("5.3 Policy & Compliance Queries", subheading_style))
    story.append(Paragraph("• \"What is the SLA for high priority issues?\"", normal_style))
    story.append(Paragraph("• \"What are the FAA regulations for aerospace components?\"", normal_style))
    story.append(Paragraph("• \"What is the data archival policy?\"", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("5.4 Multi-Domain Queries", subheading_style))
    story.append(Paragraph("The system can handle queries spanning multiple domains:", normal_style))
    story.append(Paragraph("• \"How many bugs were resolved and what is the SLA policy?\"", normal_style))
    story.append(Paragraph("• \"How many critical priority bugs were resolved this year and what percentage were compliant to SLA levels per our technical support policy?\"", normal_style))
    story.append(Paragraph(
        "The supervisor will call multiple agents and synthesize responses.",
        normal_style
    ))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("6. UPLOADING DOCUMENTS", heading_style))
    
    story.append(Paragraph("6.1 Supported File Types", subheading_style))
    story.append(Paragraph("• PDF documents (.pdf)", normal_style))
    story.append(Paragraph("• Text files (.txt)", normal_style))
    story.append(Paragraph("• Markdown files (.md)", normal_style))
    story.append(Paragraph("• JSON files (.json)", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("6.2 Upload Process", subheading_style))
    story.append(Paragraph("1. Navigate to \"Upload Documents\" page", normal_style))
    story.append(Paragraph("2. Select knowledge base:", normal_style))
    story.append(Paragraph("   • Billing Knowledge Base", normal_style))
    story.append(Paragraph("   • Technical Knowledge Base", normal_style))
    story.append(Paragraph("   • Policy Knowledge Base", normal_style))
    story.append(Paragraph("   • Auto-Map (system determines best fit)", normal_style))
    story.append(Paragraph("3. Drag and drop files or click to browse", normal_style))
    story.append(Paragraph("4. Review file list and remove any unwanted files", normal_style))
    story.append(Paragraph("5. Click \"Upload\" to begin processing", normal_style))
    story.append(Paragraph("6. Monitor progress in real-time", normal_style))
    
    story.append(PageBreak())
    
    # Page 4: Best Practices, Emergency, Troubleshooting, Support
    story.append(Paragraph("7. BEST PRACTICES", heading_style))
    
    story.append(Paragraph("7.1 Writing Effective Queries", subheading_style))
    story.append(Paragraph("• Be specific and clear in your questions", normal_style))
    story.append(Paragraph("• Include relevant context (dates, IDs, categories)", normal_style))
    story.append(Paragraph("• Break complex questions into parts if needed", normal_style))
    story.append(Paragraph("• The system can handle multi-part queries automatically", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("7.2 Document Organization", subheading_style))
    story.append(Paragraph("• Upload documents to the correct knowledge base", normal_style))
    story.append(Paragraph("• Use Auto-Map when unsure of classification", normal_style))
    story.append(Paragraph("• Keep file names descriptive", normal_style))
    story.append(Paragraph("• Ensure documents are up-to-date", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("7.3 Interpreting Results", subheading_style))
    story.append(Paragraph("• Check Contributing Agent Calls to understand response sources", normal_style))
    story.append(Paragraph("• Review source citations for verification", normal_style))
    story.append(Paragraph("• Multiple agents indicate multi-domain queries", normal_style))
    story.append(Paragraph("• AI models shown help understand processing approach", normal_style))
    story.append(Paragraph("• Monitor token count and cost to track usage", normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("8. EMERGENCY ESCALATION", heading_style))
    story.append(Paragraph(
        "The system automatically detects safety-critical queries containing:",
        normal_style
    ))
    story.append(Paragraph("• Emergency keywords (emergency, critical, urgent, hazard)", normal_style))
    story.append(Paragraph("• Safety concerns (accident, incident, failure)", normal_style))
    story.append(Paragraph("• Aircraft issues (grounded, system failure, malfunction)", normal_style))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("When detected, the system:", normal_style))
    story.append(Paragraph("1. Immediately flags the query as high priority", normal_style))
    story.append(Paragraph("2. Provides escalation contact information", normal_style))
    story.append(Paragraph("3. Routes to emergency response team", normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("9. TROUBLESHOOTING", heading_style))
    
    story.append(Paragraph("Common Issues:", subheading_style))
    story.append(Paragraph("• Response taking too long: Check internet connection", normal_style))
    story.append(Paragraph("• Upload failed: Verify file size (max 20 MB)", normal_style))
    story.append(Paragraph("• Chat history lost: Clear browser cache and reload", normal_style))
    story.append(Paragraph("• No response received: Refresh page and try again", normal_style))
    story.append(Paragraph("• Token count not updating: Check that responses are completing", normal_style))
    story.append(Paragraph("• Cost calculation incorrect: Verify pricing constants are current", normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("10. SUPPORT & CONTACT", heading_style))
    story.append(Paragraph("For technical support or questions:", normal_style))
    story.append(Paragraph("Emergency Escalation: ski@aerospace-co.com", normal_style))
    story.append(Paragraph("System Version: 1.0.0", normal_style))
    story.append(Paragraph("Last Updated: November 2025", normal_style))
    
    # Build PDF
    doc.build(story)
    
    print(f"✅ User Training Guide PDF generated successfully at: {output_path}")
    print(f"   File size: {output_path.stat().st_size / 1024:.2f} KB")


if __name__ == "__main__":
    create_guide()

