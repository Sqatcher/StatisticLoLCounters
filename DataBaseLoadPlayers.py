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

SQL_PLAYERS = "INSERT INTO players VALUES(%s)"

i = 0

with open("LotsOfPlayers.csv", 'r') as f:
	line = f.readline()  # read header
	
	#all or nothing
	for line in f:
		i+=1
		puuid = line[1:len(line)-2]
		dbCursor.execute("SELECT puuid FROM players WHERE puuid='" + puuid + "'")
		res = dbCursor.fetchone()
		if res == None:
			dbCursor.execute(SQL_PLAYERS, (puuid,))
		if i % 1000 == 0:
			print("Loaded " + str(i) + " players") 
			dbConnection.commit()

dbConnection.commit()
dbCursor.close()
dbConnection.close()