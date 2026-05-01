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

def revert_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Delete products with ID 7-22 (the ones we added)
        cursor.execute("DELETE FROM products WHERE id >= 7")
        deleted_count = cursor.rowcount
        
        # Update original 6 products with proper images
        original_images = {
            1: 'images/watch-1.jpg',
            2: 'images/watch-2.jpg',
            3: 'images/watch-3.jpg',
            4: 'images/watch-4.jpg',
            5: 'images/watch-5.jpg',
            6: 'images/watch-6.jpg',
        }
        
        for product_id, image_url in original_images.items():
            cursor.execute('''
                UPDATE products 
                SET image_url = %s 
                WHERE id = %s
            ''', (image_url, product_id))
        
        conn.commit()
        print(f"✅ Successfully deleted {deleted_count} added products!")
        print(f"✅ Reverted to original 6 products with updated images!")
        
        # Show remaining products
        cursor.execute("""
            SELECT id, name, brand, category, price, image_url 
            FROM products 
            ORDER BY id
        """)
        
        print("\n📊 Current products in database:")
        print("-" * 90)
        for product in cursor.fetchall():
            print(f"ID {product['id']}: {product['name']:25s} | {product['brand']:15s} | ${product['price']:>10.2f} | {product['image_url']}")
        
        cursor.execute("SELECT COUNT(*) as total FROM products")
        result = cursor.fetchone()
        print("-" * 90)
        print(f"Total products: {result['total']}")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error reverting products: {e}")
    
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    revert_products()
