from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ---------------- Database Connection ----------------
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='login_db',
        cursorclass=pymysql.cursors.DictCursor
    )

# ---------------- User Authentication ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except pymysql.IntegrityError:
            flash('Username already exists', 'warning')
        finally:
            cursor.close()
            conn.close()
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('index'))



@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('index'))

@app.route('/home')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/about')
def about():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('about.html')

@app.route('/contact')
def contact():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('contact.html')

# ---------------- Products Page (Dynamic with Search & Filters) ----------------
@app.route('/products')
def products():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get filter parameters
    search = request.args.get('search', '')
    brand = request.args.get('brand', '')
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    sort_by = request.args.get('sort', 'name')
    
    # Build SQL query with filters
    query = 'SELECT * FROM products WHERE 1=1'
    params = []
    
    if search:
        query += ' AND (name LIKE %s OR description LIKE %s OR brand LIKE %s)'
        search_param = f'%{search}%'
        params.extend([search_param, search_param, search_param])
    
    if brand:
        query += ' AND brand = %s'
        params.append(brand)
    
    if category:
        query += ' AND category = %s'
        params.append(category)
    
    if min_price:
        query += ' AND price >= %s'
        params.append(float(min_price))
    
    if max_price:
        query += ' AND price <= %s'
        params.append(float(max_price))
    
    # Add sorting
    valid_sorts = {
        'name': 'name ASC',
        'price_low': 'price ASC',
        'price_high': 'price DESC',
        'rating': 'average_rating DESC',
        'newest': 'created_at DESC'
    }
    
    if sort_by in valid_sorts:
        query += f' ORDER BY {valid_sorts[sort_by]}'
    else:
        query += ' ORDER BY name ASC'
    
    cursor.execute(query, params)
    products_list = cursor.fetchall()
    
    # Get filter options for dropdowns
    cursor.execute('SELECT DISTINCT brand FROM products WHERE brand IS NOT NULL ORDER BY brand')
    brands = [row['brand'] for row in cursor.fetchall()]
    
    cursor.execute('SELECT DISTINCT category FROM products WHERE category IS NOT NULL ORDER BY category')
    categories = [row['category'] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return render_template('products.html', 
                         products=products_list, 
                         brands=brands, 
                         categories=categories,
                         current_search=search,
                         current_brand=brand,
                         current_category=category,
                         current_min_price=min_price,
                         current_max_price=max_price,
                         current_sort=sort_by)

# ---------------- Cart ----------------
@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.id, c.quantity, p.name, p.price, p.image_url, (c.quantity * p.price) as total
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    ''', (session['user_id'],))
    cart_items = cursor.fetchall()
    cursor.execute('SELECT SUM(c.quantity * p.price) as grand_total FROM cart c JOIN products p ON c.product_id = p.id WHERE c.user_id = %s', (session['user_id'],))
    grand_total = cursor.fetchone()['grand_total'] or 0
    cursor.close()
    conn.close()
    return render_template('cart.html', cart_items=cart_items, grand_total=grand_total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        if request.headers.get('Content-Type') == 'application/json' or request.is_json:
            return {'success': False, 'message': 'Please login first'}, 401
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Get product name for the response
        cursor.execute('SELECT name FROM products WHERE id = %s', (product_id,))
        product = cursor.fetchone()
        
        if not product:
            if request.headers.get('Content-Type') == 'application/json' or request.is_json:
                return {'success': False, 'message': 'Product not found'}, 404
            flash('Product not found.', 'danger')
            return redirect(url_for('products'))
        
        cursor.execute('''
            INSERT INTO cart (user_id, product_id) VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE quantity = quantity + 1
        ''', (session['user_id'], product_id))
        conn.commit()
        
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return {'success': True, 'message': f'{product["name"]} added to cart successfully!', 'product_name': product['name']}
        
        flash('Product added to cart successfully!', 'success')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return {'success': False, 'message': 'Error adding product to cart.'}, 500
        flash('Error adding product to cart.', 'danger')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('products'))

@app.route('/remove_from_cart/<int:cart_id>', methods=['POST'])
def remove_from_cart(cart_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM cart WHERE id = %s AND user_id = %s', (cart_id, session['user_id']))
        conn.commit()
        flash('Item removed from cart.', 'success')
    except Exception:
        flash('Error removing item from cart.', 'danger')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('cart'))

# ---------------- Checkout ----------------
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        try:
            # Get cart items
            cursor.execute('''
                SELECT c.product_id, c.quantity, p.price 
                FROM cart c JOIN products p ON c.product_id = p.id 
                WHERE c.user_id = %s
            ''', (session['user_id'],))
            cart_items = cursor.fetchall()
            
            if not cart_items:
                flash('Your cart is empty.', 'warning')
                return redirect(url_for('cart'))
            
            # Calculate total
            total = sum(item['quantity'] * item['price'] for item in cart_items)
            
            # Create order
            cursor.execute('INSERT INTO orders (user_id, total_amount) VALUES (%s, %s)', (session['user_id'], total))
            order_id = cursor.lastrowid
            
            # Insert order items
            for item in cart_items:
                cursor.execute('''
                    INSERT INTO order_items (order_id, product_id, quantity, price) 
                    VALUES (%s, %s, %s, %s)
                ''', (order_id, item['product_id'], item['quantity'], item['price']))
            
            # Clear cart
            cursor.execute('DELETE FROM cart WHERE user_id = %s', (session['user_id'],))
            conn.commit()
            flash('Order placed successfully!', 'success')
            return redirect(url_for('order_success'))
        except Exception:
            conn.rollback()
            flash('Error processing order.', 'danger')
        finally:
            cursor.close()
            conn.close()
    else:
        # GET: Show checkout page
        cursor.execute('''
            SELECT c.quantity, p.name, p.price, (c.quantity * p.price) as total
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
        ''', (session['user_id'],))
        cart_items = cursor.fetchall()
        cursor.execute('SELECT SUM(c.quantity * p.price) as grand_total FROM cart c JOIN products p ON c.product_id = p.id WHERE c.user_id = %s', (session['user_id'],))
        grand_total = cursor.fetchone()['grand_total'] or 0
        cursor.close()
        conn.close()
        return render_template('checkout.html', cart_items=cart_items, grand_total=grand_total)

@app.route('/order_success')
def order_success():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('order_success.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

# ---------------- Wishlist ----------------
@app.route('/wishlist')
def wishlist():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT w.*, p.name, p.price, p.image_url, p.brand
        FROM wishlist w
        JOIN products p ON w.product_id = p.id
        WHERE w.user_id = %s
        ORDER BY w.added_at DESC
    ''', (session['user_id'],))
    wishlist_items = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('wishlist.html', wishlist_items=wishlist_items)

