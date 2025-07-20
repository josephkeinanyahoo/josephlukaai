from fastapi import FastAPI
import mysql.connector
from mysql.connector import Error
import ssl
import uvicorn

app = FastAPI()

# MySQL connection configuration
db_config = {
    "host": "mysql-clients.default.svc.cluster.local",
    "port": 3306,
    "user": "user_5a4cf2b226a78c56",
    "password": "e#jp6)HV0*HCCLC!@@7ccXZpnKU@s^zC",
    "database": "db_5a4cf2b226a78c56",
    "ssl_ca": "/vault/secrets/tls-clients-ca",
}

@app.get("/create-table")
async def create_table():
    connection = None
    try:
        # Establish MySQL connection with SSL
        connection = mysql.connector.connect(
            host=db_config["host"],
            port=db_config["port"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"],
            ssl_ca=db_config["ssl_ca"],
            ssl_verify_cert=True
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create a simple table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL
            )
            """
            cursor.execute(create_table_query)
            connection.commit()
            
            return {"message": "Table 'users' created successfully"}
            
    except Error as e:
        return {"error": f"Error connecting to MySQL: {str(e)}"}
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            return {"message": "Table created and connection closed successfully"}

@app.get("/")
async def root():
    return {"message": "FastAPI MySQL Service"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6007)
