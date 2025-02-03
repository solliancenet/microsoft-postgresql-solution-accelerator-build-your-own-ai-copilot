from fpdf import FPDF
import os
import sys
import json
import argparse
from collections import defaultdict
import random
from datetime import datetime, timedelta

# Load configuration from the sow_inv.config file
def load_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

# Create a function to generate an invoice PDF
def create_invoice(invoice_number, deliverables, vendor_info, client_info, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    
    # Title
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt=f"Invoice Number: {invoice_number}", ln=True, align="C")
    
    # Vendor Information
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, txt=f"Vendor: {vendor_info['name']}", ln=True, align="L")
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, txt=f"Address: {vendor_info['address']}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Contact Name: {vendor_info['contact_name']}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Contact Email: {vendor_info['contact_email']}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Contact Number: {vendor_info['contact_phone']}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"SOW Number: {vendor_info['SOW']}", ln=True, align="L")
    
    # Calculate the invoice date as the due date minus 30 days
    due_date = datetime.strptime(deliverables[0]['due_date'], '%Y-%m-%d')
    invoice_date = due_date - timedelta(days=30)
    pdf.cell(0, 10, txt=f"Invoice Date: {invoice_date.strftime('%Y-%m-%d')}", ln=True, align="L")
      
    # Client Information
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, txt=f"Client: {client_info['name']}", ln=True, align="L")
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, txt=f"Contact Name: {client_info['contact_name']}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Contact Email: {client_info['contact_email']}", ln=True, align="L")
    pdf.ln(10)  # Added line

    # Invoice Details
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(40, 10, txt="Milestone", border=1)
    pdf.cell(80, 10, txt="Deliverable", border=1)
    pdf.cell(30, 10, txt="Amount", border=1)
    pdf.cell(40, 10, txt="Due Date", border=1)
    pdf.ln()

    total_amount = 0
    pdf.set_font("Arial", size=10)
    for deliverable in deliverables:
        pdf.cell(40, 10, txt=deliverable['name'], border=1)
        pdf.cell(80, 10, txt=deliverable['deliverables'], border=1)
        pdf.cell(30, 10, txt=deliverable['amount'], border=1)
        pdf.cell(40, 10, txt=deliverable['due_date'], border=1)
        pdf.ln()
        amount = float(deliverable['amount'].replace('$', '').replace(',', ''))
        total_amount += amount
    
    # Total Amount
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(120, 10, txt="Total Amount", border=1, align='R')
    pdf.cell(70, 10, txt=f"${total_amount:,.2f}", border=1)  # Updated line
    pdf.ln(20)

    # Payment Instructions
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, txt=(
        f"If paying by Direct Credit please pay into the following bank account:\n"
        f"Account Name: {vendor_info['name']}\n"
        f"Account Number: {random.randint(10000000, 99999999)}\n"
        f"To help us allocate money correctly, please reference your invoice number: {invoice_number}\n\n"
        f"Payment Terms:\n{payment_info}\n"
    ))

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Output the PDF
    pdf.output(output_path)

if __name__ == "__main__":
    # Define the argument parser
    parser = argparse.ArgumentParser(description="Generate invoices for a given vendor.")
    parser.add_argument("vendor_name", type=str, help="The name of the vendor")
    parser.add_argument("config_file", type=str, nargs='?', default='sow_inv.config', help="The configuration file to use (default: sow_inv.config)")
    args = parser.parse_args()

    vendor_name = args.vendor_name
    config_file = args.config_file

    config_path = f'src/config/{config_file}'
    configs = load_config(config_path)
    
    # Find the vendor configuration by name
    vendor_config = next((config for config in configs if config['name'] == vendor_name), None)
    if not vendor_config:
        raise ValueError(f"Vendor '{vendor_name}' not found in configuration.")
    
    client_info = {
        "name": "Woodgrove Bank",
        "contact_name": "Chris Green",
        "contact_email": "chris.green@woodgrovebank.com"
    }

    # Extract payment terms and penalty from the configuration
    payment_terms = vendor_config['payments']['terms']
    penalty = vendor_config['payments']['penalty']

    # Use the extracted payment terms and penalty in the formatted strings
    payment_info = (
        f"- Payment is due within {payment_terms.split()[1]} days of the invoice date.\n"
        f"- A penalty of {penalty.split()[0]} will be applied for late payments."
    )

    # Group deliverables by invoice number
    grouped_deliverables = defaultdict(list)
    for deliverable in vendor_config['deliverables']:
        grouped_deliverables[deliverable['invoice#']].append(deliverable)

    # Generate invoices for each group of deliverables
    for invoice_num, deliverables in grouped_deliverables.items():
        # Generate the invoice number in the required format
        words = vendor_config['name'].split()
        invoice_prefix = f"{words[0][0]}{words[1][0]}" if len(words) > 1 else words[0][:2]
        invoice_number = f"INV-{invoice_prefix.upper()}2024-{invoice_num:03d}"
        output_path = f"../sample_docs/{invoice_number}.pdf"
        
        create_invoice(invoice_number, deliverables, vendor_config, client_info, output_path)