@app.route('/add_to_wishlist/<int:product_id>', methods=['POST'])
def add_to_wishlist(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO wishlist (user_id, product_id) VALUES (%s, %s)
        ''', (session['user_id'], product_id))
        conn.commit()
        flash('Product added to wishlist!', 'success')
    except pymysql.IntegrityError:
        flash('Product is already in your wishlist.', 'info')
    except Exception:
        flash('Error adding product to wishlist.', 'danger')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('products'))

@app.route('/remove_from_wishlist/<int:wishlist_id>', methods=['POST'])
def remove_from_wishlist(wishlist_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM wishlist WHERE id = %s AND user_id = %s', 
                      (wishlist_id, session['user_id']))
        conn.commit()
        flash('Item removed from wishlist.', 'success')
    except Exception:
        flash('Error removing item from wishlist.', 'danger')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('wishlist'))

# ---------------- Database Migration ----------------
def migrate_db():
    """Add missing columns to existing tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if brand column exists in products table
        cursor.execute("SHOW COLUMNS FROM products LIKE 'brand'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE products ADD COLUMN brand VARCHAR(100)")
            print("Added brand column to products table")
        
        # Check if category column exists in products table
        cursor.execute("SHOW COLUMNS FROM products LIKE 'category'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE products ADD COLUMN category VARCHAR(100)")
            print("Added category column to products table")
        
        # Check if stock_quantity column exists in products table
        cursor.execute("SHOW COLUMNS FROM products LIKE 'stock_quantity'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE products ADD COLUMN stock_quantity INT DEFAULT 0")
            print("Added stock_quantity column to products table")
        
        # Check if average_rating column exists in products table
        cursor.execute("SHOW COLUMNS FROM products LIKE 'average_rating'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE products ADD COLUMN average_rating DECIMAL(3,2) DEFAULT 0.00")
            print("Added average_rating column to products table")
        
        # Check if total_reviews column exists in products table
        cursor.execute("SHOW COLUMNS FROM products LIKE 'total_reviews'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE products ADD COLUMN total_reviews INT DEFAULT 0")
            print("Added total_reviews column to products table")
        
        # Check if created_at column exists in products table
        cursor.execute("SHOW COLUMNS FROM products LIKE 'created_at'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE products ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("Added created_at column to products table")
        
        # Check if created_at column exists in users table
        cursor.execute("SHOW COLUMNS FROM users LIKE 'created_at'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("Added created_at column to users table")
        
        # Update existing products with brand and category data if they're missing
        cursor.execute("SELECT COUNT(*) as count FROM products WHERE brand IS NULL OR brand = ''")
        products_without_brand = cursor.fetchone()['count']
        
        if products_without_brand > 0:
            # Update products with brand and category information
            updates = [
                ("UPDATE products SET brand = 'Rolex', category = 'Classic' WHERE name LIKE '%Rolex%'", ),
                ("UPDATE products SET brand = 'Omega', category = 'Sport' WHERE name LIKE '%Omega%'", ),
                ("UPDATE products SET brand = 'Patek Philippe', category = 'Luxury' WHERE name LIKE '%Patek%'", ),
                ("UPDATE products SET brand = 'Cartier', category = 'Elegant' WHERE name LIKE '%Cartier%'", ),
                ("UPDATE products SET brand = 'TAG Heuer', category = 'Sport' WHERE name LIKE '%TAG%'", ),
                ("UPDATE products SET brand = 'Audemars Piguet', category = 'Luxury' WHERE name LIKE '%Audemars%'", ),
                ("UPDATE products SET brand = 'Breitling', category = 'Aviation' WHERE name LIKE '%Breitling%'", ),
                ("UPDATE products SET brand = 'IWC', category = 'Classic' WHERE name LIKE '%IWC%'", ),
            ]
            
            for update_query, in updates:
                cursor.execute(update_query)
            
            print("Updated existing products with brand and category data")
        
        conn.commit()
        print("Database migration completed successfully")
        
    except Exception as e:
        print(f"Migration error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# ---------------- Initialize Database ----------------
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL,
            brand VARCHAR(100),
            category VARCHAR(100),
            image_url VARCHAR(500),
            stock_quantity INT DEFAULT 0,
            average_rating DECIMAL(3,2) DEFAULT 0.00,
            total_reviews INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Cart table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            UNIQUE KEY unique_cart_item (user_id, product_id)
        )
    ''')
    
    # Orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status ENUM('pending','completed','cancelled') DEFAULT 'pending',
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Order items
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )
    ''')
    
    # Reviews table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            product_id INT NOT NULL,
            rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
            review_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            UNIQUE KEY unique_user_product_review (user_id, product_id)
        )
    ''')
    
    # Wishlist table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wishlist (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            product_id INT NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            UNIQUE KEY unique_wishlist_item (user_id, product_id)
        )
    ''')
    
    # Insert sample products if table is empty
    cursor.execute('SELECT COUNT(*) as count FROM products')
    if cursor.fetchone()['count'] == 0:
        products = [
            ('Rolex Datejust 41', 'In Oystersteel, featuring a bright blue baton dial, smooth bezel, and Oyster bracelet. Limited to 100 pieces.', 25000.00, 'Rolex', 'Classic', '/static/images/andrey-matveev-9mU2L4dVYFA-unsplash.jpg', 15),
            ('Omega Speedmaster', 'Lightweight titanium case with ceramic bezel. Water-resistant to 300m.', 12500.00, 'Omega', 'Sport', '/static/images/pratik-prasad-ekD-UtzJn9M-unsplash.jpg', 8),
            ('Patek Philippe Calatrava', 'Platinum case set with 2.5 carats of flawless diamonds. Tourbillon movement.', 85000.00, 'Patek Philippe', 'Luxury', '/static/images/Rolex Submariner Werbung.jpg', 3),
            ('Cartier Santos', '18k rose gold with mother-of-pearl dial. Perfect for formal occasions.', 18500.00, 'Cartier', 'Elegant', '/static/images/login-bg-1.jpg', 12),
            ('TAG Heuer Carrera', 'Stainless steel case with flyback chronograph. Professional timing instrument.', 15200.00, 'TAG Heuer', 'Sport', '/static/images/login-bg-2.jpg', 20),
            ('Audemars Piguet Royal Oak', 'Open-worked movement visible through sapphire crystal. Mechanical art.', 32000.00, 'Audemars Piguet', 'Luxury', '/static/images/login-bg-3.jpg', 5),
            ('Breitling Navitimer', 'Aviation-inspired chronograph with slide rule bezel.', 8500.00, 'Breitling', 'Aviation', '/static/images/andrey-matveev-9mU2L4dVYFA-unsplash.jpg', 25),
            ('IWC Portugieser', 'Classic dress watch with power reserve indicator.', 22000.00, 'IWC', 'Classic', '/static/images/pratik-prasad-ekD-UtzJn9M-unsplash.jpg', 10)
        ]
        cursor.executemany('INSERT INTO products (name, description, price, brand, category, image_url, stock_quantity) VALUES (%s, %s, %s, %s, %s, %s, %s)', products)
    
    conn.commit()
    cursor.close()
    conn.close()

# ---------------- Main ----------------
if __name__ == '__main__':
    init_db()
    migrate_db()
    app.run(debug=True, host='0.0.0.0', port=8000)
