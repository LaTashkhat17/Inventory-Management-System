import pymysql

# MySQL connection settings
HOST = 'localhost'
USER = 'root'
PASSWORD = ''  # No password
DATABASE = 'pos_system'

def create_database():
    try:
        # Connect to MySQL server
        connection = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )
        
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
        print(f"Database '{DATABASE}' created successfully")
        
        cursor.close()
        connection.close()
        
        print("\nDatabase setup complete!")
        print("You can now run the application with: python main.py")
        
    except Exception as e:
        print(f"Error creating database: {e}")
        print("\nMake sure MySQL is running and accessible.")

if __name__ == "__main__":
    print("="*50)
    print("POS System - Database Setup")
    print("="*50)
    print("\nCreating MySQL database...")
    create_database()

