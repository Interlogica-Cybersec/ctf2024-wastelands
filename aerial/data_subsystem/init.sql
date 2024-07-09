USE sensors;
GRANT FILE ON *.* TO 'kestrel'@'%';
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS sensor_readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    reading VARCHAR(255) NOT NULL
);

INSERT INTO sensor_readings (name, reading) VALUES
    ('altimeter', '0 feet'),
    ('roll', '0 deg'),
    ('pitch', '0 deg'),
    ('yaw', '0 deg'),
    ('speed', '0 mph'),
    ('battery_level', '91%'),
    ('gps_coordinates', 'UNKNOWN');

GRANT ALL PRIVILEGES ON sensors.* TO 'kestrel'@'%';

CREATE DATABASE settings;
USE settings;

CREATE TABLE IF NOT EXISTS settings (
    name VARCHAR(255) NOT NULL,
    value VARCHAR(255) NOT NULL,
    PRIMARY KEY (name)
);
INSERT INTO settings (name, value) VALUES
    ('commercial_name', 'Kestrel'),
    ('model_name', 'K-72'),
    ('serial_number', 'KSTRL-012983'),
    ('status', 'activation_required'),
    ('activation_code', 'd36646fa-7b44-40a7-a0ac-e38618bad471');

CREATE USER 'factory'@'%' IDENTIFIED BY '28c54be327974e5d';
GRANT ALL PRIVILEGES ON settings.* TO 'factory'@'%';
FLUSH PRIVILEGES;
CREATE USER 'security'@'%' IDENTIFIED BY 'e9838f5e68811ce3';
GRANT ALL PRIVILEGES ON settings.* TO 'security'@'%';
FLUSH PRIVILEGES;
