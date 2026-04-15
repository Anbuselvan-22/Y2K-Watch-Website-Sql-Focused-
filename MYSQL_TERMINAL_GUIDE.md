# MySQL Terminal Commands Guide
## Y2K Watch E-Commerce Database

## 🔌 Connect to MySQL

```bash
mysql -u root -p
```
(Press Enter when prompted for password since it's empty)

## 📊 Basic Commands

```sql
-- Show all databases
SHOW DATABASES;

-- Select the database
USE login_db;

-- Show all tables
SHOW TABLES;

-- Exit MySQL
EXIT;
```

## 🔍 Quick View Queries

### View All Users
```sql
SELECT id, username, created_at FROM users;
```

### View All Products
```sql
SELECT id, name, price, stock_quantity, brand FROM products;
```

### View All Orders
```sql
SELECT o.id, u.username, o.total_amount, o.order_date, o.status
FROM orders o
JOIN users u ON o.user_id = u.id
ORDER BY o.order_date DESC;
```

### View Cart Contents
```sql
SELECT u.username, p.name, c.quantity, p.price
FROM cart c
JOIN users u ON c.user_id = u.id
JOIN products p ON c.product_id = p.id;
```

## 📈 Statistics Queries

### Total Revenue
```sql
SELECT SUM(total_amount) AS total_revenue FROM orders;
```

### Total Users
```sql
SELECT COUNT(*) AS total_users FROM users;
```

### Products in Stock
```sql
SELECT COUNT(*) AS in_stock_products 
FROM products 
WHERE stock_quantity > 0;
```

### Top Selling Products
```sql
SELECT p.name, SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.id
GROUP BY p.id, p.name
ORDER BY total_sold DESC;
```

## 🛠️ Update Queries

### Update Product Stock
```sql
UPDATE products SET stock_quantity = 30 WHERE id = 1;
```

### Update Order Status
```sql
UPDATE orders SET status = 'completed' WHERE id = 1;
```

### Update Product Price
```sql
UPDATE products SET price = 26000.00 WHERE id = 1;
```

## ➕ Insert Queries

### Add Product to Cart
```sql
INSERT INTO cart (user_id, product_id, quantity) 
VALUES (3, 1, 1);
```

### Add to Wishlist
```sql
INSERT INTO wishlist (user_id, product_id) 
VALUES (3, 2);
```

## 🗑️ Delete Queries

### Clear User's Cart
```sql
DELETE FROM cart WHERE user_id = 3;
```

### Remove from Wishlist
```sql
DELETE FROM wishlist WHERE user_id = 3 AND product_id = 1;
```

## 🔎 Search Queries

### Search Products by Name
```sql
SELECT * FROM products WHERE name LIKE '%Classic%';
```

### Search by Price Range
```sql
SELECT name, price FROM products 
WHERE price BETWEEN 10000 AND 30000;
```

### Search by Brand
```sql
SELECT * FROM products WHERE brand = 'Rolex';
```

## 📊 Advanced Reports

### User Order Summary
```sql
SELECT u.username, 
       COUNT(o.id) AS total_orders, 
       SUM(o.total_amount) AS total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.username
ORDER BY total_spent DESC;
```

### Monthly Sales
```sql
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
       COUNT(*) AS orders,
       SUM(total_amount) AS revenue
FROM orders
GROUP BY month
ORDER BY month DESC;
```

### Low Stock Alert
```sql
SELECT name, stock_quantity, price
FROM products
WHERE stock_quantity < 10
ORDER BY stock_quantity ASC;
```

## 💾 Backup & Restore

### Backup Database (Terminal)
```bash
mysqldump -u root -p login_db > backup_$(date +%Y%m%d).sql
```

### Restore Database (Terminal)
```bash
mysql -u root -p login_db < backup.sql
```

## 🎯 Useful One-Liners

```sql
-- Count all rows in each table
SELECT 'users' AS tbl, COUNT(*) AS cnt FROM users
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'cart', COUNT(*) FROM cart
UNION ALL SELECT 'wishlist', COUNT(*) FROM wishlist;

-- Show table sizes
SELECT table_name, 
       ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size_MB'
FROM information_schema.TABLES
WHERE table_schema = 'login_db';

-- Current database info
SELECT DATABASE() AS current_db, USER() AS current_user, NOW() AS current_time;
```

## 📝 Tips

1. **Always use semicolon (;)** at the end of SQL statements
2. **Use LIMIT** to prevent large result sets: `SELECT * FROM orders LIMIT 10;`
3. **Use transactions** for multiple related updates:
   ```sql
   START TRANSACTION;
   UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 1;
   INSERT INTO orders (user_id, total_amount) VALUES (1, 25000);
   COMMIT;
   ```
4. **Check before deleting**: Always run SELECT first to verify what you're about to delete
5. **Use EXPLAIN** to optimize queries: `EXPLAIN SELECT * FROM orders WHERE user_id = 1;`

## 🚀 Quick Access Script

Save this as `db.sh` for quick access:
```bash
#!/bin/bash
mysql -u root -p login_db
```

Make it executable:
```bash
chmod +x db.sh
./db.sh
```

---

For the complete list of queries, see `mysql_queries.sql`
