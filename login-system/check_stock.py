#!/usr/bin/env python3

from app import get_db_connection

def check_and_update_stock():
    """Check current stock levels and update them"""
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("🔍 Checking current stock levels...")
        print("-" * 50)
        
        # Check current stock
        cursor.execute('SELECT id, name, stock_quantity FROM products')
        products = cursor.fetchall()
        
        for product in products:
            print(f"ID: {product['id']} | {product['name']:<20} | Stock: {product['stock_quantity']}")
        
        print("\n📦 Updating stock levels to reasonable amounts...")
        print("-" * 50)
        
        # Update stock levels
        stock_updates = [
            (25, 1),  # Royal Classic - 25 in stock
            (30, 2),  # Titanium Sport - 30 in stock
            (5, 3),   # Diamond Prestige - 5 in stock (luxury item)
            (20, 4),  # Rose Elegance - 20 in stock
            (15, 5),  # Master Chronograph - 15 in stock
            (12, 6),  # Skeleton Master - 12 in stock
        ]
        
        for stock, product_id in stock_updates:
            cursor.execute('UPDATE products SET stock_quantity = %s WHERE id = %s', (stock, product_id))
            print(f"✅ Updated product ID {product_id} to {stock} units")
        
        conn.commit()
        
        print("\n🎯 Final stock levels:")
        print("-" * 50)
        
        # Check updated stock
        cursor.execute('SELECT id, name, stock_quantity FROM products')
        products = cursor.fetchall()
        
        total_stock = 0
        for product in products:
            print(f"ID: {product['id']} | {product['name']:<20} | Stock: {product['stock_quantity']}")
            total_stock += product['stock_quantity']
        
        print(f"\n📊 Total inventory: {total_stock} units")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Stock levels updated successfully!")
        
    except Exception as e:
        print(f"❌ Error updating stock: {e}")

if __name__ == '__main__':
    check_and_update_stock()