from fpdf import FPDF
import os
import json

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
    pdf.cell(200, 10, txt="Invoice", ln=True, align="C")
    
    # Vendor Information
    pdf.ln(10)
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, txt=f"Vendor: {vendor_info['name']}", ln=True, align="L")
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, txt=f"Address: {vendor_info['address']}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Contact Name: {vendor_info['contact_name']}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Contact Email: {vendor_info['contact_email']}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Contact Number: {vendor_info['contact_phone']}", ln=True, align="L")
      
    # Client Information
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, txt=f"Client: {client_info['name']}", ln=True, align="L")
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, txt=f"Address: {client_info['address']}", ln=True, align="L")
    
    # Invoice Details
    pdf.ln(10)
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, txt=f"Invoice Number: {invoice_number}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Milestone: {milestone_name}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Deliverables: {deliverables}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Amount Due: ${amount_due:.2f}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Due Date: {due_date}", ln=True, align="L")
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, txt="If paying by Direct Credit please pay into the following bank account:", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Account Name: {vendor_info['name']}", ln=True, align="L")
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, txt=f"Account Number: {vendor_info['account_number']}", ln=True, align="L")
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, txt=f"To help us allocate money correctly, please reference your invoice number: {invoice_number}", ln=True, align="L")
    
    # Payment Terms
    pdf.ln(10)
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, txt="Payment Terms", ln=True, align="L")
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, txt=(
        "- Payment is due within 30 days of the invoice date.\n"
        "- A penalty of 10% will be applied for late payments.\n"
    ))
    
    # Footer
    pdf.ln(10)
    pdf.set_font("Arial", style="I", size=8)
    pdf.cell(0, 10, txt="Thank you for choosing TailWind Cloud Solutions!", ln=True, align="C")
    
    # Save the PDF
    pdf.output(output_path)
    return output_path

# Main function to generate invoices based on the configuration
def generate_invoices(config_path):
    config = load_config(config_path)
    
    vendor_info = {
        "name": config['name'],
        "address": config['address'],
        "contact_name": config['contact_name'],
        "contact_email": config['contact_email'],
        "contact_phone": config['contact_phone'],
        "account_number": "123-456-789"  # Example account number
    }
    
    client_info = {
        "name": "Woodgrove Bank",
        "address": "123 Financial Avenue, Woodgrove City"
    }
    
    output_paths = []
    for index, deliverable in enumerate(config['deliverables']):
        invoice_number = f"INV-TWC2024-{str(index + 1).zfill(3)}"
        milestone_name = deliverable[1]
        deliverables = deliverable[2]
        amount_due = float(deliverable[3].replace("$", "").replace(",", ""))
        due_date = deliverable[4]
        
        file_name = f"{invoice_number}.pdf"
        create_invoice(
            invoice_number=invoice_number,
            milestone_name=milestone_name,
            deliverables=deliverables,
            amount_due=amount_due,
            due_date=due_date,
            vendor_info=vendor_info,
            client_info=client_info,
            output_path=file_name
        )
        output_paths.append(file_name)

    return output_paths

# Generate invoices
config_path = os.path.join(os.path.dirname(__file__), 'config', 'sow_inv.config')
generate_invoices(config_path)