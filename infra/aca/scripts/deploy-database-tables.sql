/*  File to idempotently load table DDL for Claims Data  */

-- Vendors table: information about companies (e.g., tags, industry codes, preferences)
CREATE TABLE IF NOT EXISTS vendors
(
    id BIGSERIAL PRIMARY KEY,
    name text NOT NULL,
    address text NOT NULL,
    contact_name text NOT NULL,
    contact_email text NOT NULL,
    contact_phone text NOT NULL,
    type text NOT NULL,
    metadata jsonb -- additional information about the vendor
)
ALTER TABLE IF EXISTS vendors
    OWNER to "adminUser";

-- Statement of work table; information about deliverables, milestones, or resource allocations.
CREATE TABLE IF NOT EXISTS sows (
    id BIGSERIAL PRIMARY KEY,
    title text NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    budget DECIMAL(18,2) NOT NULL,
    document text NOT NULL,
    details JSONB -- Flexible for deliverables, milestones, and notes
);
ALTER TABLE IF EXISTS sows
    OWNER to "adminUser";

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
ALTER TABLE IF EXISTS invoices
    OWNER to "adminUser";

-- MSA table; information about payment terms, special clauses, or additional legal notes
CREATE TABLE IF NOT EXISTS msas (
    id BIGSERIAL PRIMARY KEY,
    title text NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    additional_info JSONB -- Stores special clauses, terms, etc.
);
ALTER TABLE IF EXISTS msas
    OWNER to "adminUser";