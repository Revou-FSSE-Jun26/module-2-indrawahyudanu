INSERT INTO users (username, email, role, password_hash, created_at) VALUES 
('Bambang_pamungkas', 'bambangp@email.com', 'customer', 'rahasia123', CURRENT_TIMESTAMP),
('budi_santoso', 'budi@email.com','customer', 'rahasia123', CURRENT_TIMESTAMP),
('siti_nurhaliza', 'siti@gmail.com','customer', 'rahasia123', CURRENT_TIMESTAMP),
('andi_wijaya', 'andi@gmail.com','customer', 'rahasia123', CURRENT_TIMESTAMP),
('dewi_lestari', 'dewi@gmail.com','customer', 'rahasia123', CURRENT_TIMESTAMP),
('eko_prasetyo', 'eko@gmail.com', 'customer', 'rahasia123', CURRENT_TIMESTAMP);


INSERT INTO categories (name) VALUES
('Pakaian Pria'),
('Pakaian Wanita'),
('Elektronik'),
('Aksesoris'),
('Sepatu');


INSERT INTO products (product_name, price, stock, category_id) VALUES
('Kaos Polos Hitam', 50000.00, 100, 1),
('Kemeja Batik', 150000.00, 50, 1),
('Gaun Casual', 200000.00, 30, 2),
('Earphone Bluetooth', 120000.00, 40, 4),
('Sepatu Sneakers', 350000.00, 25, 5);


INSERT INTO orders (user_id, total_amount) VALUES
(1, 200000.00),
(2, 350000.00),
(3, 50000.00),
(1, 120000.00),
(4, 200000.00);


INSERT INTO order_items (order_id, product_id, quantity, subtotal) VALUES
(1, 1, 1, 50000.00),
(1, 2, 1, 150000.00),
(2, 5, 1, 350000.00),
(3, 1, 1, 50000.00),
(4, 4, 1, 120000.00);
