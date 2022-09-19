from ast import While
import requests
import time
import os
import json

import io
import gzip
import json
import boto3

def upload_jsonl_gz(s3client, bucket, key, objs, default=None, encoding='utf-8'):
	''' upload python dict into s3 bucket with gzip archive '''
	inmem = io.BytesIO()
	with gzip.GzipFile(fileobj=inmem, mode='wb') as fh:
		with io.TextIOWrapper(fh, encoding=encoding) as wrapper:
			for obj in objs:
				wrapper.write(json.dumps(obj, ensure_ascii=False, default=default)+'\n')
	inmem.seek(0)
	s3client.put_object(Bucket=bucket, Body=inmem, Key=key)


# Getting the token

SLEEP_503 = 120
TOKEN_ENVIRON_NAME = "XRiotToken"
token = ""

if TOKEN_ENVIRON_NAME in os.environ:
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

BUCKET_NAME = 'riot-stats'
S3_CLIENT = boto3.client('s3')

PACK_SIZE = 100
KEY_PREFIX = 'LeagueOfLegends/MatchData/'
packet = 90
gameData = []

for match in matchIDs:
	whatDo = "Nothing"
	time.sleep(sleepTime)
	print("Downloading match " + match)
	
	matchURL = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match}"

	while True:
		r1 = requests.get(matchURL, headers = head)
		if r1.status_code == 200:
			break
		print("Request failed, status code: " + str(r1.status_code))
		if r1.status_code == 404:
			print("Error 404 - skipping the match")
			whatDo = "Continue"
			break
		elif r1.status_code == 503:
			print("Error 503 - service unavailable. Sleeping " + str(SLEEP_503) + " seconds")
			time.sleep(SLEEP_503)
			continue
		elif r1.status_code == 429:
				sleep_429 = int(r1.headers["Retry-After"]) + 1
				print("Error 429 - Rate Limit Exceeded. Sleeping " + str(sleep_429) + " seconds")
				time.sleep(sleep_429)
				continue
		else:
			whatDo = "Break"
			break
	
	if whatDo == "Break":
		break
	if whatDo == "Continue":
		continue
	
	packet += 1
	matchData = r1.json()
	
	gameData.append(matchData)

	if packet == PACK_SIZE:
		packageName = KEY_PREFIX + match + ".jsonl.gz"
		upload_jsonl_gz(S3_CLIENT, BUCKET_NAME, packageName, gameData)
		print("Uploaded data package " + packageName)
		packet = 0
		gameData = []
		matchNumber += PACK_SIZE
		with open("MatchDataNumber.txt", 'w') as f:
			f.write(str(matchNumber))
