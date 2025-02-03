from fpdf import FPDF
import json
import argparse
from datetime import datetime
import os
import textwrap

# Function to generate the SOW PDF
def generate_sow_pdf(output_path, vendor_name,config):
    # Load configuration from the JSON file
    with open('src/config/sow_inv.config', 'r') as config_file:
        configs = json.load(config_file)

    # Find the vendor configuration by name
    config = next((config for config in configs if config['name'] == vendor_name), None)
    if not config:
        raise ValueError(f"Vendor '{vendor_name}' not found in configuration.")

    # Replace placeholders in compliance section and wrap text
    for i, item in enumerate(config['compliance']):
        item = item.replace("{name}", config['name'])
        config['compliance'][i] = textwrap.fill(item, width=100)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # Title
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Statement of Work", ln=True, align="C")
    pdf.ln(10)

    # Project Details
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, txt=f"Project Name: {config['project_name']}", ln=True)
    pdf.cell(0, 10, txt=f"Effective Date: {config['start_date']}", ln=True)
    pdf.cell(0, 10, txt=f"Project Completion Date: {config['completion_date']}", ln=True)
    pdf.cell(0, 10, txt=f"SOW Number: {config['SOW']}", ln=True)

    # Section Headers and Content
    sections = {
        "Project Scope": config['project_scope'],
        "Project Objectives": config['project_objectives'],
        "Tasks": config['tasks'],
        "Schedules": config['schedules'],
        "Requirements": config['requirements'],
        "Payments": config['payments'],
        "Compliance": config['compliance']
    }

    for section, content in sections.items():
        pdf.set_font("Arial", style="B", size=10)
        pdf.cell(0, 10, txt=section, ln=True)
        pdf.set_font("Arial", size=10)
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    for key, value in item.items():
                        pdf.cell(0, 10, txt=f"{key}: {value}", ln=True)
                else:
                    pdf.multi_cell(0, 10, txt=f"- {item}")
        elif isinstance(content, dict):
            for key, value in content.items():
                pdf.cell(0, 10, txt=f"{key}: {value}", ln=True)
        else:
            pdf.multi_cell(0, 10, txt=content)
        pdf.ln(10)
        
        # Insert a page break after the "Tasks" section
        if section == "Tasks":
            pdf.add_page()

    # Deliverables Table
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, txt="Project Deliverables", ln=True)
    pdf.set_font("Arial", size=10)

    # Table Header
    pdf.cell(20, 10, txt="Item", border=1)
    pdf.cell(40, 10, txt="Milestone Name", border=1)
    pdf.cell(80, 10, txt="Deliverables", border=1)
    pdf.cell(30, 10, txt="Amount", border=1)
    pdf.cell(30, 10, txt="Due Date", border=1)
    pdf.ln()

    # Table Content
    total_amount = 0
    for deliverable in config['deliverables']:
        pdf.cell(20, 10, txt=str(deliverable['number']), border=1)
        pdf.cell(40, 10, txt=deliverable['name'], border=1)
        pdf.cell(80, 10, txt=deliverable['deliverables'], border=1)
        pdf.cell(30, 10, txt=deliverable['amount'], border=1)
        pdf.cell(30, 10, txt=deliverable['due_date'], border=1)
        pdf.ln()
        # Sum the amounts
        amount = float(deliverable['amount'].replace('$', '').replace(',', ''))
        total_amount += amount

    # Total Amount
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(140, 10, txt="Total", border=1, align='R')
    pdf.cell(60, 10, txt=f"${total_amount:,.2f}", border=1)
    pdf.ln()

    # Signatures
    pdf.ln(20)
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, txt="Signatures", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, txt=f"________________ ({config['name']} - {config['contact_name']})", ln=True)
    pdf.cell(0, 10, txt="________________ (Woodgrove Bank - Chris Green)", ln=True)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    pdf.output(output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Statement of Work PDF")
    parser.add_argument("vendor_name", type=str, help="The name of the vendor")
    args = parser.parse_args()

    vendor_name = args.vendor_name

    with open('src/config/sow_inv.config', 'r') as config_file:
        configs = json.load(config_file)
    
    config = next((config for config in configs if config['name'] == vendor_name), None)
    if not config:
        raise ValueError(f"Vendor '{vendor_name}' not found in configuration.")
    
    name = config['name'].replace(" ", "_").replace(".", "")
    start_date_str = config.get('start_date', "")
    if not start_date_str:
        raise ValueError(f"Start date not found for vendor '{vendor_name}'")
    
    start_date = datetime.strptime(start_date_str, "%B %d, %Y").strftime("%Y%m%d")
    output_path = f"../sample_docs/Statement_of_Work_{name}_Woodgrove_Bank_{start_date}.pdf"
    generate_sow_pdf(output_path, vendor_name, config)