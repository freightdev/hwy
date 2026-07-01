-- Seed data: loads companies, users, drivers, brokers, loads, invoices, documents, flows
-- This migration reads from the data/mock/ JSON files via Alembic data migration.

-- Companies
INSERT INTO companies (id, name, mc, dot, scac, type, role_type, founded, address, city, state, zip, phone, email, website, fleet_size, trailer_types, operating_states, description, score, score_factors, safety, safety_programs, authority, rating, review_count)
VALUES
(1, 'Conley Logistics LLC', 'MC-1234567', '3456789', 'CONL', 'For-Hire Carrier', 'carrier', '2018-05-18', '123 Logistics Way', 'Dallas', 'TX', '75001', '(214) 555-0196', 'info@conleylogistics.com', 'conleylogistics.com', 32, ARRAY['Dry Van', 'Flatbed', 'Reefer'], ARRAY['TX','OK','LA','AR','TN','GA','FL','AL','MS','NM','AZ','CA','IL','IN','OH','KY','MO','KS','NE','CO','UT','NV','OR','WA'], 'Full service logistics and transportation company specializing in dry van, flatbed, and reefer freight across 48 states.', 9.4, '{"safety_compliance": 9.8, "on_time_performance": 9.3, "driver_satisfaction": 9.3, "load_completion_rate": 9.5, "document_accuracy": 9.2, "claims_incidents": 8.7, "communication": 9.0}', '{"preventable_accidents": 1, "non_preventable_accidents": 1, "cargo_claims": 0, "claim_amount": "$3,250", "injuries": 0, "oos_vehicles": 2}', ARRAY['Drug & Alcohol Program', 'Driver Training Program', 'Vehicle Maintenance Program', 'Safety Meetings'], '{"usdot": "11284969", "issued": "2018-05-15", "status": "Active", "sms_score": "0.62", "oos_rate": "0.45", "driver_time": "0.14", "dangerous_goods": "0.0%"}', 4.8, 126)
ON CONFLICT (id) DO NOTHING;

-- Users
INSERT INTO users (id, company_id, name, email, phone, role, is_primary, password_hash)
VALUES
(1, 1, 'Jesse Conley', 'jesse@conleylogistics.com', '(214) 555-0100', 'Owner', TRUE, '$2b$12$PuMLpLJeB4LB3C5sMbyKTO3pmcTzVKqSYGsUx6huvfnuce3fjENdi'),
(2, 1, 'Mike Johnson', 'mike.j@conleylogistics.com', '(214) 555-0101', 'Dispatcher', FALSE, '$2b$12$PuMLpLJeB4LB3C5sMbyKTO3pmcTzVKqSYGsUx6huvfnuce3fjENdi'),
(3, 1, 'Sarah Williams', 'sarah.w@conleylogistics.com', '(214) 555-0102', 'Dispatcher', FALSE, '$2b$12$PuMLpLJeB4LB3C5sMbyKTO3pmcTzVKqSYGsUx6huvfnuce3fjENdi')
ON CONFLICT (id) DO NOTHING;

