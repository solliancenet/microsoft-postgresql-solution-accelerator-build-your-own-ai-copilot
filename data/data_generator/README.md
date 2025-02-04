# SOW Invoice Generator

This project is designed to automate the generation of a Statement of Work (SOW) and associated invoices based on a standardized configuration file. The generated documents are in PDF format and include all necessary details for project management and billing.

## Project Structure

```plaintext
sow_invoice_generator
├── src
│   ├── generate_sow.py        # Script to generate the SOW PDF
│   ├── generate_invoices.py    # Script to generate invoices for each milestone
│   └── config
│       └── sow_inv.config      # Configuration file with project details
├── requirements.txt            # List of dependencies for the project
└── README.md                   # Documentation for the project
```

## Installation

To set up the project, follow these steps:

1. Install the required dependencies:

``` bash
pip install -r requirements.txt
```

## Usage

### Generating the Statement of Work (SOW)

To generate the SOW PDF, run the following command:

``` bash
python src/generate_sow.py
```

This will create a PDF document containing the project details, objectives, tasks, schedules, compliance, and deliverables as specified in the `sow_inv.config` file.

### Generating Invoices

To generate invoices for each milestone defined in the SOW, run:

```bash
python src/generate_invoices.py
```

This will create individual PDF invoices linked to the milestones and deliverables specified in the SOW.

## Configuration File

The `sow_inv.config` file contains all the necessary standardized values for the project. It includes:

- Vendor details
- Project scope and objectives
- Tasks and schedules
- Payment terms and compliance requirements
- Deliverables associated with each milestone

Ensure that the configuration file is correctly formatted to facilitate seamless integration with the SOW and invoice generation scripts.

## Output

The generated SOW and invoices will be saved in the ../data/sample_docs directory. You can open them using any PDF viewer.
