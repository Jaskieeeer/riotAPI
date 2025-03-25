import psycopg2
import sys
import pandas as pd
def connect_database():
    """Connects to the PostgreSQL database."""
    with open("./passy/passy.txt", "r") as f:
        DB_PASSWORD = f.read().strip()
        
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
conn = connect_database()
query = ("SELECT * FROM summoners")

df = pd.read_sql(query, conn)
query2 = ("SELECT * FROM match_data")
df2 = pd.read_sql(query2, conn)
print(df)
print(df2)
sorted_df_desc = df.sort_values(by='tier', ascending=False)
print(sorted_df_desc)
conn.close()
