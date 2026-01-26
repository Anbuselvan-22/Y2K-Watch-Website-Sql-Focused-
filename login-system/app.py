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
            return redirect(url_for('dashboard'))
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
    return redirect(url_for('home'))

@app.route('/')
def home():
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

# ---------------- Products Page (Dynamic) ----------------
@app.route('/products')
def products():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('products.html', products=products_list)

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
            image_url VARCHAR(500),
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
    
    # Insert sample products if table is empty
    cursor.execute('SELECT COUNT(*) as count FROM products')
    if cursor.fetchone()['count'] == 0:
        products = [
            ('Royal Classic', 'In Oystersteel, featuring a bright blue baton dial, smooth bezel, and Oyster bracelet.Limited to 100 pieces.', 25000.00, 'https://unsplash.com/photos/silver-and-white-round-analog-watch-LWPPpkn6NEQ'),
            ('Titanium Sport', 'Lightweight titanium case with ceramic bezel. Water-resistant to 300m.', 12500.00, 'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'),
            ('Diamond Prestige', 'Platinum case set with 2.5 carats of flawless diamonds. Tourbillon movement.', 85000.00, 'https://images.unsplash.com/photo-1434056886845-dac89ffe9b56?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'),
            ('Rose Elegance', '18k rose gold with mother-of-pearl dial. Perfect for formal occasions.', 18500.00, 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'),
            ('Master Chronograph', 'Stainless steel case with flyback chronograph. Professional timing instrument.', 15200.00, 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'),
            ('Skeleton Master', 'Open-worked movement visible through sapphire crystal. Mechanical art.', 32000.00, 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80')
        ]
        cursor.executemany('INSERT INTO products (name, description, price, image_url) VALUES (%s, %s, %s, %s)', products)
    
    conn.commit()
    cursor.close()
    conn.close()

# ---------------- Main ----------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
