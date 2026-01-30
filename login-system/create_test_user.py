#!/usr/bin/env python3

from app import get_db_connection, init_db, migrate_db
from werkzeug.security import generate_password_hash

def create_test_user():
    """Create a test user for login testing"""
    
    print("🔧 Creating test user...")
    
    try:
        # Initialize and migrate database first
        init_db()
        migrate_db()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if test user already exists
        cursor.execute('SELECT * FROM users WHERE username = %s', ('testuser',))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print("✅ Test user already exists")
            print("   Username: testuser")
            print("   Password: testpass")
        else:
            # Create test user
            hashed_password = generate_password_hash('testpass')
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', 
                          ('testuser', hashed_password))
            conn.commit()
            print("✅ Test user created successfully!")
            print("   Username: testuser")
            print("   Password: testpass")
        
        # Show user count
        cursor.execute('SELECT COUNT(*) as count FROM users')
        user_count = cursor.fetchone()['count']
        print(f"📊 Total users in database: {user_count}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        return False

if __name__ == '__main__':
    create_test_user()