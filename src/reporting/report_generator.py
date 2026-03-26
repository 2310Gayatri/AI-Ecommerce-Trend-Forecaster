from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
import os
import json
import shutil

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

INPUT_PATH = os.path.join(BASE_DIR, "data", "output", "market_dashboard_data.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "output", "market_report.pdf")
FRONTEND_PUBLIC_PATH = os.path.join(BASE_DIR, "frontend", "public", "market_report.pdf")


def clean_text(text):
    if text is None:
        return ""
    
    if isinstance(text, (tuple, list)):
        if isinstance(text, tuple): text = text[0]
        text = " ".join([str(t) for t in text])

    text = str(text)
    
    # Escape basic XML chars for ReportLab Paragraph
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    # Convert markdown-like bold (**) to <b>
    parts = text.split("**")
    new_text = ""
    for i, part in enumerate(parts):
        new_text += part
        if i < len(parts) - 1:
            new_text += "<b>" if i % 2 == 0 else "</b>"
    if (len(parts) - 1) % 2 != 0:
        new_text += "</b>"
        
    text = new_text.replace("\n", "<br/>")
    return text


def generate_pdf_report():
    print("🚀 Starting PDF generation (High-Stability Mode)...")
    if not os.path.exists(INPUT_PATH):
        print(f"❌ Dashboard data not found: {INPUT_PATH}")
        return

    try:
        with open(INPUT_PATH, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load JSON data: {e}")
        return

    try:
        # Build document once
        doc = SimpleDocTemplate(OUTPUT_PATH, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
        styles = getSampleStyleSheet()
        
        header_style = ParagraphStyle(
            name='HeaderStyle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#2563eb'),
            spaceAfter=10
        )

        elements = []

        # Title
        elements.append(Paragraph("<b><font size=18 color='#1e293b'>AI Market Intelligence Report</font></b>", styles["Title"]))
        elements.append(Paragraph(f"<font size=10 color='#64748b'>Report Cycle: {data.get('last_updated', 'Latest Analysis')}</font>", styles["Normal"]))
        elements.append(Spacer(1, 24))

        # Highlights
        elements.append(Paragraph("Executive Summary", header_style))
        overview = data.get("market_overview", {})
        elements.append(Paragraph(f"Trend Direction: <b>{overview.get('trend_direction', 'STABLE')}</b>", styles["Normal"]))
        elements.append(Paragraph(f"Aggregate Market Sentiment: {overview.get('current_sentiment', 0.5):.4f}", styles["Normal"]))
        elements.append(Paragraph(f"Volatility Index: {overview.get('volatility', 0):.2f}", styles["Normal"]))
        elements.append(Spacer(1, 16))

        # AI Insights
        elements.append(Paragraph("AI Market Narrative", header_style))
        elements.append(Paragraph(clean_text(data.get("ai_insight", "AI market story under analysis.")), styles["Normal"]))
        elements.append(Spacer(1, 16))

        # Competitive Landscape
        elements.append(Paragraph("Competitive Intelligence", header_style))
        elements.append(Paragraph(clean_text(data.get("brand_ai_insight", "Individual brand performance analysis pending.")), styles["Normal"]))
        elements.append(Spacer(1, 16))

        # Risk Analysis
        elements.append(Paragraph("Risk Factors", header_style))
        elements.append(Paragraph(clean_text(data.get("risk_signals", "No critical risk threats currently identified.")), styles["Normal"]))
        elements.append(Spacer(1, 16))

        # Alerts
        alerts = data.get("alerts", [])
        if alerts:
            elements.append(Paragraph("Market Alerts & Signals", header_style))
            for alert in alerts[:10]:
                elements.append(Paragraph(f"• <b>[{alert.get('severity')}]</b> {alert.get('message')} ({alert.get('brand', 'MARKET')})", styles["Normal"]))

        # BUILD THE PDF
        doc.build(elements)
        print(f"✅ Backend PDF Generated: {OUTPUT_PATH}")

        # SYNC TO FRONTEND DIRECTLY to avoid watcher race conditions on Windows
        if os.path.exists(os.path.dirname(FRONTEND_PUBLIC_PATH)):
            try:
                shutil.copy2(OUTPUT_PATH, FRONTEND_PUBLIC_PATH)
                print(f"✅ Synced to Frontend: {FRONTEND_PUBLIC_PATH}")
            except Exception as e:
                print(f"⚠️ Direct frontend sync failed: {e}")

    except Exception as e:
        print(f"❌ PDF Generation CRASHED: {e}")


if __name__ == "__main__":
    generate_pdf_report()