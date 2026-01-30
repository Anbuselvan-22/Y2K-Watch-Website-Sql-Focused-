#!/usr/bin/env python3

from app import get_db_connection
import datetime

def create_sample_orders():
    """Create sample orders for testing the profile page"""
    
    print("🛍️ Creating sample orders...")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get test user ID
        cursor.execute('SELECT id FROM users WHERE username = %s', ('testuser',))
        user = cursor.fetchone()
        
        if not user:
            print("❌ Test user not found. Run create_test_user.py first.")
            return False
        
        user_id = user['id']
        
        # Check if orders already exist
        cursor.execute('SELECT COUNT(*) as count FROM orders WHERE user_id = %s', (user_id,))
        existing_orders = cursor.fetchone()['count']
        
        if existing_orders > 0:
            print(f"✅ User already has {existing_orders} orders")
            return True
        
        # Get some products for the orders
        cursor.execute('SELECT id, name, price FROM products LIMIT 5')
        products = cursor.fetchall()
        
        if not products:
            print("❌ No products found. Make sure products are loaded.")
            return False
        
        # Create sample orders
        orders_data = [
            {
                'total': 25000.00,
                'status': 'completed',
                'items': [
                    {'product_id': products[0]['id'], 'quantity': 1, 'price': products[0]['price']}
                ]
            },
            {
                'total': 37500.00,
                'status': 'completed', 
                'items': [
                    {'product_id': products[1]['id'], 'quantity': 1, 'price': products[1]['price']},
                    {'product_id': products[2]['id'], 'quantity': 1, 'price': products[2]['price']}
                ]
            },
            {
                'total': 15200.00,
                'status': 'pending',
                'items': [
                    {'product_id': products[3]['id'], 'quantity': 1, 'price': products[3]['price']}
                ]
            }
        ]
        
        for order_data in orders_data:
            # Create order
            cursor.execute('''
                INSERT INTO orders (user_id, total_amount, status, order_date) 
                VALUES (%s, %s, %s, %s)
            ''', (user_id, order_data['total'], order_data['status'], datetime.datetime.now()))
            
            order_id = cursor.lastrowid
            
            # Add order items
            for item in order_data['items']:
                cursor.execute('''
                    INSERT INTO order_items (order_id, product_id, quantity, price)
                    VALUES (%s, %s, %s, %s)
                ''', (order_id, item['product_id'], item['quantity'], item['price']))
        
        conn.commit()
        
        # Show results
        cursor.execute('SELECT COUNT(*) as count FROM orders WHERE user_id = %s', (user_id,))
        order_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT SUM(total_amount) as total FROM orders WHERE user_id = %s', (user_id,))
        total_spent = cursor.fetchone()['total']
        
        print(f"✅ Created {order_count} sample orders")
        print(f"💰 Total spent: ${total_spent:.2f}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample orders: {e}")
        return False

if __name__ == '__main__':
    create_sample_orders()