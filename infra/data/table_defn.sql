/*  File to load table DDL for Claims Data  */

-- Contract Companies table: information about companies (e.g., tags, industry codes, preferences)
DROP TABLE IF EXISTS contract_companies;

CREATE TABLE contract_companies (
    company_id INT PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    contact_person VARCHAR(255),
    contact_email VARCHAR(255),
    metadata JSONB -- Additional dynamic attributes
);

-- MSA table; information about payment terms, special clauses, or additional legal notes


DROP TABLE IF EXISTS msas;

CREATE TABLE msas (
    msa_id INT PRIMARY KEY,
    msa_title VARCHAR(255),
    start_date DATE,
    end_date DATE,
    msa_document VARCHAR(255),
    additional_info JSONB -- Stores special clauses, terms, etc.
);

-- Statement of work table; information about deliverables, milestones, or resource allocations.

DROP TABLE IF EXISTS sows;

CREATE TABLE sows (
    sow_id INT PRIMARY KEY,
    sow_title VARCHAR(255),
    start_date DATE,
    end_date DATE,
    budget DECIMAL(18,2),
    sow_document VARCHAR(255),
    details JSONB -- Flexible for deliverables, milestones, and notes
);

-- Invoices table; tax details, discounts, or additional metadata

DROP TABLE IF EXISTS invoices;

CREATE TABLE invoices (
    invoice_id INT PRIMARY KEY,
    invoice_number VARCHAR(50),
    amount DECIMAL(18,2),
    invoice_date DATE,
    payment_status VARCHAR(50),
    invoice_details JSONB -- Tax info, discounts, or itemized breakdown
);
