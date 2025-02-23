# SOW Invoice Generator

This project is designed to automate the generation of a Statement of Work (SOW) and associated invoices based on a standardized configuration file. The generated documents are in PDF format and include all necessary details for project management and billing.

## Project Structure

```plaintext
sow_invoice_generator
├── src
│   ├── generate_sow.py        # Script to generate the SOW PDF
│   ├── generate_invoices.py    # Script to generate invoices for each milestone
│   └── config
│       ├── sow_inv.config      # Configuration file with project details
│       └── bad_inv.config  # Configuration file for generating bad invoices  
│       └── bad_sow.config  # Configuration file for generating bad SOWs 
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
cd /data/data_generator
python src/generate_sow.py "Contoso Ltd."
```

This will create a PDF document containing the project details, objectives, tasks, schedules, compliance, and deliverables as specified in the `sow_inv.config` file for the `Contoso Ltd.` vendor.

Running the command without a vendor with generate SOWs for ALL vendors.

``` bash
python src/generate_sow.py
```

### Generating Invoices

To generate invoices for each milestone defined in the SOW, run (while in the `/data/data_generator` directory):

```bash
python src/generate_invoices.py "Contoso Ltd." 
```

This will create individual PDF invoices linked to the milestones and deliverables specified in the SOW for that vendor.

Running the command without a vendor with generate invoices for ALL vendors.

``` bash
python src/generate_invoices.py
```

## Configuration File

The `sow_inv.config` file contains all the necessary standardized values for the project. It includes:

- Vendor details
- Project scope and objectives
- Tasks and schedules
- Payment terms and compliance requirements
- Deliverables associated with each milestone

Ensure that the configuration file is correctly formatted to facilitate seamless integration with the SOW and invoice generation scripts.

The `bad_sow.config` and `bad_inv.config` files contain erroneous data for vendors that are not deployed to the database as part of the seeding process.  The vendors who have not been seeded into the database are:

1. Contoso Ltd.
1. Lucerne Publishing
1. VanArsdel Ltd.
1. Trey Research
1. Fabrikam Inc.
1. The Phone Company

## Generating Bad SOWs

To generate bad SOWs using the bad_sow.config configuration file and for the `Fabrikam Inc` vendor, run (while in the `/data/data_generator` directory):

```bash
python src/generate_sow.py "Fabrikam Inc" bad_sow.config
```

## Generating Bad Invoices

To generate bad invoices using the bad_inv.config configuration file and for the `Fabrikam Inc` vendor, run (while in the `/data/data_generator` directory):

```bash
python src/generate_invoices.py "Fabrikam Inc" bad_inv.config
```

## Output

The generated SOW and invoices will be saved in the

```plaintext
../data/sample_docs 
```

directory. You can open them using any PDF viewer.
