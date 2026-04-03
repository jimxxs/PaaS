-- Schema
CREATE TABLE IF NOT EXISTS items (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    description VARCHAR(255)
);

-- Sample data
INSERT INTO items (name, description) VALUES
    ('Laptop',     'High-performance development laptop'),
    ('Monitor',    '27-inch 4K display'),
    ('Keyboard',   'Mechanical keyboard with RGB lighting');
