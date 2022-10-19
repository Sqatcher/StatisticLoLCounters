import json
import boto3
import requests
import gzip
import io
import time

def lambda_handler(event, context):
    sqs = boto3.client('sqs')
    SQS_TOKEN_URL = 'https://sqs.eu-west-1.amazonaws.com/765941628235/RiotXTokenQueue'
    
    response = sqs.receive_message(QueueUrl = SQS_TOKEN_URL)
    
    if 'Messages' not in response:
        return {'statusCode': 200, 'body': json.dumps('No token available')}
    
    token = response['Messages'][0]['Body']
    
    MATCH_ID_URL = 'https://sqs.eu-west-1.amazonaws.com/765941628235/MatchIdQueue'
    sleepTime = 100/120+0.1
    head = {"X-Riot-Token": token}
    SLEEP_503 = 120
    BUCKET_NAME = 'riot-stats'
    S3_CLIENT = boto3.client('s3')
    
    PACK_SIZE = 100
    KEY_PREFIX = 'LeagueOfLegends/MatchData/'
    gameData = []
    
    while True:
        response_match = sqs.receive_message(QueueUrl = MATCH_ID_URL)
        if 'Messages' not in response:
            return {'statusCode': 200, 'body': json.dumps('No match available')}
        match_handle = response_match['Messages'][0]['ReceiptHandle']
        match_pack = response['Messages'][0]['Body'].split('\n')
        print(match_pack)
        return {'statusCode': 200, 'body': json.dumps('Training complete.')}
        for match in match_pack:
            whatDo = "Nothing"
            time.sleep(sleepTime)
            #print("Downloading match " + match)
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
            
            gameData.append(r1.json())
            
        packageName = KEY_PREFIX + match_pack[0] + ".jsonl.gz"
        upload_jsonl_gz(S3_CLIENT, BUCKET_NAME, packageName, gameData)
        print("Uploaded data package " + packageName)
        sqs.delete_message(QueueUrl = MATCH_ID_URL, ReceiptHandle = match_handle)
        gameData = []
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


