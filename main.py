from queue import Queue
import requests
from db_handler import connect_database
from table_handler import TableHandler
from api_handler import Api_handler
import time
import psycopg2
import json
import signal
import sys


def cleanup (signal, frame):
    print("Cleaning up")
    try:
            if conn:
                conn.close()
                print("Database connection closed.")
    except NameError:
        print("No database connection to close.")
    sys.exit(0)
signal.signal(signal.SIGINT, cleanup)

with open("./passy/api.txt", "r") as f:
    API_KEY = f.read().strip() 

def write_to_json(data):
    with open("response.json", "w") as f:
        f.write(json.dumps(data, indent=4))

def queue_print(queue):
    for item in list(queue.queue):
        print(item)



if __name__ == "__main__":
    api_handler = Api_handler(API_KEY)
    conn = connect_database()
    summonerqueue = Queue()
    matchqueue = Queue()
    table_handler = TableHandler(conn)
    
    summoner_name = "612V7U02pa_cGWxqGzWJpb7rB6xxU8By-kn4YFsLC-uOT56MaCTIjJKXblqkStWnlHz_CYO64JLltg"
    
    i = 0
    summonerqueue.put(summoner_name)


    table_handler.drop_all_tables()
    table_handler.list_all_tables()
    table_handler.create_tables()
    table_handler.list_all_tables()
    
    table_handler.show_table( "match_data")
    table_handler.clear_table( "match_data")
    table_handler.show_table( "match_data")
    j=0
    try:
        while not summonerqueue.empty():
            
            summoner = summonerqueue.get()
            for id in api_handler.get_match_history(summoner):
                matchqueue.put(id)
            while not matchqueue.empty():
                match = matchqueue.get()
                if not table_handler.check_if_match_in_db(match):
                    match_data = api_handler.get_match_info(match)
                    print("processing match", match)
                    
                    for player in match_data["info"]["participants"]:
                        if not table_handler.check_if_summoner_in_db(player["puuid"]):
                            summonerqueue.put(player["puuid"])

                            rank_info = api_handler.get_rank_info(player["puuid"])

                            name = player["riotIdGameName"]
                            tagline = player["riotIdTagline"]
                            table_handler.save_summoner_data_to_db(rank_info,player["puuid"],name, tagline)
                    table_handler.save_match_data_to_db(match_data)
                    
                    print(f"Processed match: {match}")
                    i += 1
            j+=1
            print(matchqueue.qsize())
            
        table_handler.show_table("match_data")
        table_handler.show_table("summoners")
    except KeyboardInterrupt:
        cleanup(None, None)
    except Exception as e:
        print(e)
    finally:
        conn.close()