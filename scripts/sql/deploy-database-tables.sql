/*  File to idempotently load table DDL for Claims Data  */

-- Vendors table: information about companies (e.g., tags, industry codes, preferences)
CREATE TABLE IF NOT EXISTS vendors (
    id BIGSERIAL PRIMARY KEY,
    name text NOT NULL,
    address text NOT NULL,
    contact_name text NOT NULL,
    contact_email text NOT NULL,
    contact_phone text NOT NULL,
    type text NOT NULL
);

-- Insert vendors only if vendors table is empty
INSERT INTO vendors (id, name, address, contact_name, contact_email, contact_phone, type)
SELECT v.id, v.name, v.address, v.contact_name, v.contact_email, v.contact_phone, v.type
FROM (
    SELECT 1 as id, 'TailWind Cloud Solutions' as name, '789 Goldsmith Road, MainTown City' as address, 'Morgan Skinner' as contact_name, 'morgan.skinner@tailwindcloud.com' as contact_email, '123-789-7890' as contact_phone, 'IT' as type
    UNION ALL
    SELECT 2, 'Contoso DevOps Services', '456 Industrial Road, Scooton City', 'Drew Rivera', 'drew.rivera@contoso.com', '987-654-3210', 'DevOps'
    UNION ALL
    SELECT 3, 'Lucerne Publishing', '789 Live Street, Woodgrove', 'Alex Kim', 'akim@lucernepublishing.com', '321-654-9870', 'Digital Publishing'
    UNION ALL
    SELECT 4, 'Wide World Engineering', '123 Innovation Drive, TechVille', 'Jamie Patel', 'jamie.patel@wideworldeng.com', '654-321-0987', 'IT'
    UNION ALL
    SELECT 5, 'Trey Research Inc', '456 Research Avenue, Redmond', 'Charlie Davis', 'charlie.davis@treyresearch.com', '789-012-3456', 'AI Services'
) as v
WHERE NOT EXISTS (SELECT 1 FROM vendors);


-- Status table: information about the status of a invoice, milestone, etc
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

-- Statement of work table; information about deliverables, milestones, or resource allocations.
CREATE TABLE IF NOT EXISTS sows (
    id BIGSERIAL PRIMARY KEY,
    number text NOT NULL,
    vendor_id BIGINT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    budget DECIMAL(18,2) NOT NULL,
    document text NOT NULL,
    metadata JSONB,
    FOREIGN KEY (vendor_id) REFERENCES vendors (id) ON DELETE CASCADE
);

-- Insert sow values only if the specific sow number does not exist
INSERT INTO sows (number, vendor_id, start_date, end_date, budget, document, metadata)
SELECT 'SOW-WoodgroveBank-2024-001',
       1, --TailWind Cloud Solutions
       '2024-11-01',
       '2025-12-31',
       43600.00,
       '1/sow/Statement_of_Work_TailWind_Cloud_Solutions_Woodgrove_Bank_20241101.pdf',
       '{}'
WHERE NOT EXISTS (SELECT 1 FROM sows WHERE number = 'SOW-WoodgroveBank-2024-001');

INSERT INTO sows (number, vendor_id, start_date, end_date, budget, document, metadata)
SELECT 'SOW-WoodgroveBank-001',
       2, --Contoso DevOps Services
       '2024-06-01',
       '2025-11-30',
       75000.00,
       '2/sow/Statement_of_Work_Contoso_DevOps_Services_Woodgrove_Bank_20240601.pdf',
       '{}'
WHERE NOT EXISTS (SELECT 1 FROM sows WHERE number = 'SOW-WoodgroveBank-001');

INSERT INTO sows (number, vendor_id, start_date, end_date, budget, document, metadata)
SELECT 'SOW-LP-WGB-001',
       3, -- Lucerne Publishing
       '2024-12-01',
       '2024-12-31',
       50000.00,
       '3/sow/Statement_of_Work_Lucerne_Publishing_Woodgrove_Bank_20241201.pdf',
       '{}'
WHERE NOT EXISTS (SELECT 1 FROM sows WHERE number = 'SOW-LP-WGB-001');

INSERT INTO sows (number, vendor_id, start_date, end_date, budget, document, metadata)
SELECT 'SOW-WoodgroveBank-WWE-001',
       4, --Wide World Engineering
       '2024-10-01',
       '2025-09-30',
       60000.00,
       '4/sow/Statement_of_Work_Wide_World_Engineering_Woodgrove_Bank_20241001.pdf',
       '{}'
