/*  File to create tables and load sample data  */

/* VENDORS */

-- Vendors table
CREATE TABLE IF NOT EXISTS vendors (
    id BIGSERIAL PRIMARY KEY,
    name text NOT NULL,
    address text NOT NULL,
    contact_name text NOT NULL,
    contact_email text NOT NULL,
    contact_phone text NOT NULL,
    website text NOT NULL,
    type text NOT NULL
);

-- Insert vendors only if vendors table is empty
INSERT INTO vendors (id, name, address, contact_name, contact_email, contact_phone, website, type)
SELECT v.id, v.name, v.address, v.contact_name, v.contact_email, v.contact_phone, v.website, v.type
FROM (
    SELECT 1 as id, 'Adatum Corporation' as name, '789 Goldsmith Road, MainTown City' as address, 'Elizabeth Moore' as contact_name, 'elizabeth.moore@adatum.com' as contact_email, '555-789-7890' as contact_phone, 'http://www.adatum.com' as website, 'Data Engineering' as type
    UNION ALL
    SELECT 2, 'Contoso, Ltd.', '456 Industrial Road, Scooton City', 'Nicole Wagner', 'nicole@contoso.com', '555-654-3210', 'http://www.contoso.com', 'Software Engineering'
    UNION ALL
    SELECT 3, 'Lucerne Publishing', '789 Live Street, Woodgrove', 'Ana Bowman', 'abowman@lucernepublishing.com', '555-654-9870', 'http://www.lucernepublishing.com', 'Graphic Design'
    UNION ALL
    SELECT 4, 'VarArsdel, Ltd.', '123 Innovation Drive, TechVille', 'Gabriel Diaz', 'gdiaz@vanarsdelltd.com', '555-321-0987', 'http://www.vanarsdelltd.com', 'Software Engineering'
    UNION ALL
    SELECT 5, 'Trey Research', '456 Research Avenue, Redmond', 'Serena Davis', 'serena.davis@treyresearch.net', '555-867-5309', 'http://www.treyresearch.net', 'DevOps'
    UNION ALL
    SELECT 6, 'Fabrikam, Inc.', '24601 South St., Philadelphia', 'Remy Morris', 'remy.morris@fabrikam.com', '610-321-0987', 'http://www.fabrikam.com', 'AI Services'
    UNION ALL
    SELECT 7, 'The Phone Company', '10642 Meridian St., Indianapolis', 'Ashley Schroeder', 'ashley.schroeder@thephone-company.com', '719-444-2345', 'http://www.thephone-company.com', 'Communications'
) as v
WHERE NOT EXISTS (SELECT 1 FROM vendors);

/* END VENDORS */

/* STATUS */

-- Status table
DROP TABLE IF EXISTS status;
CREATE TABLE IF NOT EXISTS status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT
);

-- Insert status values
INSERT INTO status (id, name, description) VALUES (1, 'Pending', 'Awaiting action');
INSERT INTO status (id, name, description) VALUES (2, 'In Progress', 'In progress');
INSERT INTO status (id, name, description) VALUES (3, 'In Review', 'Review is required');
INSERT INTO status (id, name, description) VALUES (4, 'Cancelled', 'The process was stopped');
INSERT INTO status (id, name, description) VALUES (5, 'Overdue', 'The invoice has passed the due date without payment');
INSERT INTO status (id, name, description) VALUES (6, 'Paid', 'The invoice has been fully paid');
INSERT INTO status (id, name, description) VALUES (7, 'Completed', 'Work has been finished');

/* END STATUS */

/* SOWs */

-- Statement of work table
CREATE TABLE IF NOT EXISTS sows (
    id BIGSERIAL PRIMARY KEY,
    number text NOT NULL,
    vendor_id BIGINT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    budget DECIMAL(18,2) NOT NULL,
    document text NOT NULL,
    metadata JSONB,
    summary text,
    FOREIGN KEY (vendor_id) REFERENCES vendors (id) ON DELETE CASCADE
);

-- Insert sow values only if the specific sow number does not exist
INSERT INTO sows (number, vendor_id, start_date, end_date, budget, document, metadata)
SELECT 'SOW-2024-073',
       1,
       '2024-11-01',
       '2025-12-31',
       43600.00,
       '1/sow/Statement_of_Work_Adatum_Corporation_Woodgrove_Bank_20241101.pdf',
       '{}'
WHERE NOT EXISTS (SELECT 1 FROM sows WHERE number = 'SOW-2024-073');

