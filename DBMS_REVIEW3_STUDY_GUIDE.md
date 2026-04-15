# DBMS Review 3 - Study Guide
## Topics: Normalization, Transaction, and Concurrency Control
### Date: 13.04.2026 to 20.04.2026
### Chapters 4 and 5

---

## 📚 Table of Contents
1. [Normalization](#normalization)
2. [Transactions](#transactions)
3. [Concurrency Control](#concurrency-control)
4. [Practical Examples](#practical-examples)
5. [Practice Questions](#practice-questions)

---

## 1️⃣ NORMALIZATION

### 🎯 What is Normalization?
Normalization is the process of organizing data in a database to reduce redundancy and improve data integrity.

### 📊 Normal Forms

#### **1NF (First Normal Form)**
**Rules:**
- Each column contains atomic (indivisible) values
- Each column contains values of a single type
- Each column has a unique name
- Order doesn't matter

**Example - BEFORE 1NF (Bad):**
```
Orders Table:
order_id | customer_name | products
---------|---------------|------------------
1        | John          | Watch1, Watch2
2        | Mary          | Watch3
```

**AFTER 1NF (Good):**
```
Orders Table:
order_id | customer_name | product
---------|---------------|----------
1        | John          | Watch1
1        | John          | Watch2
2        | Mary          | Watch3
```

#### **2NF (Second Normal Form)**
**Rules:**
- Must be in 1NF
- No partial dependencies (all non-key attributes fully depend on primary key)

**Example - BEFORE 2NF (Bad):**
```
OrderItems Table:
order_id | product_id | product_name | price | quantity
---------|------------|--------------|-------|----------
1        | 101        | Rolex        | 25000 | 1
1        | 102        | Omega        | 12500 | 2
```
*Problem: product_name and price depend only on product_id, not on the composite key (order_id, product_id)*

**AFTER 2NF (Good):**
```
OrderItems Table:
order_id | product_id | quantity
---------|------------|----------
1        | 101        | 1
1        | 102        | 2

Products Table:
product_id | product_name | price
-----------|--------------|-------
101        | Rolex        | 25000
102        | Omega        | 12500
```

#### **3NF (Third Normal Form)**
**Rules:**
- Must be in 2NF
- No transitive dependencies (non-key attributes don't depend on other non-key attributes)

**Example - BEFORE 3NF (Bad):**
```
Orders Table:
order_id | customer_id | customer_name | customer_city | total
---------|-------------|---------------|---------------|-------
1        | 501         | John          | NYC           | 25000
2        | 502         | Mary          | LA            | 12500
```
*Problem: customer_name and customer_city depend on customer_id, not directly on order_id*

**AFTER 3NF (Good):**
```
Orders Table:
order_id | customer_id | total
---------|-------------|-------
1        | 501         | 25000
2        | 502         | 12500

Customers Table:
customer_id | customer_name | customer_city
------------|---------------|---------------
501         | John          | NYC
502         | Mary          | LA
```

#### **BCNF (Boyce-Codd Normal Form)**
**Rules:**
- Must be in 3NF
- For every functional dependency X → Y, X must be a super key

**Example:**
```
If: student_id, course_id → instructor
And: instructor → course_id
Then: instructor should be a key (BCNF violation if not)
```

### 🔍 Normalization in Y2K Watch Database

**Our Database is Already Normalized:**

```sql
-- 1NF: All atomic values
users (id, username, password, created_at)

-- 2NF: No partial dependencies
products (id, name, description, price, brand, category, stock_quantity)

-- 3NF: No transitive dependencies
orders (id, user_id, total_amount, order_date, status)
order_items (id, order_id, product_id, quantity, price)

-- Proper relationships maintained
cart (id, user_id, product_id, quantity)
wishlist (id, user_id, product_id)
```

---

## 2️⃣ TRANSACTIONS

### 🎯 What is a Transaction?
A transaction is a logical unit of work that contains one or more SQL statements. All statements must succeed or all must fail (atomicity).

### 📋 ACID Properties

#### **A - Atomicity**
- All operations complete successfully or none do
- "All or Nothing" principle

**Example:**
```sql
START TRANSACTION;
UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 1;
INSERT INTO orders (user_id, total_amount) VALUES (3, 25000);
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (LAST_INSERT_ID(), 1, 1, 25000);
COMMIT;
-- If any statement fails, all are rolled back
```

#### **C - Consistency**
- Database moves from one valid state to another
- All constraints are maintained

**Example:**
```sql
-- Constraint: stock_quantity >= 0
START TRANSACTION;
UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 1;
-- If this makes stock negative, transaction fails
COMMIT;
```

#### **I - Isolation**
- Concurrent transactions don't interfere with each other
- Each transaction appears to execute in isolation

**Example:**
```sql
-- Transaction 1
START TRANSACTION;
SELECT stock_quantity FROM products WHERE id = 1; -- Reads 10
UPDATE products SET stock_quantity = 9 WHERE id = 1;
COMMIT;

-- Transaction 2 (concurrent)
START TRANSACTION;
SELECT stock_quantity FROM products WHERE id = 1; -- Should read 10 or 9 depending on isolation level
COMMIT;
```

#### **D - Durability**
- Once committed, changes are permanent
- Survives system failures

**Example:**
```sql
START TRANSACTION;
INSERT INTO orders (user_id, total_amount) VALUES (3, 25000);
COMMIT;
-- Even if system crashes after COMMIT, this order persists
```

### 🔄 Transaction States

```
Active → Partially Committed → Committed
  ↓
Failed → Aborted
```

### 💻 Transaction Commands

```sql
-- Start a transaction
START TRANSACTION;
-- or
BEGIN;

-- Save changes permanently
COMMIT;

-- Undo all changes
ROLLBACK;

-- Create a savepoint
SAVEPOINT savepoint_name;

-- Rollback to savepoint
ROLLBACK TO savepoint_name;

-- Set isolation level
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

### 📝 Practical Transaction Examples

#### **Example 1: Order Placement**
```sql
START TRANSACTION;

-- Check stock
SELECT stock_quantity FROM products WHERE id = 1 FOR UPDATE;

-- Reduce stock
UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 1;

-- Create order
INSERT INTO orders (user_id, total_amount, status) VALUES (3, 25000, 'pending');
SET @order_id = LAST_INSERT_ID();

-- Add order items
INSERT INTO order_items (order_id, product_id, quantity, price) 
VALUES (@order_id, 1, 1, 25000);

-- Clear cart
DELETE FROM cart WHERE user_id = 3 AND product_id = 1;

COMMIT;
```

#### **Example 2: Money Transfer (Classic Example)**
```sql
START TRANSACTION;

-- Deduct from sender
UPDATE accounts SET balance = balance - 1000 WHERE user_id = 1;

-- Add to receiver
UPDATE accounts SET balance = balance + 1000 WHERE user_id = 2;

-- Check if sender has sufficient balance
SELECT balance FROM accounts WHERE user_id = 1;
-- If balance < 0, ROLLBACK; else COMMIT;

COMMIT;
```

#### **Example 3: Using Savepoints**
```sql
START TRANSACTION;

INSERT INTO orders (user_id, total_amount) VALUES (3, 25000);
SAVEPOINT order_created;

INSERT INTO order_items (order_id, product_id, quantity, price) 
VALUES (LAST_INSERT_ID(), 1, 1, 25000);
SAVEPOINT items_added;

UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 1;

-- If stock update fails, rollback to items_added
-- ROLLBACK TO items_added;

COMMIT;
```

---

## 3️⃣ CONCURRENCY CONTROL

### 🎯 What is Concurrency Control?
Mechanisms to ensure correct results when multiple transactions execute simultaneously.

### ⚠️ Concurrency Problems

#### **1. Lost Update Problem**
```
Time | Transaction T1              | Transaction T2
-----|----------------------------|---------------------------
t1   | READ(X) = 100              |
t2   |                            | READ(X) = 100
t3   | X = X + 50 = 150           |
t4   |                            | X = X + 30 = 130
t5   | WRITE(X) = 150             |
t6   |                            | WRITE(X) = 130
Result: T1's update is lost! Should be 180, but is 130
```

**Solution:** Use locking or isolation levels

#### **2. Dirty Read Problem**
```
Time | Transaction T1              | Transaction T2
-----|----------------------------|---------------------------
t1   | READ(X) = 100              |
t2   | X = X + 50 = 150           |
t3   | WRITE(X) = 150             |
t4   |                            | READ(X) = 150 (dirty read)
t5   | ROLLBACK                   |
t6   |                            | Uses X = 150 (wrong!)
Result: T2 read uncommitted data that was rolled back
```

**Solution:** Use READ COMMITTED isolation level

#### **3. Non-Repeatable Read Problem**
```
Time | Transaction T1              | Transaction T2
-----|----------------------------|---------------------------
t1   | READ(X) = 100              |
t2   |                            | READ(X) = 100
t3   |                            | X = X + 50 = 150
t4   |                            | WRITE(X) = 150
t5   |                            | COMMIT
t6   | READ(X) = 150              |
Result: T1 reads X twice and gets different values
```

**Solution:** Use REPEATABLE READ isolation level

#### **4. Phantom Read Problem**
```
Time | Transaction T1                    | Transaction T2
-----|----------------------------------|---------------------------
t1   | SELECT COUNT(*) FROM orders = 10 |
t2   |                                  | INSERT INTO orders...
t3   |                                  | COMMIT
t4   | SELECT COUNT(*) FROM orders = 11 |
Result: T1 sees different number of rows in same transaction
```

**Solution:** Use SERIALIZABLE isolation level

### 🔒 Locking Mechanisms

#### **Types of Locks**

**1. Shared Lock (S-Lock) - Read Lock**
```sql
-- Multiple transactions can hold shared locks
SELECT * FROM products WHERE id = 1 LOCK IN SHARE MODE;
```

**2. Exclusive Lock (X-Lock) - Write Lock**
```sql
-- Only one transaction can hold exclusive lock
SELECT * FROM products WHERE id = 1 FOR UPDATE;
```

#### **Lock Compatibility Matrix**
```
        | S-Lock | X-Lock
--------|--------|--------
S-Lock  |   ✓    |   ✗
X-Lock  |   ✗    |   ✗
```

#### **Two-Phase Locking (2PL)**

**Growing Phase:** Acquire locks, cannot release
**Shrinking Phase:** Release locks, cannot acquire

```sql
-- Example of 2PL
START TRANSACTION;

-- Growing Phase
SELECT * FROM products WHERE id = 1 FOR UPDATE;  -- Acquire X-lock
SELECT * FROM products WHERE id = 2 FOR UPDATE;  -- Acquire X-lock

-- Perform operations
UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 1;
UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 2;

-- Shrinking Phase (on COMMIT)
COMMIT;  -- Release all locks
```

### 🎚️ Isolation Levels

```sql
-- Set isolation level
SET TRANSACTION ISOLATION LEVEL level_name;
```

| Isolation Level  | Dirty Read | Non-Repeatable Read | Phantom Read |
|-----------------|------------|---------------------|--------------|
| READ UNCOMMITTED| Possible   | Possible            | Possible     |
| READ COMMITTED  | Prevented  | Possible            | Possible     |
| REPEATABLE READ | Prevented  | Prevented           | Possible     |
| SERIALIZABLE    | Prevented  | Prevented           | Prevented    |

#### **Examples:**

**READ UNCOMMITTED:**
```sql
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
START TRANSACTION;
SELECT * FROM products WHERE id = 1;  -- Can read uncommitted changes
COMMIT;
```

**READ COMMITTED (Default in MySQL):**
```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
SELECT * FROM products WHERE id = 1;  -- Only reads committed data
COMMIT;
```

**REPEATABLE READ:**
```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
SELECT * FROM products WHERE id = 1;  -- First read
-- Other transactions can't modify this row
SELECT * FROM products WHERE id = 1;  -- Same result
COMMIT;
```

**SERIALIZABLE:**
```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
START TRANSACTION;
SELECT * FROM products WHERE stock_quantity < 10;
-- Other transactions can't insert/update/delete matching rows
COMMIT;
```

### 🔄 Deadlock

**What is Deadlock?**
Two or more transactions waiting for each other to release locks.

**Example:**
```
Time | Transaction T1              | Transaction T2
-----|----------------------------|---------------------------
t1   | LOCK(A)                    |
t2   |                            | LOCK(B)
t3   | Wait for LOCK(B)           |
t4   |                            | Wait for LOCK(A)
Result: DEADLOCK! Both waiting forever
```

**Deadlock Prevention:**
```sql
-- Always acquire locks in same order
-- Transaction 1
START TRANSACTION;
SELECT * FROM products WHERE id = 1 FOR UPDATE;  -- Lock product 1 first
SELECT * FROM orders WHERE id = 1 FOR UPDATE;    -- Then lock order 1
COMMIT;

-- Transaction 2
START TRANSACTION;
SELECT * FROM products WHERE id = 1 FOR UPDATE;  -- Lock product 1 first (same order)
SELECT * FROM orders WHERE id = 1 FOR UPDATE;    -- Then lock order 1
COMMIT;
```

**Deadlock Detection:**
```sql
-- MySQL automatically detects and resolves deadlocks
-- One transaction is rolled back (victim selection)
SHOW ENGINE INNODB STATUS;  -- View deadlock information
```

---

## 4️⃣ PRACTICAL EXAMPLES (Y2K Watch Database)

### Example 1: Normalized Database Design

```sql
-- Our database follows 3NF

-- Users table (no redundancy)
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table (atomic values, no partial dependencies)
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    brand VARCHAR(100),
    category VARCHAR(100),
    stock_quantity INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table (no transitive dependencies)
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending','completed','cancelled') DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Order items (junction table, proper normalization)
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### Example 2: Complete Order Transaction

```sql
-- Transaction for placing an order
START TRANSACTION;

-- Step 1: Verify stock availability
SELECT stock_quantity INTO @stock 
FROM products 
WHERE id = 1 
FOR UPDATE;

-- Step 2: Check if sufficient stock
IF @stock >= 1 THEN
    -- Step 3: Reduce stock
    UPDATE products 
    SET stock_quantity = stock_quantity - 1 
    WHERE id = 1;
    
    -- Step 4: Create order
    INSERT INTO orders (user_id, total_amount, status) 
    VALUES (3, 25000.00, 'pending');
    
    SET @order_id = LAST_INSERT_ID();
    
    -- Step 5: Add order items
    INSERT INTO order_items (order_id, product_id, quantity, price) 
    VALUES (@order_id, 1, 1, 25000.00);
    
    -- Step 6: Clear cart
    DELETE FROM cart 
    WHERE user_id = 3 AND product_id = 1;
    
    COMMIT;
ELSE
    ROLLBACK;
END IF;
```

### Example 3: Concurrent Cart Updates

```sql
-- Transaction 1: User adds to cart
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;

INSERT INTO cart (user_id, product_id, quantity) 
VALUES (3, 1, 1)
ON DUPLICATE KEY UPDATE quantity = quantity + 1;

COMMIT;

-- Transaction 2: User removes from cart (concurrent)
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;

DELETE FROM cart 
WHERE user_id = 3 AND product_id = 1;

COMMIT;
```

### Example 4: Preventing Lost Updates

```sql
-- Wrong way (Lost Update possible)
START TRANSACTION;
SELECT stock_quantity INTO @stock FROM products WHERE id = 1;
SET @new_stock = @stock - 1;
UPDATE products SET stock_quantity = @new_stock WHERE id = 1;
COMMIT;

-- Correct way (Using FOR UPDATE)
START TRANSACTION;
SELECT stock_quantity FROM products WHERE id = 1 FOR UPDATE;
UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 1;
COMMIT;
```

---

## 5️⃣ PRACTICE QUESTIONS

### Normalization Questions

**Q1:** Identify the normal form of this table and normalize it to 3NF:
```
OrderDetails (order_id, customer_name, customer_email, product_id, 
              product_name, product_price, quantity, order_total)
```

**Q2:** What are the problems with this design? How would you fix it?
```
Products (id, name, category_name, category_description, price)
```

**Q3:** Convert this to BCNF:
```
CourseInstructor (student_id, course_id, instructor_name)
FD: {student_id, course_id} → instructor_name
FD: instructor_name → course_id
```

### Transaction Questions

**Q4:** Write a transaction to transfer $1000 from Account A to Account B with proper error handling.

**Q5:** What happens if a transaction fails after updating 2 out of 3 tables? How does ACID prevent data inconsistency?

**Q6:** Explain the difference between COMMIT and ROLLBACK with examples.

### Concurrency Control Questions

**Q7:** Two transactions try to update the same product stock simultaneously. Show how this can cause a lost update problem and how to prevent it.

**Q8:** What isolation level would you use for:
- a) Banking application
- b) Social media feed
- c) Inventory management system

**Q9:** Explain how deadlock can occur with two transactions and how to prevent it.

**Q10:** Compare optimistic vs pessimistic concurrency control.

---

## 📝 Quick Reference

### Normalization Checklist
- [ ] 1NF: Atomic values, no repeating groups
- [ ] 2NF: No partial dependencies
- [ ] 3NF: No transitive dependencies
- [ ] BCNF: Every determinant is a candidate key

### Transaction Commands
```sql
START TRANSACTION;
COMMIT;
ROLLBACK;
SAVEPOINT name;
ROLLBACK TO name;
```

### Isolation Levels (Strictest to Loosest)
1. SERIALIZABLE (Slowest, Most Consistent)
2. REPEATABLE READ (MySQL Default)
3. READ COMMITTED
4. READ UNCOMMITTED (Fastest, Least Consistent)

### Locking
```sql
SELECT ... LOCK IN SHARE MODE;  -- Shared lock
SELECT ... FOR UPDATE;           -- Exclusive lock
```

---

## 🎯 Exam Tips

1. **Normalization:** Always identify functional dependencies first
2. **Transactions:** Remember ACID properties with examples
3. **Concurrency:** Know the problems and their solutions
4. **Practical:** Be ready to write SQL transactions
5. **Theory:** Understand WHY, not just WHAT

---

**Good Luck with Your Review! 🚀**

*Study Date: 13.04.2026 to 20.04.2026*
*Review Topics: Chapters 4 & 5*
