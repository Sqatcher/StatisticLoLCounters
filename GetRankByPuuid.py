import requests
import time
import os
import json
import psycopg2
from getpass import getpass

DATA_BASE_NAME = "lolmatches1"
USERNAME = "postgres"

databasePassword = getpass("Password for user " + USERNAME + ": ")

dbConnection = psycopg2.connect(
	host = "localhost",
	database = DATA_BASE_NAME,
	user = USERNAME,
	password = databasePassword
	#port = 5432 #- default
)
dbCursor = dbConnection.cursor()

UPDATE_SQL = "UPDATE players SET id = %s, solorank = %s, flexrank = %s WHERE puuid = %s"
# Getting the token

SLEEP_503 = 120
SLEEP_429 = 60
TOKEN_ENVIRON_NAME = "X-Riot-Token"
token = ""

if "X-Riot-Token" in os.environ:
	token = os.environ[TOKEN_ENVIRON_NAME]
else:
	print("No Riot token available")
	exit()

with open("GetRankNumber.txt", 'r') as f:
	rankNumber = int(f.readline())


sleepTime = 120/100 + 0.1         # 100 every 2 minutes is max
head = {"X-Riot-Token": token}

with open("PlayersWithRank.txt", 'r') as f:
	for i in range(rankNumber):
		f.readline()
	for line in f:
		puuid = line.strip()
		if len(puuid) < 70:
			print("BOT detected, skipping the entry")
			continue
		print("Downloading id for " + puuid)
		accountURL = f"https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"

		while True:		
			time.sleep(sleepTime)	
			r1 = requests.get(accountURL, headers = head)
			if r1.status_code != 200:
				print("Request failed, status code: " + str(r1.status_code))

				if r1.status_code == 503:
					print("Error 503 - service unavailable. Sleeping " + str(SLEEP_503) + " seconds")
					time.sleep(SLEEP_503)
				else:
					if r1.status_code == 429:
						print("Error 429 - Rate Limit Exceeded. Sleeping " + str(SLEEP_429) + " seconds")
						time.sleep(SLEEP_429)
					else:
						break
			else:
				break
		if r1.status_code != 200:
			break

		accountData = r1.json()
		id = accountData["id"]
		
		print("Downloading ranked info for  " + puuid)
		rankURL = f"https://eun1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}"

		while True:		
			time.sleep(sleepTime)	
			r1 = requests.get(rankURL, headers = head)
			if r1.status_code != 200:
				print("Request failed, status code: " + str(r1.status_code))

				if r1.status_code == 503:
					print("Error 503 - service unavailable. Sleeping " + str(SLEEP_503) + " seconds")
					time.sleep(SLEEP_503)
				else:
					if r1.status_code == 429:
						print("Error 429 - Rate Limit Exceeded. Sleeping " + str(SLEEP_429) + " seconds")
						time.sleep(SLEEP_429)
					else:
						break
			else:
				break
		if r1.status_code != 200:
			break

		rankData = r1.json()
		flexRank = ""
		soloRank = ""

		for rank in rankData:
			if rank["queueType"] == "RANKED_SOLO_5x5":
				soloRank = rank["tier"] + " " + rank["rank"]
			else:
				flexRank = rank["tier"] + " " + rank["rank"]


		dbCursor.execute(UPDATE_SQL, (id, soloRank, flexRank, puuid))
		
		rankNumber += 1
		with open("GetRankNumber.txt", 'w') as f:
			f.write(str(rankNumber))
		dbConnection.commit()

dbCursor.close()
dbConnection.close()