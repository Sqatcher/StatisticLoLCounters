import boto3


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

PACKET_SIZE = 100
i = 0
sqs = boto3.client('sqs')
MATCH_ID_URL = 'https://sqs.eu-west-1.amazonaws.com/765941628235/MatchIdQueue'



while len(matchIDs) > 0:
	matchPacket = '\n'.join(matchIDs[0:PACKET_SIZE])
	matchIDs = matchIDs[PACKET_SIZE:]

	response = sqs.send_message(QueueUrl = MATCH_ID_URL, MessageBody=matchPacket)
	
	matchNumber += len(matchPacket)
	with open("MatchDataNumber.txt", 'w') as f:
		f.write(str(matchNumber))
