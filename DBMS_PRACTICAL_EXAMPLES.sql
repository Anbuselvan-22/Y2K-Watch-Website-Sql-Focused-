-- ============================================================
-- DBMS REVIEW 3 - PRACTICAL SQL EXAMPLES
-- Topics: Normalization, Transactions, Concurrency Control
-- Database: Y2K Watch E-commerce (login_db)
-- ============================================================

-- ============================================================
-- SECTION 1: NORMALIZATION EXAMPLES
-- ============================================================

-- Example 1: Unnormalized to 1NF
-- BEFORE (Unnormalized - Multiple values in one column)
/*
CREATE TABLE orders_bad (
    order_id INT,
    customer_name VARCHAR(100),
    products VARCHAR(500)  -- "Watch1, Watch2, Watch3"
);
*/

-- AFTER (1NF - Atomic values)
CREATE TABLE orders_1nf (
    order_id INT,
    customer_name VARCHAR(100),
    product_name VARCHAR(100),
    PRIMARY KEY (order_id, product_name)
);

-- Example 2: 1NF to 2NF
-- BEFORE (1NF but has partial dependency)
/*
CREATE TABLE order_details_1nf (
    order_id INT,
    product_id INT,
    product_name VARCHAR(100),  -- Depends only on product_id
    product_price DECIMAL(10,2), -- Depends only on product_id
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);
*/

