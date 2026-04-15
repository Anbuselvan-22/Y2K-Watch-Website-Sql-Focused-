-- ============================================================
-- Y2K WATCH E-COMMERCE - MySQL Terminal Queries
-- Database: login_db
-- ============================================================

-- ============================================================
-- BASIC DATABASE COMMANDS
-- ============================================================

-- Connect to MySQL
-- mysql -u root -p

-- Show all databases
SHOW DATABASES;

-- Use the login_db database
USE login_db;

-- Show all tables
SHOW TABLES;

-- ============================================================
-- TABLE STRUCTURE QUERIES
-- ============================================================

-- Show structure of a specific table
DESCRIBE users;
DESCRIBE products;
DESCRIBE orders;
DESCRIBE order_items;
DESCRIBE cart;
DESCRIBE wishlist;
DESCRIBE reviews;

-- Show detailed table information
SHOW CREATE TABLE users;
SHOW CREATE TABLE products;

-- ============================================================
-- SELECT QUERIES - VIEW DATA
-- ============================================================

-- View all users
SELECT * FROM users;

-- View all products with stock
SELECT id, name, price, stock_quantity, brand, category 
FROM products;

-- View products that are in stock
SELECT name, stock_quantity, price 
FROM products 
WHERE stock_quantity > 0;

-- View all orders
SELECT * FROM orders;

-- View orders with user information
SELECT o.id, u.username, o.total_amount, o.order_date, o.status
FROM orders o
JOIN users u ON o.user_id = u.id
ORDER BY o.order_date DESC;

-- View order details with items
SELECT o.id AS order_id, u.username, p.name AS product_name, 
       oi.quantity, oi.price, o.order_date
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
ORDER BY o.order_date DESC;

-- View cart items
SELECT u.username, p.name, c.quantity, p.price, 
       (c.quantity * p.price) AS total
FROM cart c
JOIN users u ON c.user_id = u.id
JOIN products p ON c.product_id = p.id;

-- View wishlist items
SELECT u.username, p.name, p.price, w.added_at
FROM wishlist w
JOIN users u ON w.user_id = u.id
JOIN products p ON w.product_id = p.id;

-- ============================================================
-- AGGREGATE QUERIES - STATISTICS
-- ============================================================

-- Count total users
SELECT COUNT(*) AS total_users FROM users;

-- Count total products
SELECT COUNT(*) AS total_products FROM products;

-- Count total orders
SELECT COUNT(*) AS total_orders FROM orders;

-- Total revenue
SELECT SUM(total_amount) AS total_revenue FROM orders;

-- Average order value
SELECT AVG(total_amount) AS avg_order_value FROM orders;

-- Orders by status
SELECT status, COUNT(*) AS count, SUM(total_amount) AS total
FROM orders
GROUP BY status;

-- Top selling products
SELECT p.name, SUM(oi.quantity) AS total_sold, 
       SUM(oi.quantity * oi.price) AS revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.id
GROUP BY p.id, p.name
ORDER BY total_sold DESC;

-- Products by stock level
SELECT name, stock_quantity, price
FROM products
ORDER BY stock_quantity DESC;

-- User order statistics
SELECT u.username, COUNT(o.id) AS total_orders, 
       SUM(o.total_amount) AS total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.username
ORDER BY total_spent DESC;

-- ============================================================
-- INSERT QUERIES - ADD DATA
-- ============================================================

-- Add a new user (password should be hashed in application)
INSERT INTO users (username, password) 
VALUES ('newuser', 'hashed_password_here');

-- Add a new product
INSERT INTO products (name, description, price, brand, category, 
                     image_url, stock_quantity) 
VALUES ('New Watch', 'Description here', 15000.00, 'Brand', 
        'Category', '/static/images/watch.jpg', 10);

-- Add item to cart
INSERT INTO cart (user_id, product_id, quantity) 
VALUES (1, 1, 1);

-- Add item to wishlist
INSERT INTO wishlist (user_id, product_id) 
VALUES (1, 2);

-- Create a new order
INSERT INTO orders (user_id, total_amount, status) 
VALUES (1, 25000.00, 'pending');

