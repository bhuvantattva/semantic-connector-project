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
    device_id VARCHAR(50),
    device_type VARCHAR(50),
    attribute_name VARCHAR(50),
    attribute_value VARCHAR(100),
    unit VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
