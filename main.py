from queue import Queue
import requests
from db_handler import connect_database
from table_handler import TableHandler
from api_handler import Api_handler
import time
import psycopg2


with open("api.txt", "r") as f:
    API_KEY = f.read().strip() 





if __name__ == "__main__":
    conn = connect_database()
    summonerqueue = Queue()
    matchqueue = Queue()
    table_handler = TableHandler(conn)
    api_handler = Api_handler(API_KEY)
    summoner_name = "8eYntZix4bgjDBdgKk-Cv9Me7Im-BPtYEH2T60cPbpALgi9WqBX-AyDsUk7vX-YCAlj3IIZHxaGGpg"
    match_data = api_handler.get_match_info("EUW1_7341534749")

    i = 0
    summonerqueue.put(summoner_name)


    table_handler.drop_all_tables()
    table_handler.list_all_tables()
    table_handler.create_tables()
    table_handler.list_all_tables()
    
    table_handler.show_table( "match_data")
    table_handler.clear_table( "match_data")
    table_handler.show_table( "match_data")
    try:
        while not summonerqueue.empty() and matchqueue.qsize() < 10:
            summoner = summonerqueue.get()
            for id in api_handler.get_match_history(summoner):
                matchqueue.put(id)
            while not matchqueue.empty()and i < 10 :
                match = matchqueue.get()
                match_data = api_handler.get_match_info(match)
                table_handler.save_match_data_to_db(conn, match_data)
                for player in match_data["info"]["participants"]:
                    summonerqueue.put(player["puuid"])
                    rank_info = api_handler.get_rank_info(player["puuid"])
                    name = player["riotIdGameName"]
                    tagline = player["riotIdTagline"]
                print(f"Processed match: {match}")
                i += 1
        table_handler.show_table("match_data")
    except Exception as e:
        print(e)
    finally:
        conn.close()