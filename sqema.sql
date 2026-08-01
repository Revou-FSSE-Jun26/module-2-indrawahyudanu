--1. Table users
CREATE TABLE users (
    user_id       SERIAL PRIMARY KEY,
    username      VARCHAR(50)    NOT NULL UNIQUE,
    email         VARCHAR(100)   NOT NULL UNIQUE,
    created_at    TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
);

--2. Table categories
CREATE TABLE categories (
    category_id  SERIAL PRIMARY KEY,
    name           VARCHAR(100)    NOT NULL UNIQUE
);

--3. Table products
CREATE TABLE products (
    product_id    SERIAL PRIMARY KEY,
    product_name  VARCHAR(100)   NOT NULL,
    price         DECIMAL(10, 2) NOT NULL,
    stock         INTEGER        NOT NULL,
    category_id   INTEGER        REFERENCES categories(category_id),
    created_at    TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
);

--4. Table orders
CREATE TABLE orders (
    order_id        SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES users(user_id),
    total_amount    NUMERIC (10, 2) NOT NULL
);

--5. table order_items
CREATE TABLE order_items (
    order_item_id  SERIAL PRIMARY KEY,
    order_id       INTEGER REFERENCES orders(order_id),
    product_id     INTEGER REFERENCES products(product_id),
    quantity       INTEGER NOT null,
    subtotal       numeric not null
);

INSERT INTO users (username, email) VALUES
('budi_santoso', 'budi@gmail.com'),
('siti_nurhaliza', 'siti@gmail.com'),
('andi_wijaya', 'andi@gmail.com'),
('dewi_lestari', 'dewi@gmail.com'),
('eko_prasetyo', 'eko@gmail.com');

-- 2. Isi Data Categories (Minimal 5 data)
INSERT INTO categories (name) VALUES
('Pakaian Pria'),
('Pakaian Wanita'),
('Elektronik'),
('Aksesoris'),
('Sepatu');

-- 3. Isi Data Products (Minimal 5 data)
INSERT INTO products (product_name, price, stock, category_id) VALUES
('Kaos Polos Hitam', 50000.00, 100, 1),
('Kemeja Batik', 150000.00, 50, 1),
('Gaun Casual', 200000.00, 30, 2),
('Earphone Bluetooth', 120000.00, 40, 4),
('Sepatu Sneakers', 350000.00, 25, 5);

-- 4. Isi Data Orders (Minimal 5 data)
INSERT INTO orders (user_id, total_amount) VALUES
(1, 200000.00),
(2, 350000.00),
(3, 50000.00),
(1, 120000.00),
(4, 200000.00);

-- 5. Isi Data Order Items (Minimal 5 data)
INSERT INTO order_items (order_id, product_id, quantity, subtotal) VALUES
(1, 1, 1, 50000.00),
(1, 2, 1, 150000.00),
(2, 5, 1, 350000.00),
(3, 1, 1, 50000.00),
(4, 4, 1, 120000.00);