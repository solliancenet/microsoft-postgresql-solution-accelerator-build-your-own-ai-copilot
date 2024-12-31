/*  File to load table DDL for Claims Data  */

-- Vendors table: information about companies (e.g., tags, industry codes, preferences)
DROP TABLE IF EXISTS vendors CASCADE;

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

TABLESPACE pg_default;

ALTER TABLE IF EXISTS vendors
    OWNER to "adminUser";

-- Statement of work table; information about deliverables, milestones, or resource allocations.

DROP TABLE IF EXISTS sows CASCADE;

CREATE TABLE sows (
    id BIGSERIAL PRIMARY KEY,
    title text NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    budget DECIMAL(18,2) NOT NULL,
    document text,
    details JSONB -- Flexible for deliverables, milestones, and notes
);

-- Invoices table; tax details, discounts, or additional metadata

DROP TABLE IF EXISTS invoices CASCADE;

CREATE TABLE invoices (
    id BIGSERIAL PRIMARY KEY,
    invoice_number text NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    invoice_date DATE NOT NULL,
    payment_status VARCHAR(50) NOT NULL,
    invoice_details JSONB -- Tax info, discounts, or itemized breakdown
);

-- MSA table; information about payment terms, special clauses, or additional legal notes
DROP TABLE IF EXISTS msas CASCADE;

CREATE TABLE msas (
    id BIGSERIAL PRIMARY KEY,
    title text NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    additional_info JSONB -- Stores special clauses, terms, etc.
);