-- Drivers
INSERT INTO drivers (id, company_id, name, truck, phone, email, status, route, load_id, rate, license, doe, on_time, loads_completed, rating, cdl_class, cdl_state, home_base)
VALUES
(1, 1, 'Mike Smith', '#103', '(246) 555-0132', 'mike.smith@hwy.com', 'In Transit', 'Dallas, TX → Houston, TX', 'L10025', '$1,800', 'TX12345678', '2027-08-15', 100, 12, 4.9, 'Class A', 'TX', 'Dallas, TX'),
(2, 1, 'Sarah Johnson', '#105', '(312) 555-0198', 'sarah.j@hwy.com', 'Available', 'Atlanta, GA', 'L10026', '$2,200', 'GA87654321', '2026-03-22', 98, 8, 4.8, 'Class A', 'GA', 'Atlanta, GA'),
(3, 1, 'David Brown', '#107', '(901) 555-0177', 'david.b@hwy.com', 'At Pickup', 'Memphis, TN', 'L10027', '$1,800', 'TN11223344', '2025-11-30', 96, 15, 4.7, 'Class A', 'TN', 'Memphis, TN'),
(4, 1, 'Chris Parker', '#101', '(602) 555-0154', 'chris.p@hwy.com', 'At Delivery', 'Phoenix, AZ', 'L10028', '$1,700', 'AZ55667788', '2026-07-14', 94, 10, 4.6, 'Class A', 'AZ', 'Phoenix, AZ'),
(5, 1, 'Kevin Lee', '#109', '(312) 555-0213', 'kevin.l@hwy.com', 'In Transit', 'Chicago, IL → Detroit, MI', 'L10029', '$1,950', 'IL99887766', '2027-01-08', 97, 11, 4.7, 'Class A', 'IL', 'Chicago, IL'),
(6, 1, 'Maria Garcia', '#112', '(615) 555-0241', 'maria.g@hwy.com', 'Off Duty', 'Nashville, TN', NULL, '', 'TN44332211', '2026-09-19', 99, 14, 4.9, 'Class A', 'TN', 'Nashville, TN')
ON CONFLICT (id) DO NOTHING;

-- Brokers
INSERT INTO brokers (id, company_id, name, mc, status, loads, revenue, on_time, rating, credit, available, favorite, insurance, authority, website, email, phone)
VALUES
(1, 1, 'Landstar', 'MC24872', 'Active', 487, '$491,250', 98, 4.8, '$150,000', '$187,500', TRUE, TRUE, TRUE, 'landstar.com', 'dispatch@landstar.com', '(800) 555-0001'),
(2, 1, 'TQL', 'MC161760', 'Active', 128, '$203,924', 95, 4.5, '$75,000', '$62,000', TRUE, TRUE, TRUE, 'tql.com', 'dispatch@tql.com', '(800) 555-0002'),
(3, 1, 'DAT Freight & Analytics', 'MC172323', 'Active', 76, '$245,000', 97, 4.7, '$100,000', '$98,000', FALSE, TRUE, TRUE, 'dat.com', 'loads@dat.com', '(800) 555-0003'),
(4, 1, 'Cohnrac', 'MC187641', 'Active', 45, '$89,000', 92, 4.3, '$50,000', '$50,000', FALSE, TRUE, TRUE, 'cohnrac.com', 'dispatch@cohnrac.com', '(800) 555-0004'),
(5, 1, 'CH Robinson', 'MC220488', 'Active', 82, '$314,000', 91, 4.2, '$125,000', '$110,000', FALSE, TRUE, TRUE, 'chrobinson.com', 'services@chrobinson.com', '(800) 555-0005'),
(6, 1, 'Pele Lee', 'MC171A', '180 Day', 76, '$186,000', 89, 4.1, '$40,000', '$35,000', FALSE, FALSE, TRUE, 'pelelee.com', 'dispatch@pelelee.com', '(800) 555-0006'),
(7, 1, 'RXO', 'MC171A', 'Active', 43, '$167,000', 94, 4.4, '$80,000', '$75,000', FALSE, TRUE, TRUE, 'rxo.com', 'dispatch@rxo.com', '(800) 555-0007'),
(8, 1, 'Coyote Logistics', 'MC220488', 'Active', 31, '$98,000', 96, 4.6, '$60,000', '$58,000', FALSE, TRUE, TRUE, 'coyote.com', 'loads@coyote.com', '(800) 555-0008')
ON CONFLICT (id) DO NOTHING;

