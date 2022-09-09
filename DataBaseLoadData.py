import psycopg2
from getpass import getpass
import json
import time

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
SQL_MATCHES = "INSERT INTO matches VALUES(%s, %s, %s, %s)"
SQL_PLAYERS = "INSERT INTO players VALUES(%s)"
SQL_MP      = """INSERT INTO match_player VALUES(%s, %s, %s, %s, %s)"""

COMMIT_NUMBER = 500
i = 0
index = 0
with open("DataBaseMatchNumber.txt", 'r') as f:
	index = int(f.readline().strip())


with open("MatchData.txt", 'r') as f:
	for i in range(index):
		f.readline()
	i = 0
	for line in f:

		if i == COMMIT_NUMBER:
			print("Commiting games from " + str(index) + " to " + str(index + i) + "...", end=" ")
			dbConnection.commit()
			index += i
			
			with open("DataBaseMatchNumber.txt", 'w') as f:
				f.write(str(index))
			print("Success!")
			i = 0

		gameDictionary = json.loads(line.strip())
		i += 1
		matchId = gameDictionary["metadata"]["matchId"]
		gameVersion = gameDictionary["info"]["gameVersion"]
		gameMode = gameDictionary["info"]["gameMode"]
		gameStartTimestamp = str(gameDictionary["info"]["gameStartTimestamp"])

		dbCursor.execute("SELECT matchId FROM matches WHERE matchId='" + matchId + "'")
		res = dbCursor.fetchone()
		if res != None:
			continue

		dbCursor.execute(SQL_MATCHES, (matchId, gameVersion, gameMode, gameStartTimestamp))

		for participant in gameDictionary["info"]["participants"]:
			puuid = participant["puuid"]
			championName = participant["championName"]
			teamPosition = participant["teamPosition"]
			win = participant["win"]
			isBot = False

			if puuid == "BOT":
				puuid = puuid + "-" + matchId + "-" + championName
				isBot = True

			#check if player already exists
			dbCursor.execute("SELECT puuid FROM players WHERE puuid='" + puuid + "'")
			res = dbCursor.fetchone()
			if res == None:
				dbCursor.execute(SQL_PLAYERS, (puuid,))
			else:
				if isBot:
					puuid = puuid + "-1"
					dbCursor.execute(SQL_PLAYERS, (puuid,))

			dbCursor.execute(SQL_MP, (matchId, puuid, championName, teamPosition, win))


print("Commiting games from " + str(index) + " to " + str(index + i) + "...", end=" ")
dbConnection.commit()
index += i
with open("DataBaseMatchNumber.txt", 'w') as f:
	f.write(str(index))
print("Success!")

dbCursor.close()
dbConnection.close()