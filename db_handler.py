import sys
import locale
import os
import psycopg2



def create_database():
    """Creates a database with UTF-8 encoding if it doesn't exist."""
        # Force UTF-8 encoding
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.stdout.reconfigure(encoding='utf-8')
    print(f"System Encoding: {locale.getpreferredencoding()}")

    # Read password securely
    with open("passy.txt", "r") as f:
        DB_PASSWORD = f.read().strip()  # Strip newline characters

    # Database connection parameters
    DB_NAME = "ritoapi_db"
    DB_USER = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    try:
        # Connect to 'postgres' system database first
        conn = psycopg2.connect(
            dbname=DB_NAME, # Default system database
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Check if database exists
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")
        exists = cur.fetchone()

        if not exists:
            cur.execute(f"""
                CREATE DATABASE {DB_NAME} 
                WITH ENCODING 'UTF8' 
                LC_COLLATE='pl_PL.UTF-8' 
                LC_CTYPE='pl_PL.UTF-8' 
                TEMPLATE template0;
            """)
            print(f"Database '{DB_NAME}' created successfully.")
        else:
            print(f"Database '{DB_NAME}' already exists.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")
        sys.exit(1)

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

