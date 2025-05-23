import psycopg2
import sys
import pandas as pd
import table_handler
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
def count_divisions():
    query = ("SELECT tier, COUNT(*) FROM summoners GROUP BY tier")
    df = pd.read_sql(query, conn)
    print(df)
count_divisions()

def save_data_to_csv():
    query = ("SELECT * FROM summoners")
    df = pd.read_sql(query, conn)
    df.to_csv("summoners.csv")

def save_match_data_to_csv():
    query = ("SELECT * FROM match_data")
    df = pd.read_sql(query, conn)
    df.to_csv("match_data.csv")

def save_match_participants_to_csv():
    query = ("SELECT * FROM match_participants")
    df = pd.read_sql(query, conn)
    df.to_csv("match_participants.csv")
def count_roles():
    query = ("SELECT role, COUNT(*) FROM match_participants GROUP BY role")
    df = pd.read_sql(query, conn)
    print(df)
count_roles()
table_handler = table_handler.TableHandler(conn)
table_handler.create_tables()
table_handler.populate_champion_stats()

df = pd.read_sql(query, conn)
query2 = ("SELECT * FROM match_data")
df2 = pd.read_sql(query2, conn)
df3 = pd.read_sql("SELECT * FROM match_participants", conn)
query4 = ("SELECT * FROM champion_stats where games_played > 50 order by avg_kda desc")
df4 = pd.read_sql(query4, conn)
print(df)
print(df2)
print(df3)
print(df4)
save_data_to_csv()
save_match_data_to_csv()
save_match_participants_to_csv()
conn.close()