-- Add order items
INSERT INTO order_items (order_id, product_id, quantity, price) 
VALUES (1, 1, 1, 25000.00);

-- ============================================================
-- UPDATE QUERIES - MODIFY DATA
-- ============================================================

-- Update product stock
UPDATE products 
SET stock_quantity = 50 
WHERE id = 1;

-- Update product price
UPDATE products 
SET price = 26000.00 
WHERE id = 1;

-- Update order status
UPDATE orders 
SET status = 'completed' 
WHERE id = 1;

-- Update cart quantity
UPDATE cart 
SET quantity = 2 
WHERE id = 1;

-- Update multiple products stock
UPDATE products 
SET stock_quantity = stock_quantity + 10 
WHERE stock_quantity < 5;

-- ============================================================
-- DELETE QUERIES - REMOVE DATA
-- ============================================================

-- Delete from cart
DELETE FROM cart WHERE id = 1;

-- Delete from wishlist
DELETE FROM wishlist WHERE id = 1;

-- Clear user's cart
DELETE FROM cart WHERE user_id = 1;

-- Delete old pending orders (example: older than 30 days)
DELETE FROM orders 
WHERE status = 'pending' 
AND order_date < DATE_SUB(NOW(), INTERVAL 30 DAY);

-- ============================================================
-- SEARCH QUERIES
-- ============================================================

-- Search products by name
SELECT * FROM products 
WHERE name LIKE '%Classic%';

-- Search products by brand
SELECT * FROM products 
WHERE brand = 'Rolex';

-- Search products by price range
SELECT * FROM products 
WHERE price BETWEEN 10000 AND 30000;

-- Search orders by date range
SELECT * FROM orders 
WHERE order_date BETWEEN '2026-01-01' AND '2026-01-31';

-- Find users who haven't placed orders
SELECT u.id, u.username 
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;

-- ============================================================
-- ADVANCED QUERIES
-- ============================================================

-- Products with low stock (less than 10)
SELECT name, stock_quantity, price
FROM products
WHERE stock_quantity < 10
ORDER BY stock_quantity ASC;

-- Most valuable orders
SELECT o.id, u.username, o.total_amount, o.order_date
FROM orders o
JOIN users u ON o.user_id = u.id
ORDER BY o.total_amount DESC
LIMIT 10;

-- Products never ordered
SELECT p.id, p.name, p.price, p.stock_quantity
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
WHERE oi.id IS NULL;

-- Monthly sales report
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
       COUNT(*) AS total_orders,
       SUM(total_amount) AS total_revenue
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month DESC;

-- User activity summary
SELECT u.username,
       COUNT(DISTINCT o.id) AS total_orders,
       COUNT(DISTINCT c.id) AS cart_items,
       COUNT(DISTINCT w.id) AS wishlist_items
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
LEFT JOIN cart c ON u.id = c.user_id
LEFT JOIN wishlist w ON u.id = w.user_id
GROUP BY u.id, u.username;

-- ============================================================
-- MAINTENANCE QUERIES
-- ============================================================

-- Check table sizes
SELECT 
    table_name AS 'Table',
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.TABLES
WHERE table_schema = 'login_db'
ORDER BY (data_length + index_length) DESC;

-- Count rows in all tables
SELECT 'users' AS table_name, COUNT(*) AS row_count FROM users
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'cart', COUNT(*) FROM cart
UNION ALL
SELECT 'wishlist', COUNT(*) FROM wishlist
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews;

-- ============================================================
-- BACKUP AND RESTORE
-- ============================================================

-- Backup database (run in terminal, not in MySQL)
-- mysqldump -u root -p login_db > backup.sql

-- Restore database (run in terminal, not in MySQL)
-- mysql -u root -p login_db < backup.sql

-- ============================================================
-- USEFUL TIPS
-- ============================================================

-- Show current database
SELECT DATABASE();

-- Show current user
SELECT USER();

-- Show MySQL version
SELECT VERSION();

-- Show current date and time
SELECT NOW();

-- ============================================================
-- END OF QUERIES
-- ============================================================