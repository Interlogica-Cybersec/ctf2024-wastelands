#!/bin/sh
DB_USER="factory"
DB_PASS="28c54be327974e5d"
DB_NAME="settings"

QUERY="
DROP TABLE IF EXISTS settings;
CREATE TABLE settings (
    name VARCHAR(255) NOT NULL,
    value VARCHAR(255) NOT NULL,
    PRIMARY KEY (name)
);
INSERT INTO settings (name, value) VALUES ('commercial_name', 'Kestrel');
INSERT INTO settings (name, value) VALUES ('model_name', 'K-72');
INSERT INTO settings (name, value) VALUES ('serial_number', 'KSTRL-012983');
INSERT INTO settings (name, value) VALUES ('status', 'initialization_required');
INSERT INTO settings (name, value) VALUES ('activation_code', 'D3f4ult-4c71v4T10n-C0d3');
"

mysql -u "$DB_USER" -p"$DB_PASS" -D "$DB_NAME" -e "$QUERY"
