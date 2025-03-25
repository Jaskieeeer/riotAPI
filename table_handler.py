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
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            print("Table 'summoners' created successfully.")

            cur.execute("""
                CREATE TABLE IF NOT EXISTS match_data (
                match_id VARCHAR(255) PRIMARY KEY,
                duration INTEGER, -- Match duration in seconds
                winner_team INTEGER, -- 1 or 2 (Blue or Red)
                match_date TIMESTAMP 
                );
            """)
            print("Table 'match_data' created successfully.")
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS match_participants (
                    match_id VARCHAR(255),
                    puuid VARCHAR(255),
                    champion VARCHAR(255),
                    team INTEGER, -- 1 (Blue) or 2 (Red)
                    role VARCHAR(50), -- Top, Jungle, Mid, Bot, Support
                    kills INTEGER,
                    deaths INTEGER,
                    assists INTEGER,
                    damage_dealt INTEGER,
                    gold_earned INTEGER,
                    cs INTEGER, -- Creep score
                    vision_score INTEGER,
                    PRIMARY KEY (match_id, puuid),
                    FOREIGN KEY (match_id) REFERENCES match_data(match_id) ON DELETE CASCADE,
                    FOREIGN KEY (puuid) REFERENCES summoners(puuid) ON DELETE CASCADE
                );
            """)
            print("Table 'match_participants' created successfully.")
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
        participants = match['info']['participants']
        duration = match['info']['gameDuration']
        match_date = match['info']['gameCreation']/1000
        winner_team = 1 if participants[0]['win'] else (2 if participants[5]['win'] else 0)
        cursor.execute("""
        INSERT INTO match_data (match_id,  duration, winner_team, match_date)
        VALUES (%s, %s, %s, to_timestamp(%s))
        ON CONFLICT (match_id) DO NOTHING
    """, (match_id, duration, winner_team,match_date))
        for player in participants:
            cursor.execute("""
                INSERT INTO match_participants (
                    match_id, puuid, champion, team, role, 
                    kills, deaths, assists, damage_dealt, gold_earned, cs, vision_score
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (match_id, puuid) DO NOTHING
            """, (
                match_id, player['puuid'], player['championName'], 
                1 if player['teamId'] == 100 else 2,  
                player.get('individualPosition', 'UNKNOWN'),
                player['kills'], player['deaths'], player['assists'],
                player['totalDamageDealtToChampions'], player['goldEarned'],
                player['totalMinionsKilled'] + player['neutralMinionsKilled'],
                player.get('visionScore', 0)
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