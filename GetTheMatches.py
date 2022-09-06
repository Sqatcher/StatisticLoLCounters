import requests
import time
import os
from collections import OrderedDict

# Getting the token

TOKEN_ENVIRON_NAME = "X-Riot-Token"
token = ""

if "X-Riot-Token" in os.environ:
	token = os.environ[TOKEN_ENVIRON_NAME]
else:
	print("No Riot token available")
	exit()

# Getting the matches
matchList = []
with open("MatchIds.txt", 'r') as f:
	f.readline()
	for line in f:
		matchList.append(line.strip())

with open("MatchIdsPosition.txt", 'r') as f:
	startPoint = int(f.readline())

with open("PlayersSeen.txt", 'r') as f:
	playersSeen = int(f.readline())

puuids = []
with open("Players.txt", 'r') as f:
	f.readline()
	for i in range(playersSeen):
		f.readline()
	for line in f:
		puuids.append(line.strip())

count = 100
sleepTime = 120/100 + 0.1         # 100 every 2 minutes is max
head = {"X-Riot-Token": token}

for puuid in puuids:
	start = 0
	print("Downloading matches for player " + puuid + "\n")
	while(True):
		puuidURL = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
		r1 = requests.get(puuidURL, headers = head)

		if r1.status_code != 200:
			print("Request failed, status code: " + str(r1.status_code))
			break
		matchIDs = r1.json()
		if matchIDs == []:
			break
		for match in matchIDs:
			matchList.append(match)
		matchList = list(OrderedDict.fromkeys(matchList))
		start += count
		time.sleep(sleepTime)

	if r1.status_code != 200:
		break

	playersSeen += 1
	with open("MatchIds.txt", 'a') as f:
		for matchID in matchList[int(startPoint):]:
			f.write("\n")
			f.write(matchID)
	startPoint = len(matchList)

	with open("PlayersSeen.txt", 'w') as f:
		f.write(str(playersSeen))
		
	with open("MatchIdsPosition.txt", 'w') as f:
		f.write(str(startPoint))

#writing - to be used only in first iteration
"""
with open("MatchIds.txt", 'w') as f:
	f.write(str(len(matchList)))
	for matchID in matchList:
		f.write("\n")
		f.write(matchID)
"""