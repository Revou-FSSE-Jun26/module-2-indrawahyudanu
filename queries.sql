SELECT 
    p.product_id, 
    p.product_name, 
    p.price, 
    p.stock, 
    c.category_name 
FROM products p
JOIN categories c ON p.category_id = c.category_id;

-- 2. Mencari produk dengan harga di atas 100.000 (WHERE)
SELECT * FROM products 
WHERE price > 100000.00;

-- 3. Menampilkan 3 produk termurah (ORDER BY + LIMIT)
SELECT * FROM products 
ORDER BY price ASC 
LIMIT 3;

-- 4. Menampilkan riwayat pesanan user beserta total belanjaannya (JOIN)
SELECT 
    o.order_id, 
    u.username, 
    o.order_date, 
    o.total_amount 
FROM orders o
JOIN users u ON o.user_id = u.user_id;