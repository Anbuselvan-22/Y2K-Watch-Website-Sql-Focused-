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

# Replace all product images with your custom watch images
# Distributing watch-1.jpg through watch-10.jpg across all 22 products
image_replacements = {
    1: 'images/watch-1.jpg',
    2: 'images/watch-2.jpg',
    3: 'images/watch-3.jpg',
    4: 'images/watch-4.jpg',
    5: 'images/watch-5.jpg',
    6: 'images/watch-6.jpg',
    7: 'images/watch-7.jpg',
    8: 'images/watch-8.jpg',
    9: 'images/watch-9.jpg',
    10: 'images/watch-10.jpg',
    11: 'images/watch-1.jpg',
    12: 'images/watch-2.jpg',
    13: 'images/watch-3.jpg',
    14: 'images/watch-4.jpg',
    15: 'images/watch-5.jpg',
    16: 'images/watch-6.jpg',
    17: 'images/watch-7.jpg',
    18: 'images/watch-8.jpg',
    19: 'images/watch-9.jpg',
    20: 'images/watch-10.jpg',
    21: 'images/watch-1.jpg',
    22: 'images/watch-2.jpg',
}

def replace_images():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        for product_id, image_url in image_replacements.items():
            cursor.execute('''
                UPDATE products 
                SET image_url = %s 
                WHERE id = %s
            ''', (image_url, product_id))
        
        conn.commit()
        print(f"✅ Successfully replaced images for all {len(image_replacements)} products!")
        
        # Show updated products
        cursor.execute("""
            SELECT id, name, image_url 
            FROM products 
            ORDER BY id
        """)
        
        print("\n📸 Updated product images:")
        print("-" * 70)
        for product in cursor.fetchall():
            print(f"ID {product['id']:2d}: {product['name']:30s} → {product['image_url']}")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error replacing images: {e}")
    
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    replace_images()
