# 🛍️ How Collections Work in Y2K Watch E-commerce

## 📋 Overview

Your Y2K Watch E-commerce application has a **product collections system** that allows users to browse, filter, and purchase luxury watches. Here's how everything works together.

---

## 🏗️ Architecture

### **1. Database Structure**

```sql
products (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    price DECIMAL(10,2),
    brand VARCHAR(100),          -- Collection grouping
    category VARCHAR(100),        -- Collection type
    image_url VARCHAR(500),
    stock_quantity INT,
    average_rating DECIMAL(3,2),
    total_reviews INT,
    created_at TIMESTAMP
)
```

**Current Collections:**
- **Brands**: Rolex, Omega, Patek Philippe, Cartier, TAG Heuer, Audemars Piguet, Breitling, IWC
- **Categories**: Classic, Sport, Luxury, Elegant, Aviation

---

## 🎯 How It Works - Step by Step

### **Step 1: Home Page Collections Display**

**Location**: `templates/index.html`

```html
<!-- Featured Collections Section -->
<section class="bw-collections">
    <h2>Featured Collections</h2>
    
    <div class="bw-collection-grid">
        <!-- Classic Collection Card -->
        <div class="bw-card">
            <img src="classic-watch.jpg">
            <div class="bw-card-body">
                <h4>Classic</h4>
                <p>Timeless designs for every occasion.</p>
                <a href="/products">View Collection →</a>
            </div>
        </div>
        
        <!-- Sport Collection Card -->
        <div class="bw-card">
            <img src="sport-watch.jpg">
            <div class="bw-card-body">
                <h4>Sport</h4>
                <p>Built for performance and endurance.</p>
                <a href="/products">View Collection →</a>
            </div>
        </div>
        
        <!-- Limited Collection Card -->
        <div class="bw-card">
            <img src="limited-watch.jpg">
            <div class="bw-card-body">
                <h4>Limited</h4>
                <p>Exclusive editions for collectors.</p>
                <a href="/products">View Collection →</a>
            </div>
        </div>
    </div>
</section>
```

**What Happens:**
1. User visits home page (`/home`)
2. Sees 3 featured collection cards (Classic, Sport, Limited)
3. Each card has an image, title, description, and "View Collection" link
4. Clicking any card takes user to `/products` page

---

### **Step 2: Products Page - Full Collection**

**Location**: `app.py` - `/products` route

```python
@app.route('/products')
def products():
    # Get filter parameters from URL
    search = request.args.get('search', '')
    brand = request.args.get('brand', '')
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    sort_by = request.args.get('sort', 'name')
    
    # Build dynamic SQL query
    query = 'SELECT * FROM products WHERE 1=1'
    params = []
    
    # Add filters
    if search:
        query += ' AND (name LIKE %s OR description LIKE %s OR brand LIKE %s)'
        params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
    
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
    query += ' ORDER BY name ASC'  # or price, rating, etc.
    
    # Execute query
    cursor.execute(query, params)
    products_list = cursor.fetchall()
    
    # Get unique brands and categories for filters
    cursor.execute('SELECT DISTINCT brand FROM products')
    brands = [row['brand'] for row in cursor.fetchall()]
    
    cursor.execute('SELECT DISTINCT category FROM products')
    categories = [row['category'] for row in cursor.fetchall()]
    
    # Render template with data
    return render_template('products.html', 
                         products=products_list,
                         brands=brands,
                         categories=categories)
```

**What Happens:**
1. User clicks "View Collection" or navigates to `/products`
2. Flask fetches all products from database
3. Applies any filters (search, brand, category, price range)
4. Sorts products based on user selection
5. Passes products to template for display

---

### **Step 3: Products Page Display**

**Location**: `templates/products.html`