WHERE NOT EXISTS (SELECT 1 FROM sows WHERE number = 'SOW-WoodgroveBank-WWE-001');

INSERT INTO sows (number, vendor_id, start_date, end_date, budget, document, metadata)
SELECT 'SOW-2024-WoodgroveBank-001',
       5, --Trey Research Inc
       '2024-05-01',
       '2025-08-31',
       45000.00,
       '5/sow/Statement_of_Work_Trey_Research_Inc_Woodgrove_Bank_20240501.pdf',
       '{}'
WHERE NOT EXISTS (SELECT 1 FROM sows WHERE number = 'SOW-2024-WoodgroveBank-001');

-- Invoices table; tax details, discounts, or additional metadata
CREATE TABLE IF NOT EXISTS invoices (
    id BIGSERIAL PRIMARY KEY,
    number text NOT NULL,
    vendor_id BIGINT NOT NULL,
    sow_id BIGINT NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    invoice_date DATE NOT NULL,
    payment_status VARCHAR(50) NOT NULL,
    document text NOT NULL,         -- document details
    content text,                   --  for invoice embeddings
    metadata JSONB,                 --  for additional metadata
    FOREIGN KEY (vendor_id) REFERENCES vendors (id) ON DELETE CASCADE,
    FOREIGN KEY (sow_id) REFERENCES sows (id) ON DELETE CASCADE
);


-- Insert starter data for invoices
INSERT INTO invoices (number, vendor_id, sow_id, amount, invoice_date, payment_status, document, content, metadata)
VALUES
    ('INV-TWC2024-001', 1, 1, 15600, '2024-11-08', 'Pending', 'https://stuemjxng3p6up6.blob.core.windows.net/documents/INV-TWC2024-001.pdf',  '{"Invoice Number": "INV-TWC2024-001", "Vendor": "TailWind Cloud Solutions", "Address": "789 Goldsmith Road, MainTown City", "Contact Name": "Morgan Skinner", "Contact Email": "morgan.skinner@tailwindcloud.com", "Contact Number": "123-789-7890", "SOW Number": "SOW-WoodgroveBank-2024-001", "Invoice Date": "2024-11-08", "Client": "Woodgrove Bank", "Address": "123 Financial Avenue, Woodgrove City", "Milestone Deliverables": [{"Amount": 8600.00, "Due Date": "2024-12-08", "Description": "Monitoring of resources"}, {"Amount": 7000.00, "Due Date": "2024-12-08", "Description": "Cost Management Implementation"}], "Total Amount": 15600.00, "Payment Terms": "Payment is due within 30 days of the invoice date. A penalty of 10% will be applied for late payments.", "Thank you": "Thank you for choosing TailWind Cloud Solutions"}', '{}'),
    ('INV-TWC2024-002', 1, 1, 7000, '2024-11-22', 'Pending', 'https://stuemjxng3p6up6.blob.core.windows.net/documents/INV-TWC2024-002.pdf', '{"Invoice Number": "INV-TWC2024-002", "Vendor": "TailWind Cloud Solutions", "Address": "789 Goldsmith Road, MainTown City", "Contact Name": "Morgan Skinner", "Contact Email": "morgan.skinner@tailwindcloud.com", "Contact Number": "123-789-7890", "SOW Number": "SOW-WoodgroveBank-2024-001", "Invoice Date": "2024-11-22", "Client": "Woodgrove Bank", "Address": "123 Financial Avenue, Woodgrove City", "Milestone Deliverables": [{"Amount": 7000.00, "Due Date": "2024-12-22", "Description": "Implementaion of automated scaling"}], "Total Amount": 7000.00, "Payment Terms": "Payment is due within 30 days of the invoice date. A penalty of 10% will be applied for late payments.", "Thank you": "Thank you for choosing TailWind Cloud Solutions"}', '{}'),
    ('INV-TWC2024-003', 1, 1, 12500, '2024-11-27', 'Pending', 'https://stuemjxng3p6up6.blob.core.windows.net/documents/INV-TWC2024-003.pdf',  '{"Invoice Number": "INV-TWC2024-003", "Vendor": "TailWind Cloud Solutions", "Address": "789 Goldsmith Road, MainTown City", "Contact Name": "Morgan Skinner", "Contact Email": "morgan.skinner@tailwindcloud.com", "Contact Number": "123-789-7890", "SOW Number": "SOW-WoodgroveBank-2024-001", "Invoice Date": "2024-11-27", "Client": "Woodgrove Bank", "Address": "123 Financial Avenue, Woodgrove City", "Milestone Deliverables": [{"Amount": 10500.00, "Due Date": "2024-12-27", "Description": "Maintenance and troubleshooting practices"}, {"Amount": 2000.00, "Due Date": "2024-12-27", "Description": "Identify Azure application issues"}], "Total Amount": 12500.00, "Payment Terms": "Payment is due within 30 days of the invoice date. A penalty of 10% will be applied for late payments.", "Thank you": "Thank you for choosing TailWind Cloud Solutions"}', '{}'),
    ('INV-TWC2024-004', 1, 1, 3500, '2024-11-30', 'Pending', 'https://stuemjxng3p6up6.blob.core.windows.net/documents/INV-TWC2024-004.pdf',  '{"Invoice Number": "INV-TWC2024-004", "Vendor": "TailWind Cloud Solutions", "Address": "789 Goldsmith Road, MainTown City", "Contact Name": "Morgan Skinner", "Contact Email": "morgan.skinner@tailwindcloud.com", "Contact Number": "123-789-7890", "SOW Number": "SOW-WoodgroveBank-2024-001", "Invoice Date": "2024-11-30", "Client": "Woodgrove Bank", "Address": "123 Financial Avenue, Woodgrove City", "Milestone Deliverables": [{"Amount": 3500.00, "Due Date": "2024-12-30", "Description": "Resolution of Azure application issues"}], "Total Amount": 3500.00, "Payment Terms": "Payment is due within 30 days of the invoice date. A penalty of 10% will be applied for late payments.", "Thank you": "Thank you for choosing TailWind Cloud Solutions"}', '{}'),
    ('INV-WWE2024-001', 5, 2, 36600, '2024-10-10', 'Pending', 'https://stuemjxng3p6up6.blob.core.windows.net/documents/INV-WWE2024-001.pdf',  '{"Invoice Number": "INV-WWE2024-001", "Vendor": "Wide World Engineering", "Address": "123 Innovation Drive, TechVille", "Contact Name": "Morgan Brown", "Contact Email": "morgan.brown@wideworldeng.com", "Contact Number": "555-967-8543", "SOW Number": "WWE-WoodgroveBank-SOW-001", "Invoice Date": "2024-10-10", "Client": "Woodgrove Bank", "Address": "123 Financial Avenue, Woodgrove City", "Milestone Deliverables": [{"Amount": 20100.00, "Due Date": "2024-11-10", "Description": "Design CI/CD Pipelines"}, {"Amount": 16500.00, "Due Date": "2024-11-10", "Description": "Initial setup of Cloud infrastructure monitoringg"}], "Total Amount": 36600.00, "Payment Terms": "Payment is due within 30 days of the invoice date. A penalty of 10% will be applied for late payments.", "Thank you": "Thank you for choosing Wide World Engineering"}', '{}');

