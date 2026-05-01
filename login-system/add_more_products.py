import pymysql

# Database connection
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='login_db',
        cursorclass=pymysql.cursors.DictCursor
    )

# New luxury watch products to add
new_products = [
    {
        'name': 'Submariner Deep Sea',
        'description': 'Professional diving watch with 300m water resistance, ceramic bezel, and luminescent markers.',
        'price': 42000.00,
        'brand': 'Rolex',
        'category': 'Diving',
        'stock_quantity': 8,
        'image_url': 'images/andrey-matveev-9mU2L4dVYFA-unsplash.jpg',
        'average_rating': 4.9,
        'total_reviews': 156
    },
    {
        'name': 'Speedmaster Moonwatch',
        'description': 'Legendary chronograph worn on the moon. Manual-wind movement with hesalite crystal.',
        'price': 28500.00,
        'brand': 'Omega',
        'category': 'Chronograph',
        'stock_quantity': 12,
        'image_url': 'images/pratik-prasad-ekD-UtzJn9M-unsplash.jpg',
        'average_rating': 4.8,
        'total_reviews': 203
    },
    {
        'name': 'Nautilus Steel',
        'description': 'Iconic luxury sports watch with integrated bracelet and porthole-inspired case design.',
        'price': 95000.00,
        'brand': 'Patek Philippe',
        'category': 'Luxury Sport',
        'stock_quantity': 3,
        'image_url': 'images/Rolex Submariner Werbung.jpg',
        'average_rating': 5.0,
        'total_reviews': 89
    },
    {
        'name': 'Santos de Cartier',
        'description': 'Square-cased aviation-inspired watch with exposed screws and Roman numerals.',
        'price': 35000.00,
        'brand': 'Cartier',
        'category': 'Dress',
        'stock_quantity': 10,
        'image_url': 'images/ -4.jpg',
        'average_rating': 4.7,
        'total_reviews': 134
    },
    {
        'name': 'Carrera Calibre 16',
        'description': 'Racing-inspired chronograph with tachymeter scale and date display.',
        'price': 18900.00,
        'brand': 'TAG Heuer',
        'category': 'Chronograph',
        'stock_quantity': 15,
        'image_url': 'images/ -5.jpg',
        'average_rating': 4.6,
        'total_reviews': 178
    },
    {
        'name': 'Royal Oak Offshore',
        'description': 'Bold oversized sports watch with octagonal bezel and "Tapisserie" dial pattern.',
        'price': 78000.00,
        'brand': 'Audemars Piguet',
        'category': 'Luxury Sport',
        'stock_quantity': 5,
        'image_url': 'images/andrey-matveev-9mU2L4dVYFA-unsplash.jpg',
        'average_rating': 4.9,
        'total_reviews': 112
    },
    {
        'name': 'Navitimer B01',
        'description': 'Aviation chronograph with circular slide rule for flight calculations.',
        'price': 38500.00,
        'brand': 'Breitling',
        'category': 'Aviation',
        'stock_quantity': 9,
        'image_url': 'images/pratik-prasad-ekD-UtzJn9M-unsplash.jpg',
        'average_rating': 4.7,
        'total_reviews': 145
    },
    {
        'name': 'Portugieser Chronograph',
        'description': 'Classic dress chronograph with large Arabic numerals and leaf-shaped hands.',
        'price': 45000.00,
        'brand': 'IWC',
        'category': 'Dress',
        'stock_quantity': 7,
        'image_url': 'images/Rolex Submariner Werbung.jpg',
        'average_rating': 4.8,
        'total_reviews': 98
    },
    {
        'name': 'Daytona Cosmograph',
        'description': 'Iconic racing chronograph with tachymeter bezel and contrasting sub-dials.',
        'price': 125000.00,
        'brand': 'Rolex',
        'category': 'Chronograph',
        'stock_quantity': 2,
        'image_url': 'images/ -4.jpg',
        'average_rating': 5.0,
        'total_reviews': 267
    },
    {
        'name': 'Seamaster Aqua Terra',
        'description': 'Versatile sports-elegant watch with teak-pattern dial and Master Chronometer movement.',
        'price': 32000.00,
        'brand': 'Omega',
        'category': 'Luxury Sport',
        'stock_quantity': 11,
        'image_url': 'images/ -5.jpg',
        'average_rating': 4.7,
        'total_reviews': 189
    },
    {
        'name': 'Calatrava White Gold',
        'description': 'Timeless dress watch with minimalist design and hand-wound movement.',
        'price': 68000.00,
        'brand': 'Patek Philippe',
        'category': 'Dress',
        'stock_quantity': 4,
        'image_url': 'images/andrey-matveev-9mU2L4dVYFA-unsplash.jpg',
        'average_rating': 4.9,
        'total_reviews': 76
    },
    {
        'name': 'Tank Must',
        'description': 'Rectangular Art Deco watch with Roman numerals and blue cabochon crown.',
        'price': 22500.00,
        'brand': 'Cartier',
        'category': 'Dress',
        'stock_quantity': 14,
        'image_url': 'images/pratik-prasad-ekD-UtzJn9M-unsplash.jpg',
        'average_rating': 4.6,
        'total_reviews': 156
    },
    {
        'name': 'Monaco Calibre 11',
        'description': 'Square chronograph made famous by Steve McQueen, with blue dial and red accents.',
        'price': 29000.00,
        'brand': 'TAG Heuer',
        'category': 'Chronograph',
        'stock_quantity': 8,
        'image_url': 'images/Rolex Submariner Werbung.jpg',
        'average_rating': 4.8,
        'total_reviews': 134
    },
    {
        'name': 'Royal Oak Jumbo',
        'description': 'Ultra-thin luxury sports watch with integrated bracelet and "Grande Tapisserie" dial.',
        'price': 89000.00,
        'brand': 'Audemars Piguet',
        'category': 'Luxury Sport',
        'stock_quantity': 3,
        'image_url': 'images/ -4.jpg',
        'average_rating': 5.0,
        'total_reviews': 92
    },
    {
        'name': 'Superocean Heritage',
        'description': 'Vintage-inspired diving watch with ceramic bezel and mesh bracelet option.',
        'price': 24500.00,
        'brand': 'Breitling',
        'category': 'Diving',
        'stock_quantity': 13,
        'image_url': 'images/ -5.jpg',
        'average_rating': 4.6,
        'total_reviews': 167
    },
    {
        'name': 'Big Pilot Heritage',
        'description': 'Large aviation watch with conical crown and power reserve indicator.',
        'price': 52000.00,
        'brand': 'IWC',
        'category': 'Aviation',
        'stock_quantity': 6,
        'image_url': 'images/andrey-matveev-9mU2L4dVYFA-unsplash.jpg',
        'average_rating': 4.8,
        'total_reviews': 103
    }
]

def add_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Insert new products
        for product in new_products:
            cursor.execute('''
                INSERT INTO products 
                (name, description, price, brand, category, stock_quantity, image_url, average_rating, total_reviews)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                product['name'],
                product['description'],
                product['price'],
                product['brand'],
                product['category'],
                product['stock_quantity'],
                product['image_url'],
                product['average_rating'],
                product['total_reviews']
            ))
        
        conn.commit()
        print(f"✅ Successfully added {len(new_products)} new products to the database!")
        
        # Show total products count
        cursor.execute("SELECT COUNT(*) as total FROM products")
        result = cursor.fetchone()
        print(f"📊 Total products in database: {result['total']}")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error adding products: {e}")
    
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    add_products()
