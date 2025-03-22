import sys
class TableHandler:

    def __init__(self,conn):
        self.conn = conn


    def create_tables(self):

        cur = self.conn.cursor()
        try:
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS summoners (
                        puuid VARCHAR(255) PRIMARY KEY,
                        name VARCHAR(255),
                        tagline VARCHAR(255),
                        tier VARCHAR(255),
                        rank VARCHAR(255),
                        lp INTEGER,
                        wins INTEGER,
                        losses INTEGER,

                    );
                """)
            print("Table 'summoners' created successfully.")

            # Create `matches` table
            
            cur.execute("""
                        CREATE TABLE if not exists match_data (
            match_id VARCHAR(255),
            puuid_1 VARCHAR(255),
            champion_1 VARCHAR(255),
            puuid_2 VARCHAR(255),
            champion_2 VARCHAR(255),
            puuid_3 VARCHAR(255),
            champion_3 VARCHAR(255),
            puuid_4 VARCHAR(255),
            champion_4 VARCHAR(255),
            puuid_5 VARCHAR(255),
            champion_5 VARCHAR(255),
            puuid_6 VARCHAR(255),
            champion_6 VARCHAR(255),
            puuid_7 VARCHAR(255),
            champion_7 VARCHAR(255),
            puuid_8 VARCHAR(255),
            champion_8 VARCHAR(255),
            puuid_9 VARCHAR(255),
            champion_9 VARCHAR(255),
            puuid_10 VARCHAR(255),
            champion_10 VARCHAR(255)
            FOREIGN KEY (puuid_1) REFERENCES summoners(puuid) ON DELETE CASCADE,
            FOREIGN KEY (puuid_2) REFERENCES summoners(puuid) ON DELETE CASCADE,
            FOREIGN KEY (puuid_3) REFERENCES summoners(puuid) ON DELETE CASCADE,
            FOREIGN KEY (puuid_4) REFERENCES summoners(puuid) ON DELETE CASCADE,
            FOREIGN KEY (puuid_5) REFERENCES summoners(puuid) ON DELETE CASCADE,
            FOREIGN KEY (puuid_6) REFERENCES summoners(puuid) ON DELETE CASCADE,
            FOREIGN KEY (puuid_7) REFERENCES summoners(puuid) ON DELETE CASCADE,
            FOREIGN KEY (puuid_8) REFERENCES summoners(puuid) ON DELETE CASCADE,
            FOREIGN KEY (puuid_9) REFERENCES summoners(puuid) ON DELETE CASCADE,
            FOREIGN KEY (puuid_10) REFERENCES summoners(puuid) ON DELETE CASCADE
                        );
                        """)
            print("Table 'match_table' created successfully.")
            # Commit changes and close connection
            self.conn.commit()
            cur.close()

        except Exception as e:
            print(f"Error creating tables: {e}")
            sys.exit(1)





    def clear_table(self,table_name):
        """Clears a PostgreSQL table."""
        cur = self.conn.cursor()
        cur.execute(f"TRUNCATE TABLE {table_name} CASCADE")
        self.conn.commit()
        cur.close()

    def show_table(self,table_name):
        """Shows a PostgreSQL table."""
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()

    def drop_all_tables(self):
        """Drops all PostgreSQL tables."""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        rows = cur.fetchall()
        for row in rows:
            cur.execute(f"DROP TABLE {row[0]} CASCADE")
        self.conn.commit()
        cur.close()

    def list_all_tables(self):
        """Lists all PostgreSQL tables."""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        rows = cur.fetchall()
        for row in rows:
            print(row[0])
        cur.close()
    
    def save_match_data_to_db(self, match):
        """Save match data to a PostgreSQL table."""
        cursor = self.conn.cursor()

        match_id = match['metadata']['matchId']
        players = match['info']['participants']
        cursor.execute("""
            INSERT INTO match_data (
                match_id, puuid1, champion1,
                puuid2, champion2,
                puuid3, champion3,
                puuid4, champion4,
                puuid5, champion5,
                puuid6, champion6,
                puuid7, champion7,
                puuid8, champion8,
                puuid9, champion9,
                puuid10, champion10
                
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s
            )
        """, (
            match_id,
            players[0]['puuid'], players[0]['championName'],
            players[1]['puuid'], players[1]['championName'],
            players[2]['puuid'], players[2]['championName'],
            players[3]['puuid'], players[3]['championName'],
            players[4]['puuid'], players[4]['championName'],
            players[5]['puuid'], players[5]['championName'],
            players[6]['puuid'], players[6]['championName'],
            players[7]['puuid'], players[7]['championName'],
            players[8]['puuid'], players[8]['championName'],
            players[9]['puuid'], players[9]['championName'],

        
        ))
        self.conn.commit()


