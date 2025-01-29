from fpdf import FPDF
import os
import json
import argparse
from datetime import datetime

# Load configuration from the sow_inv.config file
def load_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

# Create a function to generate an invoice PDF
def create_invoice(invoice_number, milestone_name, deliverables, amount_due, due_date, vendor_info, client_info, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    
    # Title
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt=f"Invoice Number: {invoice_number}", ln=True, align="C")
    
    # Vendor Information
    pdf.ln(10)
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, txt=f"Vendor: {vendor_info['name']}", ln=True, align="L")
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, txt=f"Address: {vendor_info['address']}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Contact Name: {vendor_info['contact_name']}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Contact Email: {vendor_info['contact_email']}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Contact Number: {vendor_info['contact_phone']}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"SOW Number: {vendor_info['SOW']}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Invoice Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="L")
      
    # Client Information
    pdf.ln(10)
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, txt=f"Client: {client_info['name']}", ln=True, align="L")
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, txt=f"Address: {client_info['address']}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Contact Name: {client_info['contact_name']}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Contact Email: {client_info['contact_email']}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Contact Number: {client_info['contact_phone']}", ln=True, align="L")
    
    # Invoice Details
    pdf.ln(10)
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, txt=f"Milestone Name: {milestone_name}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Deliverables: {deliverables}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Amount Due: {amount_due}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Due Date: {due_date}", ln=True, align="L")
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Output the PDF
    pdf.output(output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Invoices for a Vendor")
    parser.add_argument("vendor_name", type=str, help="The name of the vendor")
    args = parser.parse_args()

    vendor_name = args.vendor_name

    config_path = 'src/config/sow_inv.config'
    configs = load_config(config_path)
    
    # Find the vendor configuration by name
    vendor_config = next((config for config in configs if config['name'] == vendor_name), None)
    if not vendor_config:
        raise ValueError(f"Vendor '{vendor_name}' not found in configuration.")
    
    client_info = {
        "name": "Woodgrove Bank",
        "address": "456 Client Ave, Client City, CC 67890",
        "contact_name": "Chris Green",
        "contact_email": "chris.green@woodgrovebank.com",
        "contact_phone": "098-765-4321"
    }

    # Generate invoices for each deliverable
    for deliverable in vendor_config['deliverables']:
        invoice_number = f"INV-{vendor_config['SOW']}-{deliverable['number']:03d}"
        milestone_name = deliverable['name']
        deliverables = deliverable['deliverables']
        amount_due = deliverable['amount']
        due_date = deliverable['due_date']
        output_path = f"../output/Invoice_{invoice_number}.pdf"
        
        create_invoice(invoice_number, milestone_name, deliverables, amount_due, due_date, vendor_config, client_info, output_path)