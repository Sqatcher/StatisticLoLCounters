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

commands = (
"""
CREATE TABLE matches (
	matchId varchar(50) NOT NULL PRIMARY KEY,
	gameVersion varchar(50) NOT NULL,
	gameMode varchar(50) NOT NULL,
	gameStartTimestamp varchar(50) NOT NULL
)
""",
"""
CREATE TABLE players (
	puuid varchar(100) NOT NULL PRIMARY KEY,
	id varchar(100),
	soloRank varchar(50),
	flexRank varchar(50)
)
""",
"""
CREATE TABLE match_player (
	matchId varchar(50) NOT NULL,
	puuid varchar(100) NOT NULL,
	championName varchar(50) NOT NULL,
	teamPosition varchar(50) NOT NULL,
	win boolean NOT NULL,
	PRIMARY KEY(matchId, puuid),
	CONSTRAINT fk_matchId FOREIGN KEY(matchId) REFERENCES matches(matchId),
	CONSTRAINT fk_puuid FOREIGN KEY(puuid) REFERENCES players(puuid)
)
""")

for command in commands:
	dbCursor.execute(command)

dbCursor.close()
dbConnection.commit()
dbConnection.close()