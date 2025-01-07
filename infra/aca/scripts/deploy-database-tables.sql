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

-- MSA table; information about payment terms, special clauses, or additional legal notes
CREATE TABLE IF NOT EXISTS msas (
    id BIGSERIAL PRIMARY KEY,
    title text NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    additional_info JSONB -- Stores special clauses, terms, etc.
);

-- Statement of work table; information about deliverables, milestones, or resource allocations.
CREATE TABLE IF NOT EXISTS sows (
    id BIGSERIAL PRIMARY KEY,
    sow_number text NOT NULL,
    msa_id BIGINT NOT NULL,
    msa_title text NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    budget DECIMAL(18,2) NOT NULL,
    document text NOT NULL,
    FOREIGN KEY (msa_id) REFERENCES msas (id) ON DELETE CASCADE,
    details JSONB -- Flexible for deliverables, milestones, and notes
);

-- Invoices table; tax details, discounts, or additional metadata
CREATE TABLE IF NOT EXISTS invoices (
    id BIGSERIAL PRIMARY KEY,
    invoice_number text NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    invoice_date DATE NOT NULL,
    payment_status VARCHAR(50) NOT NULL,
    document text NOT NULL,
    invoice_details JSONB -- Tax info, discounts, or itemized breakdown
);


-- Milestones table
CREATE TABLE IF NOT EXISTS milestones (
    id BIGSERIAL PRIMARY KEY,
    sow_id BIGINT NOT NULL,
    milestone_name text NOT NULL,
    milestone_status text NOT NULL,
    due_date DATE,
    FOREIGN KEY (sow_id) REFERENCES sows (id) ON DELETE CASCADE
);

-- Deliverables table
CREATE TABLE IF NOT EXISTS deliverables (
    id SERIAL PRIMARY KEY,
    milestone_id BIGINT NOT NULL,
    deliverable_name VARCHAR(100) NOT NULL,
    description TEXT,
    amount NUMERIC(10, 2),
    deliverable_status text NOT NULL,
    FOREIGN KEY (milestone_id) REFERENCES milestones (id) ON DELETE CASCADE
);
