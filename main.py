from fastapi import FastAPI
import mysql.connector
from mysql.connector import Error
import ssl # Although not directly used for context in this snippet, it's kept for completeness
import uvicorn
import logging

# Configure logging to see messages in the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# MySQL connection configuration
db_config = {
    "host": "mysql-clients.default.svc.cluster.local",
    "port": 3306,
    "user": "user_5a4cf2b226a78c56",
    "password": "e#jp6)HV0*HCCLC!@@7ccXZpnKU@s^zC",
    "database": "db_5a4cf2b226a78c56",
    "ssl_ca":  "/vault/secrets/tls-clients-ca"
}

@app.get("/")
async def root():
    """
    Handles requests to the root path.
    Attempts to connect to MySQL and create the 'users' table.
    Logs database connection status and errors.
    """
    connection = None
    try:
        logger.info("Attempting to connect to MySQL database...")
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
            logger.info("Successfully connected to MySQL database!")
            cursor = connection.cursor()

            # Create a simple table if it doesn't exist
            create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL
            )
            """
            cursor.execute(create_table_query)
            connection.commit()
            logger.info("Table 'users' creation/check completed successfully.")
            return {"message": "FastAPI MySQL Service - Table 'users' created/checked."}
        else:
            logger.warning("Failed to establish a connection to MySQL database.")
            return {"message": "FastAPI MySQL Service - Could not connect to database."}

    except Error as e:
        logger.error(f"Error connecting to MySQL or creating table: {e}", exc_info=True)
        return {"error": f"Error during database operation: {str(e)}"}

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            logger.info("MySQL connection closed.")

@app.get("/health")
async def health_check():
    """
    Health check endpoint for container monitoring.
    """
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6007)

