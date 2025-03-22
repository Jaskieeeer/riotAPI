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
                    losses INTEGER
                );
            """)
            print("Table 'summoners' created successfully.")

            cur.execute("""
                CREATE TABLE IF NOT EXISTS match_data (
                    match_id VARCHAR(255),
                    puuid1 VARCHAR(255),
                    champion1 VARCHAR(255),
                    puuid2 VARCHAR(255),
                    champion2 VARCHAR(255),
                    puuid3 VARCHAR(255),
                    champion3 VARCHAR(255),
                    puuid4 VARCHAR(255),
                    champion4 VARCHAR(255),
                    puuid5 VARCHAR(255),
                    champion5 VARCHAR(255),
                    puuid6 VARCHAR(255),
                    champion6 VARCHAR(255),
                    puuid7 VARCHAR(255),
                    champion7 VARCHAR(255),
                    puuid8 VARCHAR(255),
                    champion8 VARCHAR(255),
                    puuid9 VARCHAR(255),
                    champion9 VARCHAR(255),
                    puuid10 VARCHAR(255),
                    champion10 VARCHAR(255),
                    FOREIGN KEY (puuid1) REFERENCES summoners(puuid) ON DELETE CASCADE,
                    FOREIGN KEY (puuid2) REFERENCES summoners(puuid) ON DELETE CASCADE,
                    FOREIGN KEY (puuid3) REFERENCES summoners(puuid) ON DELETE CASCADE,
                    FOREIGN KEY (puuid4) REFERENCES summoners(puuid) ON DELETE CASCADE,
                    FOREIGN KEY (puuid5) REFERENCES summoners(puuid) ON DELETE CASCADE,
                    FOREIGN KEY (puuid6) REFERENCES summoners(puuid) ON DELETE CASCADE,
                    FOREIGN KEY (puuid7) REFERENCES summoners(puuid) ON DELETE CASCADE,
                    FOREIGN KEY (puuid8) REFERENCES summoners(puuid) ON DELETE CASCADE,
                    FOREIGN KEY (puuid9) REFERENCES summoners(puuid) ON DELETE CASCADE,
                    FOREIGN KEY (puuid10) REFERENCES summoners(puuid) ON DELETE CASCADE
                );
            """)
            print("Table 'match_data' created successfully.")
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
                %s, %s, %s,
                %s, %s, 
                %s, %s, 
                %s, %s, 
                %s, %s, 
                %s, %s, 
                %s, %s, 
                %s, %s, 
                %s, %s, 
                %s, %s
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
    
    def save_summoner_data_to_db(self, rank_info,puuid,name,tagline):
        """Save summoner data to a PostgreSQL table."""
        cursor = self.conn.cursor()
        if len(rank_info) != 0:
            
            cursor.execute("""
                INSERT INTO summoners (
                    puuid, name, tagline, tier, rank, lp, wins, losses
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                puuid, name, tagline, rank_info[0]['tier'], rank_info[0]['rank'], rank_info[0]['leaguePoints'], rank_info[0]['wins'], rank_info[0]['losses']
            ))
        else:
            cursor.execute("""
                INSERT INTO summoners (
                    puuid, name, tagline
                ) VALUES (
                    %s, %s, %s
                )
            """, (
                puuid, name, tagline
            ))
        self.conn.commit()


    def check_if_summoner_in_db(self, puuid):
        """Check if a summoner is already in the database."""
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT 1 FROM summoners WHERE puuid = '{puuid}'")
        exists = cursor.fetchone()
        cursor.close()
        return exists

    def check_if_match_in_db(self, match_id):
        """Check if a match is already in the database."""
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT 1 FROM match_data WHERE match_id = '{match_id}'")
        exists = cursor.fetchone()
        cursor.close()
        return exists