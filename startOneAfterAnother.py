import os, sys
if 'SUMO_HOME' in os.environ:
     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
     sys.path.append(tools)
else:   
     sys.exit("please declare environment variable 'SUMO_HOME'")


import sumolib
import mysql.connector
import math
import os.path
import re

def getDuration(carId):
	outputFile = open('output3.xml', 'r')
	for line in outputFile:
		if 'id="'+carId+'"' in line:
			result = re.search('duration=\"([0-9.]+)\"',line)
			outputFile.close()
			return float(result.group(1))
	outputFile.close()
	return None

f = open('trip.rou.xml','r')
f3 = open('startOneAfterTrip.rou.xml','w')

nextStart = 0.0
lastId = 400
for line in f:
	result = re.search('id=\"([0-9]+)\"',line)
	
	if result != None:
		if int(result.group(1)) != lastId +1:
			lastId = lastId + 1
			print(lastId)
		lastId = lastId +1 
		duration = getDuration(result.group(1))
		if duration != None:
			departResult = re.search('depart=\"([0-9.]+)\"',line)
			newDepart = 'depart="%.2f"' % nextStart
			newLine = line.replace(departResult.group(0),newDepart)
			nextStart = duration + nextStart-0.05

	else:
		newLine = line
	
	f3.write(newLine)

f.close()

f3.close()