-- AFTER (2NF - No partial dependencies)
CREATE TABLE order_items_2nf (
    order_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE products_2nf (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    product_price DECIMAL(10,2)
);

-- Example 3: 2NF to 3NF
-- BEFORE (2NF but has transitive dependency)
/*
CREATE TABLE orders_2nf (
    order_id INT PRIMARY KEY,
    customer_id INT,
    customer_name VARCHAR(100),  -- Depends on customer_id (transitive)
    customer_city VARCHAR(100),  -- Depends on customer_id (transitive)
    order_total DECIMAL(10,2)
);
*/

-- AFTER (3NF - No transitive dependencies)
CREATE TABLE orders_3nf (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_total DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE customers_3nf (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_city VARCHAR(100)
);

-- ============================================================
-- SECTION 2: TRANSACTION EXAMPLES
-- ============================================================

-- Example 1: Basic Transaction
START TRANSACTION;
INSERT INTO users (username, password) VALUES ('john_doe', 'hashed_password');
INSERT INTO orders (user_id, total_amount) VALUES (LAST_INSERT_ID(), 25000.00);
COMMIT;

-- Example 2: Transaction with Rollback
START TRANSACTION;
UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 1;
-- Check if stock went negative
SELECT stock_quantity INTO @stock FROM products WHERE id = 1;
IF @stock < 0 THEN
    ROLLBACK;
ELSE
    COMMIT;
END IF;

-- Example 3: Complete Order Placement Transaction
DELIMITER //
CREATE PROCEDURE place_order(
    IN p_user_id INT,
    IN p_product_id INT,
    IN p_quantity INT
)
BEGIN
    DECLARE v_stock INT;
    DECLARE v_price DECIMAL(10,2);
    DECLARE v_total DECIMAL(10,2);
    DECLARE v_order_id INT;
    
    -- Start transaction
    START TRANSACTION;
    
    -- Lock and check stock
    SELECT stock_quantity, price INTO v_stock, v_price
    FROM products
    WHERE id = p_product_id
    FOR UPDATE;
    
    -- Verify sufficient stock
    IF v_stock >= p_quantity THEN
        -- Calculate total
        SET v_total = v_price * p_quantity;
        
        -- Reduce stock
        UPDATE products
        SET stock_quantity = stock_quantity - p_quantity
        WHERE id = p_product_id;
        
        -- Create order
        INSERT INTO orders (user_id, total_amount, status)
        VALUES (p_user_id, v_total, 'pending');
        
        SET v_order_id = LAST_INSERT_ID();
        
        -- Add order items
        INSERT INTO order_items (order_id, product_id, quantity, price)
        VALUES (v_order_id, p_product_id, p_quantity, v_price);
        
        -- Clear from cart
        DELETE FROM cart
        WHERE user_id = p_user_id AND product_id = p_product_id;
        
        COMMIT;
        SELECT 'Order placed successfully' AS message, v_order_id AS order_id;
    ELSE
        ROLLBACK;
        SELECT 'Insufficient stock' AS message;
    END IF;
END //
DELIMITER ;

-- Example 4: Transaction with Savepoints
START TRANSACTION;

-- Create order
INSERT INTO orders (user_id, total_amount, status)
VALUES (3, 50000.00, 'pending');
SAVEPOINT order_created;

-- Add first item
INSERT INTO order_items (order_id, product_id, quantity, price)
VALUES (LAST_INSERT_ID(), 1, 1, 25000.00);
SAVEPOINT first_item_added;

-- Add second item
INSERT INTO order_items (order_id, product_id, quantity, price)
VALUES (LAST_INSERT_ID(), 2, 1, 25000.00);
SAVEPOINT second_item_added;

-- If second item fails, rollback to first item
-- ROLLBACK TO first_item_added;

-- Or commit everything
COMMIT;

-- Example 5: Money Transfer Transaction (Classic Example)
DELIMITER //
CREATE PROCEDURE transfer_money(
    IN from_account INT,
    IN to_account INT,
    IN amount DECIMAL(10,2)
)
BEGIN
    DECLARE from_balance DECIMAL(10,2);
    
    START TRANSACTION;
    
    -- Lock and get sender's balance
    SELECT balance INTO from_balance
    FROM accounts
    WHERE account_id = from_account
    FOR UPDATE;
    
    -- Check sufficient balance
    IF from_balance >= amount THEN
        -- Deduct from sender
        UPDATE accounts
        SET balance = balance - amount
        WHERE account_id = from_account;
        
        -- Add to receiver
        UPDATE accounts
        SET balance = balance + amount
        WHERE account_id = to_account;
        
        COMMIT;
        SELECT 'Transfer successful' AS message;
    ELSE
        ROLLBACK;
        SELECT 'Insufficient balance' AS message;
    END IF;
END //
DELIMITER ;

-- ============================================================
-- SECTION 3: CONCURRENCY CONTROL EXAMPLES
-- ============================================================

-- Example 1: Demonstrating Lost Update Problem
-- Transaction 1
START TRANSACTION;
SELECT stock_quantity INTO @stock1 FROM products WHERE id = 1;
-- Simulate delay
SELECT SLEEP(2);
UPDATE products SET stock_quantity = @stock1 - 1 WHERE id = 1;
COMMIT;

-- Transaction 2 (run concurrently)
START TRANSACTION;
SELECT stock_quantity INTO @stock2 FROM products WHERE id = 1;
UPDATE products SET stock_quantity = @stock2 - 1 WHERE id = 1;
COMMIT;
-- Result: Lost update! One update is lost

-- Solution: Use FOR UPDATE
-- Transaction 1 (Correct)
START TRANSACTION;
SELECT stock_quantity FROM products WHERE id = 1 FOR UPDATE;
UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 1;
COMMIT;

-- Transaction 2 (Correct - will wait for T1 to complete)
START TRANSACTION;
SELECT stock_quantity FROM products WHERE id = 1 FOR UPDATE;
UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 1;
COMMIT;

-- Example 2: Isolation Levels

-- READ UNCOMMITTED (Can read dirty data)
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
START TRANSACTION;
SELECT * FROM products WHERE id = 1;  -- Can see uncommitted changes
COMMIT;

-- READ COMMITTED (Default - No dirty reads)
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
SELECT * FROM products WHERE id = 1;  -- Only sees committed data
-- Another transaction updates and commits
SELECT * FROM products WHERE id = 1;  -- Sees new value (non-repeatable read)
COMMIT;

-- REPEATABLE READ (No dirty reads, no non-repeatable reads)
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
SELECT * FROM products WHERE id = 1;  -- Reads value
-- Another transaction updates and commits
SELECT * FROM products WHERE id = 1;  -- Sees same value (repeatable)
COMMIT;

-- SERIALIZABLE (Strictest - No dirty, non-repeatable, or phantom reads)
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
START TRANSACTION;
SELECT * FROM products WHERE stock_quantity < 10;
-- Other transactions cannot insert/update/delete matching rows
COMMIT;

-- Example 3: Shared vs Exclusive Locks

-- Shared Lock (Multiple readers allowed)
START TRANSACTION;
SELECT * FROM products WHERE id = 1 LOCK IN SHARE MODE;
-- Other transactions can also read with shared lock
-- But cannot write (exclusive lock)
COMMIT;

-- Exclusive Lock (Only one writer allowed)
START TRANSACTION;
SELECT * FROM products WHERE id = 1 FOR UPDATE;
-- Other transactions cannot read or write
UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 1;
COMMIT;

-- Example 4: Deadlock Scenario

-- Transaction 1
START TRANSACTION;
UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 1;  -- Lock product 1
SELECT SLEEP(2);  -- Simulate delay
UPDATE orders SET status = 'completed' WHERE id = 1;  -- Try to lock order 1
COMMIT;

-- Transaction 2 (run concurrently)
START TRANSACTION;
UPDATE orders SET status = 'completed' WHERE id = 1;  -- Lock order 1
UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 1;  -- Try to lock product 1
COMMIT;
-- Result: DEADLOCK! MySQL will detect and rollback one transaction

-- Solution: Always acquire locks in same order
-- Transaction 1 (Correct)
START TRANSACTION;
UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 1;  -- Lock product first
UPDATE orders SET status = 'completed' WHERE id = 1;  -- Then lock order
COMMIT;

-- Transaction 2 (Correct)
START TRANSACTION;
UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 2;  -- Lock product first
UPDATE orders SET status = 'completed' WHERE id = 2;  -- Then lock order
COMMIT;

-- Example 5: Preventing Phantom Reads

-- Transaction 1 (REPEATABLE READ - Phantom reads possible)
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
SELECT COUNT(*) FROM orders WHERE status = 'pending';  -- Returns 5
-- Transaction 2 inserts a new pending order
SELECT COUNT(*) FROM orders WHERE status = 'pending';  -- Still returns 5 (in MySQL InnoDB)
COMMIT;

-- Transaction 1 (SERIALIZABLE - No phantom reads)
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
START TRANSACTION;
SELECT COUNT(*) FROM orders WHERE status = 'pending';  -- Returns 5
-- Transaction 2 tries to insert but is blocked
SELECT COUNT(*) FROM orders WHERE status = 'pending';  -- Still returns 5
COMMIT;

-- ============================================================
-- SECTION 4: PRACTICAL SCENARIOS
-- ============================================================

-- Scenario 1: Add to Cart with Concurrency Control
DELIMITER //
CREATE PROCEDURE add_to_cart(
    IN p_user_id INT,
    IN p_product_id INT,
    IN p_quantity INT
)
BEGIN
    DECLARE v_stock INT;
    
    START TRANSACTION;
    
    -- Check stock with lock
    SELECT stock_quantity INTO v_stock
    FROM products
    WHERE id = p_product_id
    FOR UPDATE;
    
    IF v_stock >= p_quantity THEN
        -- Add to cart or update quantity
        INSERT INTO cart (user_id, product_id, quantity)
        VALUES (p_user_id, p_product_id, p_quantity)
        ON DUPLICATE KEY UPDATE quantity = quantity + p_quantity;
        
        COMMIT;
        SELECT 'Added to cart' AS message;
    ELSE
        ROLLBACK;
        SELECT 'Insufficient stock' AS message;
    END IF;
END //
DELIMITER ;

-- Scenario 2: Checkout Process
DELIMITER //
CREATE PROCEDURE checkout(IN p_user_id INT)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_product_id INT;
    DECLARE v_quantity INT;
    DECLARE v_price DECIMAL(10,2);
    DECLARE v_stock INT;
    DECLARE v_total DECIMAL(10,2) DEFAULT 0;
    DECLARE v_order_id INT;
    
    DECLARE cart_cursor CURSOR FOR
        SELECT c.product_id, c.quantity, p.price
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = p_user_id;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    START TRANSACTION;
    
    -- Create order
    INSERT INTO orders (user_id, total_amount, status)
    VALUES (p_user_id, 0, 'pending');
    SET v_order_id = LAST_INSERT_ID();
    
    -- Process each cart item
    OPEN cart_cursor;
    read_loop: LOOP
        FETCH cart_cursor INTO v_product_id, v_quantity, v_price;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Check and lock stock
        SELECT stock_quantity INTO v_stock
        FROM products
        WHERE id = v_product_id
        FOR UPDATE;
        
        IF v_stock >= v_quantity THEN
            -- Reduce stock
            UPDATE products
            SET stock_quantity = stock_quantity - v_quantity
            WHERE id = v_product_id;
            
            -- Add order item
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (v_order_id, v_product_id, v_quantity, v_price);
            
            -- Update total
            SET v_total = v_total + (v_quantity * v_price);
        ELSE
            -- Insufficient stock, rollback everything
            CLOSE cart_cursor;
            ROLLBACK;
            SELECT 'Insufficient stock for some items' AS message;
            LEAVE read_loop;
        END IF;
    END LOOP;
    CLOSE cart_cursor;
    
    IF NOT done THEN
        -- Update order total
        UPDATE orders SET total_amount = v_total WHERE id = v_order_id;
        
        -- Clear cart
        DELETE FROM cart WHERE user_id = p_user_id;
        
        COMMIT;
        SELECT 'Checkout successful' AS message, v_order_id AS order_id;
    END IF;
END //
DELIMITER ;

-- Scenario 3: Update Product Stock (Batch)
DELIMITER //
CREATE PROCEDURE restock_products()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Restock failed' AS message;
    END;
    
    START TRANSACTION;
    
    -- Add 10 units to all products with low stock
    UPDATE products
    SET stock_quantity = stock_quantity + 10
    WHERE stock_quantity < 5;
    
    -- Log the restock operation
    INSERT INTO stock_logs (operation, timestamp)
    VALUES ('Restock low inventory', NOW());
    
    COMMIT;
    SELECT 'Restock successful' AS message;
END //
DELIMITER ;

-- ============================================================
-- SECTION 5: TESTING QUERIES
-- ============================================================

-- Test 1: View current isolation level
SELECT @@transaction_isolation;

-- Test 2: Check for locks
SELECT * FROM information_schema.innodb_locks;

-- Test 3: View running transactions
SELECT * FROM information_schema.innodb_trx;

-- Test 4: Check deadlock information
SHOW ENGINE INNODB STATUS;

-- Test 5: Simulate concurrent updates
-- Run these in two separate MySQL sessions simultaneously

-- Session 1:
START TRANSACTION;
UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 1;
SELECT SLEEP(5);
COMMIT;

-- Session 2 (run while Session 1 is sleeping):
START TRANSACTION;
UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 1;
-- This will wait for Session 1 to commit
COMMIT;

-- ============================================================
-- SECTION 6: CLEANUP
-- ============================================================

-- Drop test procedures
DROP PROCEDURE IF EXISTS place_order;
DROP PROCEDURE IF EXISTS transfer_money;
DROP PROCEDURE IF EXISTS add_to_cart;
DROP PROCEDURE IF EXISTS checkout;
DROP PROCEDURE IF EXISTS restock_products;

-- ============================================================
-- END OF PRACTICAL EXAMPLES
-- ============================================================