-- Loads
INSERT INTO loads (id, company_id, broker_id, driver_id, route, date, rate, rpm, miles, equipment, weight, broker_name, mc, pickup, delivery, stops, status, pickup_location, delivery_location)
VALUES
('L10025', 1, 1, 1, 'Dallas, TX → Houston, TX', 'Today', '$2,100', '$1.94', 239, '53'' Dry Van', '42,000 lbs', 'Landstar', 'MC24872', '7:00 AM', '3:00 PM', 1, 'In Transit', 'Dallas, TX', 'Houston, TX'),
('L10026', 1, 2, 2, 'Atlanta, GA → Tampa, FL', 'Today', '$2,450', '$2.18', 456, '48'' Flatbed', '38,500 lbs', 'TQL', 'MC161760', '8:30 AM', '6:00 PM', 1, 'Available', 'Atlanta, GA', 'Tampa, FL'),
('L10027', 1, 3, 3, 'Chicago, IL → Nashville, TN', 'Today', '$1,950', '$1.76', 476, 'Dry Van', '35,000 lbs', 'DAT', 'MC172323', '6:00 AM', '5:00 PM', 2, 'At Pickup', 'Chicago, IL', 'Nashville, TN'),
('L10028', 1, 5, 4, 'Memphis, TN → Dallas, TX', 'Today', '$2,000', '$1.88', 452, 'Reefer', '40,000 lbs', 'CH Robinson', 'MC220488', '9:00 AM', '7:00 PM', 1, 'At Delivery', 'Memphis, TN', 'Dallas, TX'),
('L10029', 1, 8, 5, 'Phoenix, AZ → Los Angeles, CA', 'Tomorrow', '$1,850', '$2.12', 373, 'Dry Van', '28,000 lbs', 'Coyote Logistics', 'MC220488', '6:00 AM', '2:00 PM', 1, 'In Transit', 'Phoenix, AZ', 'Los Angeles, CA'),
('L10030', 1, 1, NULL, 'Denver, CO → Salt Lake City, UT', 'Tomorrow', '$1,600', '$1.91', 525, 'Flatbed', '42,000 lbs', 'Landstar', 'MC24872', '7:00 AM', '5:00 PM', 1, 'Available', 'Denver, CO', 'Salt Lake City, UT')
ON CONFLICT (id) DO NOTHING;

-- Invoices
INSERT INTO invoices (id, company_id, broker_id, load_id, broker_name, amount, amount_cents, status, date, due_date)
VALUES
('INV-2025-1068', 1, 1, 'L10025', 'Landstar', '$4,250.00', 425000, 'Paid', '2025-05-25', '2025-06-24'),
('INV-2025-1065', 1, 2, 'L10026', 'TQL', '$3,850.00', 385000, 'Paid', '2025-05-22', '2025-06-21'),
('INV-2025-1064', 1, 8, 'L10027', 'Coyote Logistics', '$2,790.00', 279000, 'Sent', '2025-05-20', '2025-06-19'),
('INV-2025-1063', 1, 3, 'L10028', 'DAT Freight & Analytics', '$1,860.00', 186000, 'Overdue', '2025-05-10', '2025-06-09'),
('INV-2025-1062', 1, 5, 'L10029', 'CH Robinson', '$3,100.00', 310000, 'Paid', '2025-05-08', '2025-06-07'),
('INV-2025-1061', 1, 2, NULL, 'TQL', '$2,450.00', 245000, 'Paid', '2025-05-05', '2025-06-04')
ON CONFLICT (id) DO NOTHING;

-- Payments
INSERT INTO payments (id, company_id, from_broker, broker_id, amount, amount_cents, date, method, status, invoice_id)
VALUES
(1, 1, 'Landstar', 1, '+$4,250', 425000, '2025-05-26', 'ACH', 'Received', 'INV-2025-1068'),
(2, 1, 'TQL', 2, '+$3,850', 385000, '2025-05-23', 'ACH', 'Received', 'INV-2025-1065'),
(3, 1, 'CH Robinson', 5, '+$3,100', 310000, '2025-05-09', 'Wire', 'Received', 'INV-2025-1062'),
(4, 1, 'TQL', 2, '+$2,450', 245000, '2025-05-06', 'ACH', 'Received', 'INV-2025-1061')
ON CONFLICT (id) DO NOTHING;

