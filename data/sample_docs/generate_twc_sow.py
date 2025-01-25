import json
from fpdf import FPDF

# Function to generate the SOW PDF
def generate_sow_pdf(output_path, config_path):
    # Load configuration from JSON file
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # Title
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(200, 10, txt=config["title"], ln=True, align="C")
    pdf.ln(10)

    # Project Details
    pdf.set_font("Arial", style="B", size=8)
    project_details = config["project_details"]
    pdf.cell(0, 10, txt=f"Project Name: {project_details['project_name']}", ln=True)
    pdf.cell(0, 10, txt=f"Effective Date: {project_details['effective_date']}", ln=True)
    pdf.cell(0, 10, txt=f"Project Completion Date: {project_details['completion_date']}", ln=True)
    pdf.cell(0, 10, txt=f"SOW Number: {project_details['sow_number']}", ln=True)

    # Section Headers and Content
    sections = config["sections"]
    for title, content in sections.items():
        pdf.set_font("Arial", style="B", size=8)
        pdf.cell(0, 10, txt=title, ln=True)
        pdf.set_font("Arial", size=8)
        pdf.multi_cell(0, 10, txt=content)
        pdf.ln(5)

    # Add Deliverables Table
    pdf.set_font("Arial", style="B", size=8)
    pdf.cell(0, 10, txt="Project Deliverables", ln=True)
    pdf.set_font("Arial", size=8)
    deliverables = config["deliverables"]

    # Table Header
    pdf.cell(20, 10, txt="Milestone", border=1, align="C")
    pdf.cell(50, 10, txt="Name", border=1, align="C")
    pdf.cell(50, 10, txt="Deliverables", border=1, align="C")
    pdf.cell(25, 10, txt="Amount", border=1, align="C")
    pdf.cell(25, 10, txt="Due Date", border=1, align="C", ln=True)

    # Table Content
    total_amount = 0
    for row in deliverables:
        pdf.cell(20, 10, txt=row[0], border=1)
        pdf.cell(50, 10, txt=row[1], border=1)
        pdf.cell(50, 10, txt=row[2], border=1)
        pdf.cell(25, 10, txt=row[3], border=1)
        pdf.cell(25, 10, txt=row[4], border=1, ln=True)
        total_amount += float(row[3].replace("$", "").replace(",", ""))

    # Add Total Amount row
    pdf.cell(120, 10, txt="", border=0)
    pdf.cell(25, 10, txt="Total", border=1, align="C")
    pdf.cell(25, 10, txt=f"${total_amount:,.2f}", border=1, align="C", ln=True)

    # Output the PDF
    pdf.output(output_path)

# Example usage
generate_sow_pdf("output.pdf", "config.json")