-- Schema di pantry per MariaDB.
-- Uso: mariadb -u pantry -p pantry < schema.sql

CREATE TABLE IF NOT EXISTS pantry_item (
    id         INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(120) NOT NULL,
    category   ENUM('secchi', 'scatolame', 'freschi', 'surgelati', 'spezie') NOT NULL,
    quantity   DECIMAL(10, 3) NOT NULL CHECK (quantity >= 0),
    unit       ENUM('g', 'kg', 'ml', 'l', 'pz') NOT NULL,
    expires_on DATE NULL,
    added_at   DATETIME NOT NULL DEFAULT UTC_TIMESTAMP(),
    INDEX ix_expires_on (expires_on)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
