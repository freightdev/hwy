-- HWY TMS Initial Schema
-- Creates all core tables for the transportation management system

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Companies (carrier/dispatch profiles)
CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL DEFAULT '',
    mc VARCHAR(50) DEFAULT '',
    dot VARCHAR(50) DEFAULT '',
    scac VARCHAR(10) DEFAULT '',
    type VARCHAR(50) DEFAULT 'For-Hire Carrier',
    role_type VARCHAR(20) DEFAULT 'carrier',
    founded VARCHAR(50) DEFAULT '',
    address VARCHAR(255) DEFAULT '',
    city VARCHAR(100) DEFAULT '',
    state VARCHAR(10) DEFAULT '',
    zip VARCHAR(20) DEFAULT '',
    phone VARCHAR(50) DEFAULT '',
    email VARCHAR(255) DEFAULT '',
    website VARCHAR(255) DEFAULT '',
    fleet_size INTEGER DEFAULT 0,
    trailer_types TEXT[] DEFAULT '{}',
    operating_states TEXT[] DEFAULT '{}',
    description TEXT DEFAULT '',
    score REAL DEFAULT 0,
    score_factors JSONB DEFAULT '{}',
    safety JSONB DEFAULT '{}',
    safety_programs TEXT[] DEFAULT '{}',
    authority JSONB DEFAULT '{}',
    rating REAL DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    show_mock_data BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Users (people within companies)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL DEFAULT '',
    email VARCHAR(255) DEFAULT '',
    phone VARCHAR(50) DEFAULT '',
    role VARCHAR(50) DEFAULT 'Owner',
    avatar VARCHAR(500) DEFAULT '',
    is_primary BOOLEAN DEFAULT FALSE,
    password_hash VARCHAR(255) DEFAULT '',
    device_id VARCHAR(255) DEFAULT '',
    location_lat DOUBLE PRECISION,
    location_lng DOUBLE PRECISION,
    user_agent VARCHAR(500) DEFAULT '',
    ip_address VARCHAR(45) DEFAULT '',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Drivers
CREATE TABLE IF NOT EXISTS drivers (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL DEFAULT '',
    truck VARCHAR(50) DEFAULT '',
    phone VARCHAR(50) DEFAULT '',
    email VARCHAR(255) DEFAULT '',
    status VARCHAR(50) DEFAULT 'Available',
    route TEXT DEFAULT '',
    load_id VARCHAR(50) DEFAULT NULL,
    rate VARCHAR(50) DEFAULT '',
    license VARCHAR(100) DEFAULT '',
    doe VARCHAR(50) DEFAULT '',
    on_time INTEGER DEFAULT 0,
    loads_completed INTEGER DEFAULT 0,
    rating REAL DEFAULT 0,
    cdl_class VARCHAR(20) DEFAULT 'Class A',
    cdl_state VARCHAR(10) DEFAULT '',
    home_base VARCHAR(255) DEFAULT '',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Brokers
CREATE TABLE IF NOT EXISTS brokers (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL DEFAULT '',
    mc VARCHAR(50) DEFAULT '',
    status VARCHAR(50) DEFAULT 'Active',
    loads INTEGER DEFAULT 0,
    revenue VARCHAR(50) DEFAULT '',
    on_time INTEGER DEFAULT 0,
    rating REAL DEFAULT 0,
    credit VARCHAR(50) DEFAULT '',
    available VARCHAR(50) DEFAULT '',
    favorite BOOLEAN DEFAULT FALSE,
    insurance BOOLEAN DEFAULT TRUE,
    authority BOOLEAN DEFAULT TRUE,
    website VARCHAR(255) DEFAULT '',
    email VARCHAR(255) DEFAULT '',
    phone VARCHAR(50) DEFAULT '',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Loads
CREATE TABLE IF NOT EXISTS loads (
    id VARCHAR(50) PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    broker_id INTEGER REFERENCES brokers(id) ON DELETE SET NULL,
    driver_id INTEGER REFERENCES drivers(id) ON DELETE SET NULL,
    route TEXT DEFAULT '',
    date VARCHAR(50) DEFAULT '',
    rate VARCHAR(50) DEFAULT '',
    rpm VARCHAR(50) DEFAULT '',
    miles INTEGER DEFAULT 0,
    equipment VARCHAR(100) DEFAULT '',
    weight VARCHAR(50) DEFAULT '',
    broker_name VARCHAR(255) DEFAULT '',
    mc VARCHAR(50) DEFAULT '',
    pickup VARCHAR(50) DEFAULT '',
    delivery VARCHAR(50) DEFAULT '',
    stops INTEGER DEFAULT 1,
    status VARCHAR(50) DEFAULT 'Available',
    pickup_location VARCHAR(255) DEFAULT '',
    delivery_location VARCHAR(255) DEFAULT '',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Invoices
CREATE TABLE IF NOT EXISTS invoices (
    id VARCHAR(50) PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    broker_id INTEGER REFERENCES brokers(id) ON DELETE SET NULL,
    load_id VARCHAR(50) REFERENCES loads(id) ON DELETE SET NULL,
    broker_name VARCHAR(255) DEFAULT '',
    amount VARCHAR(50) DEFAULT '',
    amount_cents BIGINT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'Sent',
    date VARCHAR(50) DEFAULT '',
    due_date VARCHAR(50) DEFAULT '',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Payments
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    from_broker VARCHAR(255) DEFAULT '',
    broker_id INTEGER REFERENCES brokers(id) ON DELETE SET NULL,
    amount VARCHAR(50) DEFAULT '',
    amount_cents BIGINT DEFAULT 0,
    date VARCHAR(50) DEFAULT '',
    method VARCHAR(50) DEFAULT 'ACH',
    status VARCHAR(50) DEFAULT 'Received',
    invoice_id VARCHAR(50) REFERENCES invoices(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Documents
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL DEFAULT '',
    category VARCHAR(100) DEFAULT '',
    expiry VARCHAR(50) DEFAULT NULL,
    status VARCHAR(50) DEFAULT 'Valid',
    icon VARCHAR(10) DEFAULT '📄',
    size VARCHAR(20) DEFAULT '',
    file_url TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Flows (automation workflows)
CREATE TABLE IF NOT EXISTS flows (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL DEFAULT '',
    steps INTEGER DEFAULT 0,
    type VARCHAR(50) DEFAULT 'Manual',
    enabled BOOLEAN DEFAULT FALSE,
    icon VARCHAR(10) DEFAULT '⚡',
    category VARCHAR(100) DEFAULT '',
    step_details JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_company ON users(company_id);
CREATE INDEX idx_drivers_company ON drivers(company_id);
CREATE INDEX idx_drivers_status ON drivers(status);
CREATE INDEX idx_brokers_company ON brokers(company_id);
CREATE INDEX idx_loads_company ON loads(company_id);
CREATE INDEX idx_loads_status ON loads(status);
CREATE INDEX idx_invoices_company ON invoices(company_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_payments_company ON payments(company_id);
CREATE INDEX idx_documents_company ON documents(company_id);
CREATE INDEX idx_flows_company ON flows(company_id);
