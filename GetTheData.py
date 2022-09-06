import requests
import time
import os
import json

# Getting the token

TOKEN_ENVIRON_NAME = "X-Riot-Token"
token = ""

if "X-Riot-Token" in os.environ:
	token = os.environ[TOKEN_ENVIRON_NAME]
else:
	print("No Riot token available")
	exit()

# Getting the matches
with open("MatchDataNumber.txt", 'r') as f:
	matchNumber = int(f.readline())

matchIDs = []
with open("MatchIds.txt", 'r') as f:
	f.readline()
	for i in range(matchNumber):   # skip matches that are already downloaded
		f.readline()
	for line in f:
		matchIDs.append(line.strip())


sleepTime = 120/100 + 0.1         # 100 every 2 minutes is max
head = {"X-Riot-Token": token}

for match in matchIDs:
	print("Downloading match " + match)
	
	matchURL = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match}"
	r1 = requests.get(matchURL, headers = head)

	if r1.status_code != 200:
		print("Request failed, status code: " + str(r1.status_code))
		if r1.status_code == 404:
			print("Error 404 - skipping the match")
			continue
		else:
			break
	matchData = r1.json()
	
	with open("MatchData.txt", 'a') as f:
		json.dump(matchData, f)
		f.write("\n")

	matchNumber += 1
	with open("MatchDataNumber.txt", 'w') as f:
		f.write(str(matchNumber))

	time.sleep(sleepTime)
