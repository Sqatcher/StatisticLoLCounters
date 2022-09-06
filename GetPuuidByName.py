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

playerOne = "Lord Of Rings 12"
puuidOne = ""
puuidURL = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + playerOne

head = {
		"X-Riot-Token": token
		}
r1 = requests.get(puuidURL, headers = head)

if r1.status_code != 200:
	print("Request failed, status code: " + str(r1.status_code))
	exit()
#print(r1.json())
puuidOne = r1.json()["puuid"]
print(puuidOne)
