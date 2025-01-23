/*  File to idempotently load table DDL for Claims Data  */

-- Vendors table: information about companies (e.g., tags, industry codes, preferences)
CREATE TABLE IF NOT EXISTS vendors (
    id BIGSERIAL PRIMARY KEY,
    name text NOT NULL,
    address text NOT NULL,
    contact_name text NOT NULL,
    contact_email text NOT NULL,
    contact_phone text NOT NULL,
    type text NOT NULL,
    metadata jsonb -- additional information about the vendor
);

-- Insert vendor values
INSERT INTO vendors (name, address, contact_name, contact_email, contact_phone, type, metadata)
VALUES
    ('TailWind Cloud Solutions', '789 Goldsmith Road, MainTown City', 'Morgan Skinner', 'morgan.skinner@tailwindcloud.com', '123-789-7890', 'Cloud Services', '{}'),
    ('Contoso DevOps Services', '456 Industrial Road, Scooton City', 'Drew Rivera', 'drew.rivera@contoso.com', '987-654-3210', 'DevOps', '{}'),
    ('Lucerne Publishing', '789 Live Street, Woodgrove', 'Alex Kim', 'akim@lucernepublishing.com', '321-654-9870', 'Digital Publishing', '{}'),
    ('Wide World Engineering', '123 Innovation Drive, TechVille', 'Jamie Patel', 'jamie.patel@wideworldeng.com', '654-321-0987', 'Cloud Engineering', '{}'),
    ('Trey Research Inc', '456 Research Avenue, Redmond', 'Charlie Davis', 'charlie.davis@treyresearch.com', '789-012-3456', 'AI Services', '{}');



-- Status table: information about the status of a invoice, milestone, etc
DROP TABLE status;
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

-- Insert sow values

-- Insert sample data into sows table
-- Insert sample data into sows table
INSERT INTO sows (number, vendor_id, start_date, end_date, budget, document, metadata)
VALUES
    (
        'SOW-WoodgroveBank-2024-001',
        (SELECT id FROM vendors WHERE name = 'TailWind Cloud Solutions'),
        '2024-01-01',
        '2024-12-31',
        100000.00,
        'Statement_of_Work_TailWind_Cloud_Solutions_Woodgrove_Bank_20240101.pdf',
        '{}'
    ),
    (
        'WoodgroveBank-SOW-001',
        (SELECT id FROM vendors WHERE name = 'Contoso DevOps Services'),
        '2024-02-01',
        '2024-11-30',
        75000.00,
        'Statement_of_Work_Contoso_DevOps_Services_Woodgrove_Bank_20240201.pdf',
        '{}'
    ),
    (
        'SOW-LP-WGB-001',
        (SELECT id FROM vendors WHERE name = 'Lucerne Publishing'),
        '2024-03-01',
        '2024-10-31',
        50000.00,
        'Statement_of_Work_Lucerne_Publishing_Woodgrove_Bank_20240301.pdf',
        '{}'
    ),
    (
        'WWE-WoodgroveBank-SOW-001',
        (SELECT id FROM vendors WHERE name = 'Wide World Engineering'),
        '2024-04-01',
        '2024-09-30',
        60000.00,
        'Statement_of_Work_Wide_World_Engineering_Woodgrove_Bank_20240401.pdf',
        '{}'
    ),
    (
        'SOW-2024-WoodgroveBank-001',
        (SELECT id FROM vendors WHERE name = 'Trey Research Inc'),
        '2024-05-01',
        '2024-08-31',
        45000.00,
        'Statement_of_Work_Trey_Research_Inc_Woodgrove_Bank_20240501.pdf',
        '{}'
    );

-- Invoices table; tax details, discounts, or additional metadata
CREATE TABLE IF NOT EXISTS invoices (
    id BIGSERIAL PRIMARY KEY,
    number text NOT NULL,
    vendor_id BIGINT NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    invoice_date DATE NOT NULL,
    payment_status VARCHAR(50) NOT NULL,
    document text NOT NULL,
    metadata JSONB, -- Tax info, discounts, or itemized breakdown
    FOREIGN KEY (vendor_id) REFERENCES vendors (id) ON DELETE CASCADE
);

-- Milestones table
CREATE TABLE IF NOT EXISTS milestones (
    id BIGSERIAL PRIMARY KEY,
    sow_id BIGINT NOT NULL,
    name text NOT NULL,
    status VARCHAR(50) NOT NULL,
    due_date DATE,
    FOREIGN KEY (sow_id) REFERENCES sows (id) ON DELETE CASCADE
);

-- Deliverables table
CREATE TABLE IF NOT EXISTS deliverables (
    id BIGSERIAL PRIMARY KEY,
    milestone_id BIGINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    amount NUMERIC(10, 2),
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (milestone_id) REFERENCES milestones (id) ON DELETE CASCADE
);