```html
<!-- Search and Filter Section -->
<div class="search-filter-section">
    <form method="GET" action="/products">
        <!-- Search Bar -->
        <input type="text" name="search" placeholder="Search watches...">
        
        <!-- Brand Filter -->
        <select name="brand">
            <option value="">All Brands</option>
            <option value="Rolex">Rolex</option>
            <option value="Omega">Omega</option>
            <!-- More brands... -->
        </select>
        
        <!-- Category Filter -->
        <select name="category">
            <option value="">All Categories</option>
            <option value="Classic">Classic</option>
            <option value="Sport">Sport</option>
            <!-- More categories... -->
        </select>
        
        <!-- Price Range -->
        <input type="number" name="min_price" placeholder="Min Price">
        <input type="number" name="max_price" placeholder="Max Price">
        
        <!-- Sort -->
        <select name="sort">
            <option value="name">Name A-Z</option>
            <option value="price_low">Price: Low to High</option>
            <option value="price_high">Price: High to Low</option>
        </select>
        
        <button type="submit">Search</button>
    </form>
</div>

<!-- Products Grid -->
<div class="row">
    {% for product in products %}
    <div class="col-lg-3 col-md-6">
        <div class="product-card">
            <!-- Product Image -->
            <img src="{{ product.image_url }}" alt="{{ product.name }}">
            
            <!-- Product Info -->
            <h5>{{ product.name }}</h5>
            <p>{{ product.description }}</p>
            
            <!-- Brand & Category Badges -->
            <span class="brand-badge">{{ product.brand }}</span>
            <span class="category-badge">{{ product.category }}</span>
            
            <!-- Price & Stock -->
            <p class="price">${{ product.price }}</p>
            <p class="stock">{{ product.stock_quantity }} in stock</p>
            
            <!-- Actions -->
            <form action="/add_to_cart/{{ product.id }}" method="POST">
                <button type="submit">Add to Cart</button>
            </form>
            
            <form action="/add_to_wishlist/{{ product.id }}" method="POST">
                <button type="submit">♥ Wishlist</button>
            </form>
        </div>
    </div>
    {% endfor %}
</div>
```

**What Happens:**
1. Products are displayed in a responsive grid
2. Each product card shows:
   - Image
   - Name and description
   - Brand and category badges
   - Price and stock status
   - Add to Cart button
   - Add to Wishlist button
3. Users can filter by brand, category, price range
4. Users can sort by name, price, rating, date

---

## 🔍 Filtering System

### **How Filters Work:**

```
User Action → URL Parameters → SQL Query → Filtered Results

Example:
1. User selects "Rolex" brand
2. URL becomes: /products?brand=Rolex
3. SQL: SELECT * FROM products WHERE brand = 'Rolex'
4. Only Rolex watches are displayed
```

### **Multiple Filters:**

```
URL: /products?brand=Rolex&category=Classic&min_price=20000&max_price=30000

SQL Query:
SELECT * FROM products 
WHERE brand = 'Rolex' 
  AND category = 'Classic' 
  AND price >= 20000 
  AND price <= 30000
ORDER BY name ASC
```

---

## 🛒 Add to Cart Flow

```
1. User clicks "Add to Cart" button
   ↓
2. POST request to /add_to_cart/<product_id>
   ↓
3. Flask checks if user is logged in
   ↓
4. Checks product stock availability
   ↓
5. Inserts into cart table:
   INSERT INTO cart (user_id, product_id, quantity)
   VALUES (3, 1, 1)
   ON DUPLICATE KEY UPDATE quantity = quantity + 1
   ↓
6. Shows popup notification "Added to cart!"
   ↓
7. User can continue shopping or go to cart
```

---

## ❤️ Wishlist Flow

```
1. User clicks "♥ Wishlist" button
   ↓
2. POST request to /add_to_wishlist/<product_id>
   ↓
3. Flask checks if user is logged in
   ↓
4. Inserts into wishlist table:
   INSERT INTO wishlist (user_id, product_id)
   VALUES (3, 1)
   ↓
5. Shows success message
   ↓
6. User can view wishlist from navigation menu
```

---

## 📊 Database Queries

### **Get All Products:**
```sql
SELECT * FROM products ORDER BY name ASC;
```

### **Get Products by Brand:**
```sql
SELECT * FROM products WHERE brand = 'Rolex';
```

### **Get Products by Category:**
```sql
SELECT * FROM products WHERE category = 'Sport';
```

### **Get Products by Price Range:**
```sql
SELECT * FROM products 
WHERE price BETWEEN 10000 AND 30000;
```

### **Search Products:**
```sql
SELECT * FROM products 
WHERE name LIKE '%Classic%' 
   OR description LIKE '%Classic%' 
   OR brand LIKE '%Classic%';
```

### **Get Available Brands:**
```sql
SELECT DISTINCT brand FROM products 
WHERE brand IS NOT NULL 
ORDER BY brand;
```