INSERT INTO sows (number, vendor_id, start_date, end_date, budget, document, metadata)
SELECT 'SOW-2024-052',
       2,
       '2024-06-01',
       '2025-11-30',
       75000.00,
       '2/sow/Statement_of_Work_Contoso_DevOps_Services_Woodgrove_Bank_20240601.pdf',
       '{}'
WHERE NOT EXISTS (SELECT 1 FROM sows WHERE number = 'SOW-2024-052');

INSERT INTO sows (number, vendor_id, start_date, end_date, budget, document, metadata)
SELECT 'SOW-2024-081',
       3,
       '2024-12-01',
       '2024-12-31',
       50000.00,
       '3/sow/Statement_of_Work_Lucerne_Publishing_Woodgrove_Bank_20241201.pdf',
       '{}'
WHERE NOT EXISTS (SELECT 1 FROM sows WHERE number = 'SOW-2024-081');

INSERT INTO sows (number, vendor_id, start_date, end_date, budget, document, metadata)
SELECT 'SOW-2024-070',
       4,
       '2024-10-01',
       '2025-09-30',
       60000.00,
       '4/sow/Statement_of_Trey_Research_Woodgrove_Bank_20241001.pdf',
       '{}'
WHERE NOT EXISTS (SELECT 1 FROM sows WHERE number = 'SOW-2024-070');

INSERT INTO sows (number, vendor_id, start_date, end_date, budget, document, metadata)
SELECT 'SOW-2024-W-038',
       5,
       '2024-05-01',
       '2025-08-31',
       45000.00,
       '5/sow/Statement_of_Work_Trey_Research_Inc_Woodgrove_Bank_20240501.pdf',
       '{}'
WHERE NOT EXISTS (SELECT 1 FROM sows WHERE number = 'SOW-2024-W-038');

-- SOW Chunks table: Holds the content of the SOW in sections
CREATE TABLE IF NOT EXISTS sow_chunks (
    id BIGSERIAL PRIMARY KEY,
    sow_id BIGINT NOT NULL,
    heading text NOT NULL,
    content text NOT NULL,
    page_number INT NOT NULL,
    FOREIGN KEY (sow_id) REFERENCES sows (id) ON DELETE CASCADE
);

-- Insert starter data for sow_chunks
INSERT INTO sow_chunks (sow_id, heading, content, page_number)
VALUES
(1, 'Project Scope', 'Adatum Corporation will provide comprehensive Azure resource management services, including infrastructure monitoring, automated scaling, cost optimization, and application troubleshooting, to ensure high availability and efficiency for Woodgrove Bank.', 1),
(1, 'Project Objectives', 'Ensure the continuous performance and scalability of Azure resources. Implement cost-efficient resource management strategies. Minimize downtime through proactive monitoring and rapid troubleshooting.', 1),
(1, 'Tasks', '1. Set up Azure resource monitoring tools. 2. Design and implement automated scaling strategies. 3. Conduct cost analysis and apply optimization measures. 4. Perform regular maintenance on Azure-hosted applications. 5. Troubleshoot and resolve any application or resource issues.', 1),
(1, 'Schedules', 'Project kick-off: November 01, 2024 - Initial monitoring setup: November 08, 2024 - Scaling implementation: November 15, 2024 - Cost optimization review: November 22, 2024 - Maintenance practices established: December 13, 2024 - Final troubleshooting and wrap-up: December 31, 2025', 1),
(1, 'Payments', 'Payment terms are Net 30. Invoices will be issued upon the completion of each milestone and are payable within 30 days. A penalty of 10% will be applied for late deliveries or payments.', 1),
(1, 'Compliance', '- Data Security: All data transfers between the Service Provider and Client will use secure, encrypted communication protocols. Data at rest will be encrypted using industry-standard encryption algorithms (e.g., AES-256). - Access Control: Access to the Azure resources and sensitive client information will be granted only to authorized personnel. Multi-factor authentication (MFA) will be enforced for all administrative access. - Audit and Monitoring: Adatum Corporation will maintain comprehensive logs of all access and changes to Azure resources. Regular audits will be conducted to ensure compliance with security protocols. - Incident Response: In the event of a security incident, the Service Provider will notify the Client within 24 hours. A detailed incident report will be provided within 48 hours, outlining the root cause, impact, and mitigation steps. - Regulatory Compliance: The project will comply with applicable regulations, including GDPR, PCI DSS, and ISO 27001, as they pertain to the management of Azure resources.', 2),
(1, 'Project Deliverables', 'Milestone Name Deliverables Amount Due Date 1 Monitoring Monitoring of resources $8,600.00 2024-11-08 2 Resource Scaling Implementation of automated scaling $7,000.00 2024-11-15 3 Cost Management Cost Management Implementation $7,000.00 2024-11-22 4 Maintenance Practices Maintenance & troubleshooting practice $10,500.00 2024-11-27 5 App Troubleshooting Identify Azure application issues $2,000.00 2024-11-27 5 App Troubleshooting Resolution of Azure application issues $3,500.00 2024-12-13 5 App Troubleshooting Implementation of app monitoring $5,000.00 2024-12-31 Total $43,600.00 Signatures (Adatum Corporation - Elizabeth Moore) (Woodgrove Bank - Sora Kim)', 2);


