#!/usr/bin/env python3

from app import get_db_connection

def show_all_tables():
    """Display all tables and their structure in the database"""
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("=" * 60)
        print("DATABASE: login_db")
        print("=" * 60)
        
        # Show all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"\n📋 TABLES ({len(tables)} total):")
        print("-" * 40)
        for table in tables:
            table_name = list(table.values())[0]
            print(f"• {table_name}")
        
        print("\n" + "=" * 60)
        print("TABLE STRUCTURES")
        print("=" * 60)
        
        # Show structure of each table
        for table in tables:
            table_name = list(table.values())[0]
            
            print(f"\n🗂️  TABLE: {table_name}")
            print("-" * 50)
            
            # Show table structure
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            
            print(f"{'Field':<20} {'Type':<20} {'Null':<8} {'Key':<8} {'Default':<15} {'Extra'}")
            print("-" * 90)
            
            for column in columns:
                field = column['Field']
                type_info = column['Type']
                null_info = column['Null']
                key_info = column['Key']
                default_info = str(column['Default']) if column['Default'] is not None else 'NULL'
                extra_info = column['Extra']
                
                print(f"{field:<20} {type_info:<20} {null_info:<8} {key_info:<8} {default_info:<15} {extra_info}")
            
            # Show row count
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = cursor.fetchone()['count']
            print(f"\n📊 Rows: {count}")
            
            # Show sample data for small tables
            if count <= 10 and count > 0:
                print(f"\n📄 Sample Data:")
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                sample_data = cursor.fetchall()
                
                if sample_data:
                    # Print column headers
                    headers = list(sample_data[0].keys())
                    header_line = " | ".join(f"{header:<15}" for header in headers)
                    print(header_line)
                    print("-" * len(header_line))
                    
                    # Print data rows
                    for row in sample_data:
                        row_line = " | ".join(f"{str(row[header]):<15}" for header in headers)
                        print(row_line)
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ Database structure displayed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error displaying database structure: {e}")

if __name__ == '__main__':
    show_all_tables()