### **Get Available Categories:**
```sql
SELECT DISTINCT category FROM products 
WHERE category IS NOT NULL 
ORDER BY category;
```

---

## 🎨 Visual Flow

```
┌─────────────────┐
│   Home Page     │
│  (index.html)   │
└────────┬────────┘
         │
         │ Click "View Collection"
         ↓
┌─────────────────┐
│ Products Page   │
│ (products.html) │
│                 │
│ ┌─────────────┐ │
│ │   Filters   │ │
│ │  - Search   │ │
│ │  - Brand    │ │
│ │  - Category │ │
│ │  - Price    │ │
│ │  - Sort     │ │
│ └─────────────┘ │
│                 │
│ ┌─────────────┐ │
│ │  Products   │ │
│ │   Grid      │ │
│ │             │ │
│ │ [Product 1] │ │
│ │ [Product 2] │ │
│ │ [Product 3] │ │
│ └─────────────┘ │
└────────┬────────┘
         │
         │ Click "Add to Cart"
         ↓
┌─────────────────┐
│   Cart Page     │
│  (cart.html)    │
└────────┬────────┘
         │
         │ Click "Checkout"
         ↓
┌─────────────────┐
│ Checkout Page   │
│ (checkout.html) │
└────────┬────────┘
         │
         │ Complete Order
         ↓
┌─────────────────┐
│ Order Success   │
│ (order_success) │
└─────────────────┘
```

---

## 🔧 Key Features

### **1. Dynamic Filtering**
- Real-time filtering without page reload
- Multiple filters can be combined
- URL parameters preserve filter state

### **2. Search Functionality**
- Searches across name, description, and brand
- Case-insensitive search
- Partial matching supported

### **3. Sorting Options**
- Name (A-Z)
- Price (Low to High / High to Low)
- Rating (Highest first)
- Newest first

### **4. Stock Management**
- Shows current stock quantity
- Disables "Add to Cart" when out of stock
- Real-time stock updates

### **5. Responsive Design**
- Mobile-friendly grid layout
- Burger menu for mobile navigation
- Touch-friendly buttons

---

## 💾 Data Flow

```
Database (MySQL)
    ↓
Flask Backend (app.py)
    ↓
Jinja2 Template (products.html)
    ↓
HTML/CSS (Browser)
    ↓
User Interaction
    ↓
AJAX/Form Submit
    ↓
Flask Backend
    ↓
Database Update
    ↓
Response to User
```

---

## 🎯 Current Collections

### **By Brand:**
1. **Rolex** - Royal Classic ($25,000) - 25 in stock
2. **Omega** - Titanium Sport ($12,500) - 30 in stock
3. **Patek Philippe** - Diamond Prestige ($85,000) - 5 in stock
4. **Cartier** - Rose Elegance ($18,500) - 20 in stock
5. **TAG Heuer** - Master Chronograph ($15,200) - 15 in stock
6. **Audemars Piguet** - Skeleton Master - 12 in stock

### **By Category:**
- **Classic**: Traditional, timeless designs
- **Sport**: Performance-oriented watches
- **Luxury**: High-end, premium watches
- **Elegant**: Formal occasion watches
- **Aviation**: Pilot-inspired watches

---

## 🚀 How to Test

### **1. View All Products:**
```
http://127.0.0.1:8000/products
```

### **2. Filter by Brand:**
```
http://127.0.0.1:8000/products?brand=Rolex
```

### **3. Filter by Category:**
```
http://127.0.0.1:8000/products?category=Sport
```

### **4. Search Products:**
```
http://127.0.0.1:8000/products?search=Classic
```

### **5. Price Range:**
```
http://127.0.0.1:8000/products?min_price=10000&max_price=30000
```

### **6. Multiple Filters:**
```
http://127.0.0.1:8000/products?brand=Rolex&category=Classic&sort=price_low
```

---

## 📝 Summary

Your collections system works through:

1. **Database**: Stores products with brand and category
2. **Backend**: Flask routes handle filtering and sorting
3. **Frontend**: Jinja2 templates display products dynamically
4. **User Interaction**: Forms and AJAX for cart/wishlist
5. **Responsive Design**: Works on all devices

The system is fully functional with 6 products across multiple brands and categories, with complete filtering, searching, and sorting capabilities! 🎉
