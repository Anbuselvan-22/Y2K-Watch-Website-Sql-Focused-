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

# Update old products with brand and category
updates = [
    {'id': 1, 'brand': 'Rolex', 'category': 'Dress'},
    {'id': 2, 'brand': 'TAG Heuer', 'category': 'Luxury Sport'},
    {'id': 3, 'brand': 'Patek Philippe', 'category': 'Luxury Sport'},
    {'id': 4, 'brand': 'Cartier', 'category': 'Dress'},
    {'id': 5, 'brand': 'Omega', 'category': 'Chronograph'},
    {'id': 6, 'brand': 'Audemars Piguet', 'category': 'Luxury Sport'}
]

def update_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        for update in updates:
            cursor.execute('''
                UPDATE products 
                SET brand = %s, category = %s 
                WHERE id = %s
            ''', (update['brand'], update['category'], update['id']))
        
        conn.commit()
        print(f"✅ Successfully updated {len(updates)} existing products with brand and category!")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error updating products: {e}")
    
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    update_products()
