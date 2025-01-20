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
    metadata jsonb, -- additional information about the vendor
    embeddings vector(3072) -- embeddings for the vendor
);

-- Status table: information about the status of a invoice, milestone, etc
CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT
);
-- Insert default status values - if table hasn't been populated yet
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM status) THEN
        INSERT INTO status (id, name, description) VALUES (1, 'Pending', 'Awaiting action');
        INSERT INTO status (id, name, description) VALUES (2, 'In Progress', 'In progress');
        INSERT INTO status (id, name, description) VALUES (3, 'In Review', 'Review is required');
        INSERT INTO status (id, name, description) VALUES (4, 'Cancelled', 'The process was stopped');
        INSERT INTO status (id, name, description) VALUES (5, 'Overdue', 'The invoice has passed the due date without payment');
        INSERT INTO status (id, name, description) VALUES (6, 'Paid', 'The invoice has been fully paid');
        INSERT INTO status (id, name, description) VALUES (7, 'Completed', 'Work has been finished');
    END IF;
END $$;


CREATE TABLE IF NOT EXISTS msas (
    id BIGSERIAL PRIMARY KEY,
    title text NOT NULL,
    vendor_id BIGINT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    document text NOT NULL,
    metadata JSONB, -- Stores special clauses, terms, etc.
    embeddings vector(3072), -- embeddings for the vendor
    FOREIGN KEY (vendor_id) REFERENCES vendors(id) ON DELETE CASCADE
);

-- Statement of work table; information about deliverables, milestones, or resource allocations.
CREATE TABLE IF NOT EXISTS sows (
    id BIGSERIAL PRIMARY KEY,
    number text NOT NULL,
    msa_id BIGINT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    budget DECIMAL(18,2) NOT NULL,
    document text NOT NULL,
    FOREIGN KEY (msa_id) REFERENCES msas (id) ON DELETE CASCADE,
    metadata JSONB, -- Flexible for deliverables, milestones, and notes
    embeddings vector(3072) -- embeddings for the vendor
);

-- Invoices table; tax details, discounts, or additional metadata
CREATE TABLE IF NOT EXISTS invoices (
    id BIGSERIAL PRIMARY KEY,
    number text NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    invoice_date DATE NOT NULL,
    payment_status VARCHAR(50) NOT NULL,
    document text NOT NULL,
    metadata JSONB, -- Tax info, discounts, or itemized breakdown
    embeddings vector(3072) -- embeddings for the vendor
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
    id SERIAL PRIMARY KEY,
    milestone_id BIGINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    amount NUMERIC(10, 2),
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (milestone_id) REFERENCES milestones (id) ON DELETE CASCADE
);
