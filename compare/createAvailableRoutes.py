import os, sys
if 'SUMO_HOME' in os.environ:
     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
     sys.path.append(tools)
else:   
     sys.exit("please declare environment variable 'SUMO_HOME'")


import sumolib
import mysql.connector
import math	
import re

class ENodeB:
	def __init__(self, id, x, y, xSumo, ySumo,nodeRange, closestIds):
	    self.id = id
	    self.x = x
	    self.y = y
	    self.xSumo = xSumo
	    self.ySumo = ySumo
	    self.nodeRange = nodeRange
	    self.closestIds = closestIds
	
	def addCloseNodeId(self, ids):
	    self.closestIds = ids

def checkLane(xSumo,ySumo,nodeRange,shape):
	available = True
	for point in shape:
		available = available and (sumolib.geomhelper.distance(point,[xSumo,ySumo]) < nodeRange)
	return available

def removeAFromListB(listA,listB):
	for i in range(0,len(shape)):
		if i < (len(shape)-1):
			print(sumolib.geomhelper.distance(shape[i],shape[i+1]))
def getLaneIdsList(lanesWithDistance):
	laneIds = []
	for lane in lanesWithDistance:
		laneIds.append(lane[0].getID())
	return laneIds
def createNewNetFile(laneIds,removingIds):
	f = open('testEdit.net.xml','r')
	f2 = open('mathematicalAvailable.net.xml', 'w')
	removingString = []
	replacingString = []
	for laneId in removingIds:
		removingString.append('id=\"%s\" '%(laneId))
		replacingString.append('id=\"%s\" disallow=\"custom1\" '%(laneId))
	for line in f:
	    for check, rep in zip(removingString, replacingString):
		line = line.replace(check, rep)
	    f2.write(line)

def checkIfAllEdgesUsed():
	checkedEdges = []
	f = open('trip.rou.xml','r')
	for line in f:
		result = re.search('<route edges=\"(.*?)\"\/>',line)
		if result != None:
			edges = result.group(1).split()
			for edge in edges:
				if edge not in checkedEdges:
					checkedEdges.append(edge)		
	f.close()
	allEdges = []
	for edge in net.getEdges():
		allEdges.append(edge.getID())
	#print("Num Of Edges:%s\n"%(len(allEdges)))
	#print("Num Of CheckedEdges:%s\n"%(len(checkedEdges)))
	return [x for x in allEdges if x not in checkedEdges] == []



	
net = sumolib.net.readNet('erlangen.net.xml')
xmin,ymin,xmax,ymax = net.getBoundary()
lonmin, latmin = net.convertXY2LonLat(xmin, ymin)
lonmax, latmax = net.convertXY2LonLat(xmax, ymax)

db = mysql.connector.connect(
  host="localhost",
  user="newuser",
  passwd="password",
  db="Thesis"
)

cur = db.cursor()

# SELECT CELLS TO CHANGE
#cur.execute("SELECT * FROM OpenCell WHERE lon BETWEEN 10.998228 and 11.035606 And lat between 49.560940 and 49.587550 LIMIT 0,104;"
cur.execute("SELECT * FROM OpenCell WHERE lon BETWEEN %f and %f And lat between %f and %f LIMIT 0,70;"% (lonmin, lonmax, latmin, latmax))


counter = 1
margin= 25
allENodeBs = []
availableLanesList = []

for row in cur.fetchall():
	xSumo = row[15]
	ySumo = row[16]
	x = xSumo - xmin + margin
	y = (ymax - ymin) - (ySumo - ymin) + margin
	nodeRange = row[9]
	allENodeBs.append(ENodeB(counter,x,y,xSumo,ySumo,nodeRange,[]))
	testingLanes = net.getNeighboringLanes(xSumo,ySumo,500)
	for lane in testingLanes:
		#test(lane[0].getShape())
		#if lane[0].getID() not in availableLanesList:
			#availableLanesList.append(lane[0].getID())
		if checkLane(xSumo,ySumo,500,lane[0].getShape()):
			if lane[0].getID() not in availableLanesList:
				availableLanesList.append(lane[0].getID())
	counter = counter + 1

laneIds = getLaneIdsList(net.getNeighboringLanes(((xmin+xmax)/2),((ymin+ymax)/2),20000))
removingIds = [x for x in laneIds if x not in availableLanesList] 
createNewNetFile(laneIds,removingIds)



#print(checkIfAllEdgesUsed()) 	





print(len(availableLanesList))
print(len(laneIds))
#print(removingIds)
#for lane in lanes:
#	print(lane[0].getID())












#f= open("enodes.txt","w+")
#f.write(submodules+connections+ini+x2AppsPerNode+x2Clients)
#f.close()

