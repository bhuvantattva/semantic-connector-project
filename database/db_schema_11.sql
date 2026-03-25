CREATE DATABASE raw_data_db;
USE raw_data_db;

CREATE TABLE raw_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(50),
    device_type VARCHAR(50),
    payload JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE DATABASE processed_data_db;
USE processed_data_db;

CREATE TABLE standardized_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(50) NOT NULL,
    device_type VARCHAR(50),
    temperature DECIMAL(10,2),
    energy_consumption DECIMAL(10,2),
    voltage DECIMAL(10,2),
    unit VARCHAR(20),
    motion_detected BOOLEAN,
    event_timestamp DATETIME,
    charging_power DECIMAL(10,2),
    vehicle_connected BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_device (device_id)
);
