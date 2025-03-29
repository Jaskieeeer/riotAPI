import requests
import time
class Api_handler:
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def get_match_history(self,puuid):
        """Get match history for a player."""
        current_time = int(time.time())
        two_weeks_ago = current_time - (14 * 24 * 60 * 60)
        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&startTime={two_weeks_ago}&count=100"
        headers = {
            "X-Riot-Token": self.API_KEY
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print("Rate limit exceeded. Waiting for 1 seconds...")
            time.sleep(1)  
            return self.get_match_history(puuid)  # Retry the request
        else:
            print(f"Error getting match history: {response.text}")
            return None

    def get_match_info(self,match_id):
        """Get match information for a match ID."""
        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
        headers = {
            "X-Riot-Token": self.API_KEY
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print("Rate limit exceeded. Waiting for 1 seconds...")
            time.sleep(1)  # Wait for 10 seconds before retrying
            return self.get_match_info(match_id)  # Retry the request
        else:
            print(f"Error getting match information: {response.text}")
            return None
    
    def get_rank_info(self,puuid):
        """Get summoner information for a player."""
        url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
        headers = {
            "X-Riot-Token": self.API_KEY
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print("Rate limit exceeded. Waiting for 1 seconds...")
            time.sleep(1)
            return self.get_rank_info(puuid)
        else:
            print(f"Error getting rank information: {response.text}")
            return None
        
