import json

# Getting the players
playerList = []
with open("Players.txt", 'r') as f:
	f.readline()
	for line in f:
		playerList.append(line.strip())

with open("PlayersNumber.txt", 'r') as f:
	playerNumber = int(f.readline())

with open("GamesSeen.txt", 'r') as f:
	gameNumber = int(f.readline())

with open("MatchData.txt", 'r') as f:
	for i in range(gameNumber):
		f.readline()
	for line in f:
		gameDictionary = json.loads(line.strip())
		for player in gameDictionary["info"]["participants"]:
			if player["puuid"] not in playerList:
				playerList.append(player["puuid"])
		gameNumber += 1
		with open("Players.txt", 'a') as f:
			for player in playerList[int(playerNumber):]:
				f.write("\n")
				f.write(player)
		playerNumber = len(playerList)
		with open("PlayersNumber.txt", 'w') as f:
			f.write(str(len(playerList)))

		with open("GamesSeen.txt", 'w') as f:
			f.write(str(gameNumber))

#writing - to be used only in first iteration
"""
with open("Players.txt", 'w') as f:
	f.write("Player puuids")
	for player in playerList:
		f.write("\n")
		f.write(player)
"""