-- Documents
INSERT INTO documents (id, company_id, name, category, expiry, status, icon, size)
VALUES
(1, 1, 'Insurance Certificate', 'Insurance', '2025-06-15', 'Valid', '🛡️', '245 KB'),
(2, 1, 'Cargo Insurance', 'Insurance', '2025-06-15', 'Valid', '🛡️', '198 KB'),
(3, 1, 'BMC-84 Insurance', 'Insurance', '2025-06-15', 'Valid', '🛡️', '312 KB'),
(4, 1, 'Operating Authority', 'Authority & Compliance', NULL, 'Valid', '⚖️', '89 KB'),
(5, 1, 'Safety Policy Manual', 'Safety & Policies', '2025-05-01', 'Valid', '⚠️', '1.2 MB'),
(6, 1, 'Driver Handbook', 'Safety & Policies', '2025-04-12', 'Valid', '📖', '892 KB'),
(7, 1, 'IFTA License', 'Permits & Licenses', '2025-12-31', 'Valid', '📋', '124 KB'),
(8, 1, 'IRP Registration', 'Permits & Licenses', '2025-12-31', 'Valid', '📋', '234 KB'),
(9, 1, 'Landstar Contract', 'Contracts', NULL, 'Active', '📝', '456 KB'),
(10, 1, 'W-9 Form', 'Tax & Finance', '2025-01-05', 'Valid', '💰', '67 KB')
ON CONFLICT (id) DO NOTHING;

-- Flows
INSERT INTO flows (id, company_id, name, steps, type, enabled, icon, category, step_details)
VALUES
(1, 1, 'Post-Delivery Workflow', 7, 'Auto', TRUE, '📦', 'Load Management', '[{"icon": "📥", "title": "Receive POD from Driver", "sub": "Trigger: Document Uploaded"}, {"icon": "✅", "title": "Validate POD", "sub": "Check document completeness"}, {"icon": "🔄", "title": "Update Load Status", "sub": "Mark as Delivered"}, {"icon": "📧", "title": "Notify Customer", "sub": "Send delivery notification"}, {"icon": "💰", "title": "Generate Invoice", "sub": "Create & send invoice"}, {"icon": "📁", "title": "Archive Documents", "sub": "Store in load folder"}]'),
(2, 1, 'Driver Check-In Flow', 5, 'Manual', FALSE, '🚛', 'Driver Communication', '[{"icon": "👤", "title": "Driver Starts Check-In", "sub": "Manual Trigger"}, {"icon": "📍", "title": "Capture Location", "sub": "Get current GPS location"}, {"icon": "✅", "title": "Confirm Appointment", "sub": "Verify pickup details"}, {"icon": "📡", "title": "Notify Dispatcher", "sub": "Send check-in notification"}, {"icon": "🔄", "title": "Update Load", "sub": "Mark as Checked In"}]'),
(3, 1, 'Invoice & Docs Flow', 6, 'Auto', TRUE, '📄', 'Billing & Invoicing', '[]'),
(4, 1, 'Emergency Call Flow', 3, 'Manual', FALSE, '🚨', 'Safety & Alerts', '[]'),
(5, 1, 'POD Upload Flow', 4, 'Auto', TRUE, '📋', 'Documents & Compliance', '[]'),
(6, 1, 'Load Assignment Flow', 6, 'Auto', TRUE, '🗂️', 'Dispatch Operations', '[]'),
(7, 1, 'Broker Update Flow', 4, 'Auto', FALSE, '🤝', 'Load Management', '[]')
ON CONFLICT (id) DO NOTHING;

-- Reset sequences
SELECT setval('companies_id_seq', (SELECT MAX(id) FROM companies));
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
SELECT setval('drivers_id_seq', (SELECT MAX(id) FROM drivers));
SELECT setval('brokers_id_seq', (SELECT MAX(id) FROM brokers));
SELECT setval('payments_id_seq', (SELECT MAX(id) FROM payments));
SELECT setval('documents_id_seq', (SELECT MAX(id) FROM documents));
SELECT setval('flows_id_seq', (SELECT MAX(id) FROM flows));
