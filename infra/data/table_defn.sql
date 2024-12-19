/*  File to load table DDL for Claims Data  */

-- Contract Companies table: information about companies (e.g., tags, industry codes, preferences)
CREATE TABLE Contract_Companies (
    company_id INT PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    contact_person VARCHAR(255),
    contact_email VARCHAR(255),
    metadata JSONB -- Additional dynamic attributes
);
