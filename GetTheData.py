import requests
import time
import os
import json

import io
import gzip
import json
import boto3

def upload_json_gz(s3client, bucket, key, obj, default=None, encoding='utf-8'):
    ''' upload python dict into s3 bucket with gzip archive '''
    inmem = io.BytesIO()
    with gzip.GzipFile(fileobj=inmem, mode='wb') as fh:
        with io.TextIOWrapper(fh, encoding=encoding) as wrapper:
            wrapper.write(json.dumps(obj, ensure_ascii=False, default=default))
    inmem.seek(0)
    s3client.put_object(Bucket=bucket, Body=inmem, Key=key)


# Getting the token

SLEEP_503 = 120
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

BUCKET_NAME = ''
S3_CLIENT = boto3.client('s3')

for match in matchIDs:
	time.sleep(sleepTime)
	print("Downloading match " + match)
	
	matchURL = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match}"
	r1 = requests.get(matchURL, headers = head)

	if r1.status_code != 200:
		print("Request failed, status code: " + str(r1.status_code))
		if r1.status_code == 404:
			print("Error 404 - skipping the match")
			continue
		elif r1.status_code == 503:
			print("Error 503 - service unavailable. Sleeping " + str(SLEEP_503) + " seconds")
			time.sleep(SLEEP_503)
			continue
		elif r1.status_code == 429:
				sleep_429 = int(r1.headers["Retry-After"]) + 1
				print("Error 429 - Rate Limit Exceeded. Sleeping " + str(sleep_429) + " seconds")
				time.sleep(sleep_429)
				r1 = requests.get(matchURL, headers = head)
				if r1.status_code != 200:
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
