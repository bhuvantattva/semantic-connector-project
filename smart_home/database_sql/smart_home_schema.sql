CREATE DATABASE smart_home;

USE smart_home;

CREATE TABLE raw_device_data_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(50),
    device_type VARCHAR(50),
    raw_payload JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE processed_device_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entity_id VARCHAR(100),
    entity_type VARCHAR(50),
    attribute_name VARCHAR(50),
    attribute_value VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
