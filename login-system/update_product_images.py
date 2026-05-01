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

# Assign specific images to products based on their category and brand
image_assignments = {
    # Rolex products
    1: 'images/watch-1.jpg',      # Royal Classic - Dress
    7: 'images/watch-6.jpg',      # Submariner Deep Sea - Diving
    15: 'images/watch-2.jpg',     # Daytona Cosmograph - Chronograph
    
    # Omega products
    5: 'images/watch-5.jpg',      # Master Chronograph
    8: 'images/watch-5.jpg',      # Speedmaster Moonwatch - Chronograph
    16: 'images/watch-4.jpg',     # Seamaster Aqua Terra - Luxury Sport
    
    # Patek Philippe products
    3: 'images/watch-9.jpg',      # Diamond Prestige - Luxury Sport
    9: 'images/watch-9.jpg',      # Nautilus Steel - Luxury Sport
    17: 'images/watch-3.jpg',     # Calatrava White Gold - Dress
    
    # Cartier products
    4: 'images/watch-7.jpg',      # Rose Elegance - Dress
    10: 'images/watch-7.jpg',     # Santos de Cartier - Dress
    18: 'images/watch-3.jpg',     # Tank Must - Dress
    
    # TAG Heuer products
    2: 'images/watch-4.jpg',      # Titanium Sport - Luxury Sport
    11: 'images/watch-5.jpg',     # Carrera Calibre 16 - Chronograph
    19: 'images/watch-8.jpg',     # Monaco Calibre 11 - Chronograph
    
    # Audemars Piguet products
    6: 'images/watch-9.jpg',      # Skeleton Master - Luxury Sport
    12: 'images/watch-9.jpg',     # Royal Oak Offshore - Luxury Sport
    20: 'images/watch-9.jpg',     # Royal Oak Jumbo - Luxury Sport
    
    # Breitling products
    13: 'images/watch-10.jpg',    # Navitimer B01 - Aviation
    21: 'images/watch-6.jpg',     # Superocean Heritage - Diving
    
    # IWC products
    14: 'images/watch-3.jpg',     # Portugieser Chronograph - Dress
    22: 'images/watch-10.jpg',    # Big Pilot Heritage - Aviation
}

def update_images():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        for product_id, image_url in image_assignments.items():
            cursor.execute('''
                UPDATE products 
                SET image_url = %s 
                WHERE id = %s
            ''', (image_url, product_id))
        
        conn.commit()
        print(f"✅ Successfully updated images for {len(image_assignments)} products!")
        
        # Show sample of updated products
        cursor.execute("""
            SELECT id, name, brand, category, image_url 
            FROM products 
            ORDER BY brand, name 
            LIMIT 10
        """)
        
        print("\n📸 Sample of updated products:")
        print("-" * 80)
        for product in cursor.fetchall():
            print(f"ID {product['id']}: {product['name']} ({product['brand']}) - {product['image_url']}")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error updating images: {e}")
    
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    update_images()
