import csv
import json

finalJson = {"name": "champions", "children": []}
championNameIntoIndex = {}
positionIntoIndex = {"TOP": 0, "JUNGLE": 1, "MIDDLE": 2, "BOTTOM": 3, "UTILITY" : 4}

with open("ChampionNames.csv", newline='') as f:
	content = csv.reader(f, delimiter=',', quotechar='"')
	i=0
	for line in content:
		championname = line[0]
		championD = {"name": championname, "children":[
			{"name": "TOP", "value":0},
			{"name": "JUNGLE", "value":0},
			{"name": "MIDDLE", "value":0},
			{"name": "BOTTOM", "value":0},
			{"name": "UTILITY", "value":0}
		]}
		finalJson["children"].append(championD)
		championNameIntoIndex[championname] = i
		i+=1


with open('FinalData.csv', newline='') as f:
	content = csv.reader(f, delimiter = ',', quotechar='"')
	#matchid;gameversion;championname;teamposition;win
	next(content)
	for line in content:
		championname = line[2]
		position = line[3]
		index = championNameIntoIndex[championname]
		if position == '':
			continue
		posIndex = positionIntoIndex[position]
		finalJson["children"][index]["children"][posIndex]["value"]+=1

with open('champions.json', 'w') as f:
	json.dump(finalJson, f)