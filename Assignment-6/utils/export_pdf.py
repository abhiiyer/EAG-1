from fpdf import FPDF
import os
from datetime import datetime

class RMReport(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 14)
        self.cell(0, 10, "RM Assist - Customer Summary Report", ln=True, align="C")
        self.ln(8)

    def section(self, title):
        self.set_font("DejaVu", "B", 12)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, title, ln=True)
        self.set_text_color(0, 0, 0)

    def body_text(self, label, text):
        self.set_font("DejaVu", "", 11)
        self.multi_cell(0, 8, f"{label}: {text}")
        self.ln(1)

    def txn_table(self, transactions):
        self.set_font("DejaVu", "B", 11)
        self.cell(50, 8, "Date", 1)
        self.cell(90, 8, "Description", 1)
        self.cell(40, 8, "Amount (AED)", 1, ln=1)
        self.set_font("DejaVu", "", 11)
        for txn in transactions:
            self.cell(50, 8, txn['date'], 1)
            self.cell(90, 8, txn['description'], 1)
            self.cell(40, 8, str(txn['amount']), 1, ln=1)

def generate_pdf(rm_name, customer, decision, intent_score=75, pitch_text="Pitch pending"):
    export_dir = "pdf_exports"
    os.makedirs(export_dir, exist_ok=True)
    today = datetime.today().strftime("%Y%m%d")
    filename = f"{rm_name}_{customer.name}_{today}.pdf".replace(" ", "_")
    filepath = os.path.join(export_dir, filename)

    pdf = RMReport()
    font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.add_font("DejaVu", "B", font_path, uni=True)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.section("Smart Summary")
    pdf.body_text("Recommendation Message", decision.message)
    pdf.body_text("Next Best Action", decision.suggested_action)
    pdf.body_text("Engagement Score", f"{intent_score}/100")
    pdf.body_text("Pitch for RM", pitch_text)

    pdf.section("Customer Profile")
    pdf.body_text("Name", f"{customer.name} | CIF: {customer.cif}")
    pdf.body_text("Segment", customer.segment)
    pdf.body_text("Employer", f"{customer.employer} ({customer.industry})")
    pdf.body_text("Net Worth", f"AED {customer.net_worth}")
    pdf.body_text("Balance History", str(customer.balance_history))
    pdf.body_text("Campaign History", customer.campaign_history)
    pdf.body_text("Products", ", ".join(customer.products))

    pdf.section("Recent Transactions")
    pdf.txn_table(customer.transactions)

    pdf.section("RM Info")
    pdf.body_text("Relationship Manager", rm_name)

    pdf.output(filepath)