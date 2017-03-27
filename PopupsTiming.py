import sys 
import csv 
import math

import pandas as pd

if len(sys.argv) != 3:
	print "Usage: python [python-script] [eye-data-csv-file] [game-data-csv-file]"
	sys.exit(1)

eyeDataPath = sys.argv[1]
gameDataPath = sys.argv[2]
eyeData=[]
gameData=[]

popupPositions=dict()
popupPositions["currentSpeed"] = [1599,1400]
popupPositions["speed"] = [950,1350]
popupPositions["current"] = [875,1400]
popupPositions["tire"] = [1035,1292.5]
popupPositions["compass"] = [1084,1274]
popupPositions["navigation"] = [1034,1324]

with open(eyeDataPath, 'rb') as f:
	csvreader = csv.reader(f, delimiter=',')

	for row in csvreader:
		if len(row) == 4: 
			eyeData.append(row)

with open(gameDataPath, 'rb') as f:
	csvreader = csv.reader(f, delimiter=',')
	for row in csvreader:
		row[1] = row[1].strip()
		gameData.append(row)
		#print gameData

for i in range(0, len(gameData) -2):
	if gameData[i][1] == gameData[i+2][1] and gameData[i][1] != "": 
		gameData[i+1][1] = gameData[i][1]

gameDataFinal=dict()
emptyCount = 0
popupCount = 0
label = ""

currentTime = -1

for row in gameData:
	if row[1] != "":
		label = row[1]
	if row[0] != currentTime: 
		if popupCount > emptyCount:
			gameDataFinal[currentTime] = label
		else:
			gameDataFinal[currentTime] = ""	
		emptyCount = 0
		popupCount = 0
		currentTime = row[0]

	if row[1] == "":
		emptyCount += 1	
	else:
		popupCount += 1	

if popupCount > emptyCount:
	gameDataFinal[currentTime] = label

else:
	gameDataFinal[currentTime] = ""		

del gameDataFinal[-1]


finalData=[]

for row in eyeData:
	time = row[3].strip()
	if time in gameDataFinal:
		label = gameDataFinal[time]
		row.append(label)
		
		if label != "" and label != "all":
			diffX = abs(float(row[0]) - popupPositions[label][0])
			diffY = abs(float(row[1]) - popupPositions[label][1])
			diffX = math.pow(diffX,2)
			diffY = math.pow(diffY,2)
			row.append(math.sqrt(diffX + diffY))
		else:
			row.append(-1)
		finalData.append(row)	
		#print finalData		
	
#getting rid of unnecessary columns
for row in finalData:
	del row[0]
	del row[0]
	del row[0]
	#only do this if don't want actual x, y values
	#print finalData
		
outputFile = open('OutputCSVForAnalysis/DataParticipant5Draft2.csv', "wb")
writer = csv.writer(outputFile)
for row in finalData:	
	writer.writerow(row)	
outputFile.close()

navigation = [row for row in finalData if 'navigation' == row[1]]
currentStreet = [row for row in finalData if 'current' == row[1]]
lowTire = [row for row in finalData if 'tire' == row[1]]
compass = [row for row in finalData if 'compass' == row[1]]
speedLimit = [row for row in finalData if 'speed' == row[1]]


for row in navigation:
 	del row[1]	

for row in currentStreet: 	
	del row[1]

for row in lowTire:
 	del row[1]
	
for row in compass:
 	del row[1]

for row in speedLimit:
	del row[1]			

#--------NAVIGATION -----------
from collections import defaultdict
dicNav = defaultdict(list)
for item in navigation:
 	key = "/".join(item[:-1])
	dicNav[key].append(item[-1])	
print dicNav
#so dicNav= 'time': [distance1, distance2, distance3,...]

#--------CURRENT STREET --------
from collections import defaultdict
dicStreet = defaultdict(list)
for item in currentStreet:
 	key = "/".join(item[:-1])
	dicStreet[key].append(item[-1])	
print dicStreet

#--------LOW TIRE ------------
from collections import defaultdict
dicTire = defaultdict(list)
for item in lowTire:
 	key = "/".join(item[:-1])
	dicTire[key].append(item[-1])	
print dicTire

#-------COMPASS --------------
from collections import defaultdict
dicCompass = defaultdict(list)
for item in compass:
 	key = "/".join(item[:-1])
	dicCompass[key].append(item[-1])	
print dicCompass

#------SPEED LIMIT ------
from collections import defaultdict
dicLimit = defaultdict(list)
for item in speedLimit:
 	key = "/".join(item[:-1])
	dicLimit[key].append(item[-1])	
print dicLimit

#to print everything from console to a file 
f = open("OutputCSVForAnalysis/DataParticipant5Final2.csv", 'w')
sys.stdout = f

print "NAVIGATION:"
valueListNav = []
for key,val in dicNav.items():
 	valueListNav = []
 	average = reduce(lambda x, y: x + y, val) / len(val)
 	valueListNav.append(average)
	
	print valueListNav

print "-------------"

print "CURRENT STREET:"
valueListStreet = []
for key,val in dicStreet.items():
 	valueListStreet = []
 	average = reduce(lambda x, y: x + y, val) / len(val)
 	valueListStreet.append(average)
	
	print valueListStreet

print "-----------"


print "LOW TIRE PRESSURE:"
valueListTire = []
for key,val in dicTire.items():
 	valueListTire = []
 	average = reduce(lambda x, y: x + y, val) / len(val)
 	valueListTire.append(average)
	
	print valueListTire

print "-----------"

print "COMPASS:"
valueListCompass = []
for key,val in dicTire.items():
 	valueListCompass = []
 	average = reduce(lambda x, y: x + y, val) / len(val)
 	valueListCompass.append(average)
	
	print valueListCompass

print "----------"

print "SPEED LIMIT:"
valueListLimit = []
for key,val in dicLimit.items():
 	valueListLimit = []
 	average = reduce(lambda x, y: x + y, val) / len(val)
 	valueListLimit.append(average)
	
	print valueListLimit	

f.close()

#/Users/cclapp/Dropbox/4th/CS4099/CSVEyeData/CorrectCSVEyeParticipant1.csv
#/Users/cclapp/Dropbox/4th/CS4099/CSVParticipantGameOutput/CSVGameParticipant1.csv