-- Milestones table
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

-- Deliverables table
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
(5,'Identify Azure application issues','Completed', '2024-11-27'),
(5,'Resolution of Azure application issues','Completed', '2024-12-13'),
(6,'Design CI/CD pipelines','Completed', '2024-10-10'),
(8,'Initial setup of Cloud infrastructure monitoring','Completed', '2024-10-10');


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
(2,'Cost Management Implementation',7000,'Completed','2024-12-08'),
(3,'Implementation of automated scaling',7000,'Completed','2024-12-22'),
(4,'Maintenance and troubleshooting practices',10500,'Completed','2024-12-27'),
(5,'Identify Azure application issues',2000,'In Progress','2024-12-27'),
(5,'Resolution of Azure application issues',3500,'Completed','2024-12-30'),
(6,'Design CI/CD pipelines',20100,'Completed','2024-12-10'),
(8,'Initial setup of Cloud infrastructure monitoring',16500,'In Progress','2024-12-10');


CREATE TABLE IF NOT EXISTS sow_chunks (
    id BIGSERIAL PRIMARY KEY,
    sow_id BIGINT NOT NULL,
    heading text NOT NULL,
    content text NOT NULL,
    page_number INT NOT NULL,
    FOREIGN KEY (sow_id) REFERENCES sows (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS invoice_validation_results (
    id BIGSERIAL PRIMARY KEY,
    invoice_id BIGINT NOT NULL,
    datestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    result TEXT,
    validation_passed BOOLEAN,
    FOREIGN KEY (invoice_id) REFERENCES invoices (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sow_validation_results (
    id BIGSERIAL PRIMARY KEY,
    sow_id BIGINT NOT NULL,
    datestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    result TEXT,
    validation_passed BOOLEAN,
    FOREIGN KEY (sow_id) REFERENCES sows (id) ON DELETE CASCADE
);