-- Milestones table: Holds the milestones for each SOW
CREATE TABLE IF NOT EXISTS milestones (
    id BIGSERIAL PRIMARY KEY,
    sow_id BIGINT NOT NULL,
    name text NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (sow_id) REFERENCES sows (id) ON DELETE CASCADE
);

-- Insert starter data for milestones 
INSERT INTO milestones (sow_id, name, status)
VALUES
    (1,'Monitoring','Completed'),
    (1,'Resource Scaling','Completed'),
    (1,'Cost Management','Completed'),
    (1,'Maintenance Practices','Completed'),
    (1,'App Troubleshooting','In Progress'),
    (2,'CI/CD Pipelines','Completed'),
    (2,'Containerized Applications','In Progress'),
    (2,'Cloud Monitoring','In Progress');

-- Deliverables table: Holds the deliverables for each milestone
CREATE TABLE IF NOT EXISTS deliverables (
    id BIGSERIAL PRIMARY KEY,
    milestone_id BIGINT NOT NULL,
    description TEXT,
    amount NUMERIC(10, 2),
    status TEXT NOT NULL,
    due_date DATE NOT NULL,
    FOREIGN KEY (milestone_id) REFERENCES milestones (id) ON DELETE CASCADE
);

-- Insert starter data for deliverable
INSERT INTO deliverables (milestone_id, description, status, due_date)
VALUES
(1,'Monitoring of resources','Completed', '2024-11-08'),
(2,'Implementation of automated scaling','Completed', '2024-11-15'),
(3,'Cost Management Implementation','Completed', '2024-11-22'),
(4,'Maintenance and troubleshooting practices','Completed', '2024-11-27'),
(5,'Identify Azure application issues','In Progress', '2024-11-27'),
(5,'Resolution of Azure application issues','Completed', '2024-12-13'),
(6,'Design CI/CD pipelines','Completed', '2024-10-10'),
(8,'Initial setup of Cloud infrastructure monitoring','In Progress', '2024-10-10');

-- SOW Validation Results table
CREATE TABLE IF NOT EXISTS sow_validation_results (
    id BIGSERIAL PRIMARY KEY,
    sow_id BIGINT NOT NULL,
    datestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    result TEXT,
    validation_passed BOOLEAN,
    FOREIGN KEY (sow_id) REFERENCES sows (id) ON DELETE CASCADE
);

-- Insert starter data for sow_validation_results
INSERT INTO sow_validation_results (
    sow_id,
    datestamp,
    result,
    validation_passed
)
VALUES
    (1, CURRENT_TIMESTAMP - INTERVAL '2 hours', 'Missing deliverables section.', FALSE),
    (1, CURRENT_TIMESTAMP - INTERVAL '1 hour', 'Deliverables section contains wrong information and incorrect total billable amount for milestone 1.', FALSE),
    (1, CURRENT_TIMESTAMP, 'The SOW has been correct and is now correct.', TRUE),
    (2, CURRENT_TIMESTAMP - INTERVAL '1 hour', 'Incorrect milestone dates.', FALSE),
    (2, CURRENT_TIMESTAMP, 'Everything is correct now.', TRUE),
    (3, CURRENT_TIMESTAMP, 'SOW looks good.', TRUE),
    (4, CURRENT_TIMESTAMP, 'The required compliance section is missing.', FALSE),
    (4, CURRENT_TIMESTAMP, 'All fields are valid.', TRUE),
    (5, CURRENT_TIMESTAMP, 'All fields are valid.', TRUE);

/* END SOWs */

/* INVOICES */

