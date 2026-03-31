INSERT INTO raw_device_data_table (device_id, device_type, raw_payload)
VALUES 

('dev001', 'smart_meter', JSON_OBJECT('power', 1500, 'voltage', 230)),
('dev002', 'thermostat', JSON_OBJECT('temperature', 22.5, 'unit', 'C')),
('dev003', 'camera', JSON_OBJECT('motion_detected', true, 'timestamp', '2026-03-24T10:00:00')),
('dev004', 'ev_charger', JSON_OBJECT('charging_power', 7200, 'vehicle_connected', true)),
('dev005', 'humidity_sensor', JSON_OBJECT('humidity', 60, 'unit', '%')),
('dev006', 'solar_inverter', JSON_OBJECT('power_output', 3500, 'status', 'active')),

('dev007', 'smart_light', JSON_OBJECT('brightness', 75, 'state', 'on')),
('dev008', 'thermostat', JSON_OBJECT('temperature', 21.0, 'unit', 'C')),
('dev009', 'door_lock', JSON_OBJECT('lock_status', 'locked', 'battery', 85)),
('dev010', 'smart_meter', JSON_OBJECT('power', 1800, 'voltage', 230)),
('dev011', 'camera', JSON_OBJECT('motion_detected', false, 'timestamp', '2026-03-24T11:30:00')),
('dev012', 'ev_charger', JSON_OBJECT('charging_power', 6800, 'vehicle_connected', false)),

('dev013', 'humidity_sensor', JSON_OBJECT('humidity', 55, 'unit', '%')),
('dev014', 'solar_inverter', JSON_OBJECT('power_output', 4200, 'status', 'active')),
('dev015', 'smart_light', JSON_OBJECT('brightness', 40, 'state', 'off')),
('dev016', 'thermostat', JSON_OBJECT('temperature', 23.2, 'unit', 'C')),
('dev017', 'smart_meter', JSON_OBJECT('power', 1200, 'voltage', 230)),
('dev018', 'solar_inverter', JSON_OBJECT('power_output', 3000, 'status', 'inactive')),

('dev019', 'humidity_sensor', JSON_OBJECT('humidity', 70, 'unit', '%')),
('dev020', 'ev_charger', JSON_OBJECT('charging_power', 7500, 'vehicle_connected', true));
