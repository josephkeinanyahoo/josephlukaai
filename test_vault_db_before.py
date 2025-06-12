#!/usr/bin/env python3
import os
import json
from datetime import datetime

def test_vault_secrets():
    """Test database connection using Vault-injected secrets"""
    
    print("=== Vault Database Test ===")
    print(f"Pod: {os.environ.get('HOSTNAME', 'unknown')}")
    print(f"Time: {datetime.now()}")
    
    # Source the Vault secrets
    os.system('source /vault/secrets/config')
    
    # Read the secrets file directly
    secrets = {}
    try:
        with open('/vault/secrets/config', 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    value = value.strip('"').strip("'")
                    secrets[key] = value
        
        print(f"\n✓ Loaded {len(secrets)} secrets from Vault")
        print("\nDatabase-related secrets found:")
        
        # List all database-related secrets
        db_secrets = [k for k in secrets.keys() if 'DB' in k or 'DATABASE' in k or 'MYSQL' in k]
        for key in sorted(db_secrets):
            if 'PASSWORD' in key.upper():
                print(f"  - {key}: ***hidden***")
            else:
                print(f"  - {key}: {secrets[key]}")
        
        # Try to connect to database using different credential sets
        # First try DB_* variables
        if all(k in secrets for k in ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']):
            print("\n\nTrying connection with DB_* credentials...")
            test_mysql_connection(
                secrets['DB_HOST'],
                secrets.get('DB_PORT', '3306'),
                secrets['DB_USER'],
                secrets['DB_PASSWORD'],
                secrets['DB_NAME']
            )
        
        # Then try DATABASE_* variables
        elif all(k in secrets for k in ['DATABASE_HOST', 'DATABASE_USER', 'DATABASE_PASSWORD', 'DATABASE_NAME']):
            print("\n\nTrying connection with DATABASE_* credentials...")
            test_mysql_connection(
                secrets['DATABASE_HOST'],
                secrets.get('DATABASE_PORT', '3306'),
                secrets['DATABASE_USER'],
                secrets['DATABASE_PASSWORD'],
                secrets['DATABASE_NAME']
            )
        
        # Finally try MYSQL_* variables
        elif all(k in secrets for k in ['MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DATABASE']):
            print("\n\nTrying connection with MYSQL_* credentials...")
            test_mysql_connection(
                secrets['MYSQL_HOST'],
                secrets.get('MYSQL_PORT', '3306'),
                secrets['MYSQL_USER'],
                secrets['MYSQL_PASSWORD'],
                secrets['MYSQL_DATABASE']
            )
        else:
            print("\n✗ No complete set of database credentials found!")
            print("Available secrets:", list(secrets.keys()))
            
    except Exception as e:
        print(f"\n✗ Error reading Vault secrets: {str(e)}")
        print(f"File exists: {os.path.exists('/vault/secrets/config')}")

def test_mysql_connection(host, port, user, password, database):
    """Test MySQL connection and create test table"""
    try:
        import pymysql
        
        print(f"Connecting to {host}:{port} as {user}...")
        
        connection = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            connect_timeout=10
        )
        
        print("✓ Connected successfully!")
        
        with connection.cursor() as cursor:
            # Create test table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vault_test (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    test_name VARCHAR(255),
                    test_value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✓ Created test table")
            
            # Insert test data
            cursor.execute(
                "INSERT INTO vault_test (test_name, test_value) VALUES (%s, %s)",
                ("vault_integration", f"Test from pod {os.environ.get('HOSTNAME', 'unknown')}")
            )
            connection.commit()
            print("✓ Inserted test data")
            
            # Query data
            cursor.execute("SELECT * FROM vault_test ORDER BY id DESC LIMIT 5")
            results = cursor.fetchall()
            
            print("\nRecent test records:")
            for row in results:
                print(f"  ID: {row[0]}, Name: {row[1]}, Value: {row[2]}, Time: {row[3]}")
        
        connection.close()
        print("\n✓ Database test completed successfully!")
        
    except ImportError:
        print("✗ pymysql not installed. Install it with: pip install pymysql")
    except Exception as e:
        print(f"✗ Database connection failed: {str(e)}")

if __name__ == "__main__":
    test_vault_secrets()