-- Invoices table
CREATE TABLE IF NOT EXISTS invoices (
    id BIGSERIAL PRIMARY KEY,
    number text NOT NULL,
    vendor_id BIGINT NOT NULL,
    sow_id BIGINT NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    invoice_date DATE NOT NULL,
    payment_status VARCHAR(50) NOT NULL,
    document text NOT NULL, -- document path
    content text, --  text content from the invoice
    metadata JSONB, --  additional metadata
    FOREIGN KEY (vendor_id) REFERENCES vendors (id) ON DELETE CASCADE,
    FOREIGN KEY (sow_id) REFERENCES sows (id) ON DELETE CASCADE
);

-- Insert starter data for invoices
INSERT INTO invoices (id, number, vendor_id, sow_id, amount, invoice_date, payment_status, document, content, metadata)
VALUES
    (1, 'INV-TWC2024-001', 1, 1, 15600, '2024-11-08', 'Paid', '1/invoice/INV-TWC2024-001.pdf',  '{"Invoice Number: INV-TWC2024-001 Vendor: Adatum Corporation Address: 789 Goldsmith Road, MainTown City Contact Name: Elizabeth Moore Contact Email: elizabeth.moore@adatum.com Contact Number: 123-789-7890 SOW Number: SOW-2024-073 Invoice Date: 2024-11-08 Client: Woodgrove Bank Address: 123 Financial Avenue, Woodgrove City Milestone  Deliverables Amount Due Date Monitoring Monitoring of resources $8600.00 2024-12-08 Cost Management Cost Mangement Implementation $7000.00 2024-12-08 Total Amount $15600.00 If paying by Direct Credit please pay into the following bank account: Account Name: Adatum Corporation Account Number: 456-123-789 To help us allocate money correctly, please reference your invoice number: INV-TWC2024-001 Payment Terms - Payment is due within 30 days of the invoice date. - A penalty of 10% will be applied for late payments.","Thank you for choosing Adatum Corporation"}', '{}'),
    (2, 'INV-TWC2024-002', 1, 1, 7000, '2024-11-22', 'Paid', '2/invoice/INV-TWC2024-002.pdf', '{"Invoice Number: INV-TWC2024-002 Vendor: Adatum Corporation Address: 789 Goldsmith Road, MainTown City Contact Name: Elizabeth Moore Contact Email: elizabeth.moore@adatum.com Contact Number: 123-789-7890 SOW Number: SOW-2024-073 Invoice Date: 2024-11-22 Client: Woodgrove Bank Address: 123 Financial Avenue, Woodgrove City Milestone Deliverables Amount Due Date Resource Scaling Implementation of automated scaling $7000.00 2024-12-22 Total Amount $7000.00 If paying by Direct Credit please pay into the following bank account: Account Name: Adatum Corporation Account Number: 456-123-789 To help us allocate money correctly, please reference your invoice number: INV-TWC2024-002 Payment Terms - Payment is due within 30 days of the invoice date. - A penalty of 10% will be applied for late payments. Thank you for choosing Adatum Corporation"}', '{}'),
    (3, 'INV-TWC2024-003', 1, 1, 12500, '2024-11-27', 'In Review', '3/invoice/INV-TWC2024-003.pdf',  '{"Invoice Number: INV-TWC2024-003 Vendor: Adatum Corporation Address: 789 Goldsmith Road, MainTown City Contact Name: Elizabeth Moore Contact Email: elizabeth.moore@adatum.com Contact Number: 123-789-7890 SOW Number: SOW-2024-073 Invoice Date: 2024-11-27 Client: Woodgrove Bank Address: 123 Financial Avenue, Woodgrove City Milestone Deliverables Amount Due Date Maintenance Practices Maintenance and troubleshooting practices $10500.00 2024-12-27 App Troubleshooting Identify Azure application issues $2000.00 2024-12-27 Total Amount $12500.00 If paying by Direct Credit please pay into the following bank account: Account Name: Adatum Corporation Account Number: 456-123-789 To help us allocate money correctly, please reference your invoice number: INV-TWC2024-003 Payment Terms - Payment is due within 30 days of the invoice date. - A penalty of 10% will be applied for late payments.","Thank you for choosing Adatum Corporation"}', '{}'),
    (4, 'INV-TWC2024-004', 1, 1, 3500, '2024-11-30', 'Paid', '4/invoice/INV-TWC2024-004.pdf',  '{"Invoice Number: INV-TWC2024-004 Vendor: Adatum Corporation Address: 789 Goldsmith Road, MainTown City Contact Name: Elizabeth Moore Contact Email: elizabeth.moore@adatum.com Contact Number: 123-789-7890 SOW Number: SOW-2024-073 Invoice Date: 2024-11-30 Client: Woodgrove Bank Address: 123 Financial Avenue, Woodgrove City Milestone Deliverables Amount Due Date App Troubleshooting Resolution of Azure application issues $3500.00 2024-12-30 Total Amount $3500.00 If paying by Direct Credit please pay into the following bank account: Account Name: Adatum Corporation Account Number: 456-123-789 To help us allocate money correctly, please reference your invoice number: INV-TWC2024-004 Payment Terms - Payment is due within 30 days of the invoice date. - A penalty of 10% will be applied for late payments. Thank you for choosing Adatum Corporation"}', '{}'),
    (5, 'INV-WWE2024-001', 5, 2, 36600, '2024-10-10', 'Pending', '5/invoice/INV-WWE2024-001.pdf',  '{"Invoice Number: INV-WWE2024-001 Vendor: Trey Research Address: 123 Innovation Drive, TechVille Contact Name: Serena Davis Contact Email: serena.davis@treyresearch.net Contact Number: 555-967-8543 SOW Number: SOW-2024-W-038 Invoice Date: 2024-10-10 Client: Woodgrove Bank Address: 123 Financial Avenue, Woodgrove City Milestone Deliverables Amount Due Date CI/CD Pipelines Design CI/CD pipelines $20100.00 2024-11-10 Cloud Monitoring Initial setup of Cloud infrastructure monitoring $16500.00 2024-11-10 Total Amount $36600.00 If paying by Direct Credit please pay into the following bank account: Account Name: Trey Research Account Number: 123-456-789 To help us allocate money correctly, please reference your invoice number: INV-WWE2024-001 Payment Terms - Payment is due within 30 days of the invoice date. - A penalty of 10% will be applied for late payments. Thank you for choosing Trey Research"}', '{}');

