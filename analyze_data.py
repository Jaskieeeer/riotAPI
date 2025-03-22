import psycopg2
import sys

def connect_database():
    """Connects to the PostgreSQL database."""
    with open("passy.txt", "r") as f:
        DB_PASSWORD = f.read().strip()  # Strip newline characters

    # Database connection parameters
    DB_NAME = "ritoapi_db"
    DB_USER = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print(f"Connected to database '{DB_NAME}' successfully.")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)
connect_database()

