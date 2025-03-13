-- Ensure database is fresh
DROP TABLE IF EXISTS maintenance_logs;
DROP TABLE IF EXISTS machines;
DROP TABLE IF EXISTS areas;

-- Create Areas Table
CREATE TABLE areas (
    area_id SERIAL PRIMARY KEY,
    area_name VARCHAR(100) UNIQUE NOT NULL
);

-- Create Machines Table
CREATE TABLE machines (
    machine_id SERIAL PRIMARY KEY,
    area_id INT NOT NULL,
    machine_name VARCHAR(100) NOT NULL,
    asset_number VARCHAR(50) UNIQUE NOT NULL,
    location VARCHAR(255),
    last_maintenance_date VARCHAR(50),
    FOREIGN KEY (area_id) REFERENCES areas(area_id) ON DELETE CASCADE
);

-- Create Maintenance Logs Table
CREATE TABLE maintenance_logs (
    log_id SERIAL PRIMARY KEY,
    machine_id INT NOT NULL,
    technician_name VARCHAR(100) NOT NULL,
    date VARCHAR(50) DEFAULT CURRENT_DATE,
    total_time_spent FLOAT NOT NULL,
    comments TEXT,
    parts_used TEXT,  -- Store parts as a JSON string (for flexibility)
    FOREIGN KEY (machine_id) REFERENCES machines(machine_id) ON DELETE CASCADE
);

-- Insert Sample Data
INSERT INTO areas (area_name) VALUES ('Assembly Line'), ('Paint Booth'), ('Welding Station');

INSERT INTO machines (area_id, machine_name, asset_number, location, last_maintenance_date) VALUES
(1, 'Hydraulic Press', 'HP-001', 'North Wall', '2025-03-01'),
(2, 'Spray Booth', 'SB-004', 'South Corner', '2025-02-25'),
(3, 'Welding Rig', 'WR-008', 'East Bay', '2025-03-05');

INSERT INTO maintenance_logs (machine_id, technician_name, total_time_spent, comments, parts_used) VALUES
(1, 'John Doe', 1.5, 'Replaced hydraulic seals.', '{"part_name": "Seal Kit", "part_number": "SK-450"}'),
(2, 'Jane Smith', 2.0, 'Cleaned spray nozzles.', '{"part_name": "Nozzle Cleaner", "part_number": "NC-200"}'),
(3, 'Mike Johnson', 3.0, 'Checked welding electrodes.', '{"part_name": "Electrode Set", "part_number": "ES-100"}');