-- Invoice Line Items table
CREATE TABLE IF NOT EXISTS invoice_line_items (
    id BIGSERIAL PRIMARY KEY,
    invoice_id BIGINT NOT NULL,
    description TEXT,
    amount NUMERIC(10, 2),
    status TEXT NOT NULL,
    due_date DATE NOT NULL,
    FOREIGN KEY (invoice_id) REFERENCES invoices (id) ON DELETE CASCADE
);

-- Insert starter data for invoice_line_items
INSERT INTO invoice_line_items (invoice_id, description, amount, status, due_date)
VALUES

(1,'Monitoring of resources',8600,'Completed','2024-12-08'),
(1,'Cost Management Implementation',7000,'Completed','2024-12-08'),
(2,'Implementation of automated scaling',7000,'Completed','2024-12-22'),
(3,'Maintenance and troubleshooting practices',10500,'Completed','2024-12-27'),
(3,'Identify Azure application issues',2000,'In Progress','2024-12-27'),
(4,'Resolution of Azure application issues',3500,'Completed','2024-12-30'),
(5,'Design CI/CD pipelines',20100,'Completed','2024-12-10'),
(5,'Initial setup of Cloud infrastructure monitoring',16500,'In Progress','2024-12-10');

-- Invoice Validation Results table
CREATE TABLE IF NOT EXISTS invoice_validation_results (
    id BIGSERIAL PRIMARY KEY,
    invoice_id BIGINT NOT NULL,
    datestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    result TEXT,
    validation_passed BOOLEAN,
    FOREIGN KEY (invoice_id) REFERENCES invoices (id) ON DELETE CASCADE
);

-- Insert starter data for invoice_validation_results
INSERT INTO invoice_validation_results (
    invoice_id, 
	datestamp,
    result, 
    validation_passed
)
VALUES
    
    (1, CURRENT_TIMESTAMP - INTERVAL '2 hours', 'Total amount was wrong.', FALSE),
    (1, CURRENT_TIMESTAMP, 'Invoice had total amount added changed and passed with no errors.', TRUE),
    (2, CURRENT_TIMESTAMP, 'Invoice validation passed with warnings: Payment terms was missing penalty text.', TRUE),
    (3, CURRENT_TIMESTAMP - INTERVAL '2 hours', 'The amount invoiced for fixing application issues was $500 more than allowed by the contract.', FALSE),
    (4, CURRENT_TIMESTAMP - INTERVAL '2 hours', 'Lots of mistakes. Returning to vendor for corrections', FALSE),
    (4, CURRENT_TIMESTAMP, 'Everything fix. All good.', TRUE);

/* END INVOICES */
