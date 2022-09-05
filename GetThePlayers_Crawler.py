import requests
import time
import os

# Getting the token

TOKEN_ENVIRON_NAME = "X-Riot-Token"
token = ""

if "X-Riot-Token" in os.environ:
	token = os.environ[TOKEN_ENVIRON_NAME]
else:
	print("No Riot token available")
	exit()

# Getting the puuid

playerOne = "idusia123"
puuidOne = ""
puuidURL = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + playerOne

head = {
		"X-Riot-Token": token,
  		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
    	"Accept-Language": "en,en-US;q=0.7,pl;q=0.3",
    	"Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    	"Origin": "https://developer.riotgames.com"
		}
body = {"apiName": "summoner-v4", "apiSampleName": "summoner-v4", "methodName": "getBySummonerName", "httpMethod": "GET", "summonerName": playerOne, "execute_against": "EUN1", "app": "440615", "app_key_url": "0"}

r1 = requests.post(puuidURL, headers = head, data = body)
print(r1.status_code)

