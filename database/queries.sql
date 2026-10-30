
--1. show table users, products, orders.
select * from users; 
select * from products;
select * from orders;

--2. show data price product more than 100000.
SELECT * FROM products 
WHERE price > 100000.00;

--3. Display the 3 cheapest product, max 3 data 
SELECT * FROM products 
ORDER BY price ASC 
LIMIT 3;
