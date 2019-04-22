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

def createNewNetFile(removingIds):
	f = open('erlangen.net.xml','r')
	f2 = open('erlangenSim.net.xml', 'w')
	removingString = []
	replacingString = []
	for laneId in removingIds:
		removingString.append('id=\"%s\" '%(laneId))
		replacingString.append('id=\"%s\" disallow=\"all\" '%(laneId))
	for line in f:
	    for check, rep in zip(removingString, replacingString):
		line = line.replace(check, rep)
	    f2.write(line)
	f.close()
	f2.close()
def getCenterCoord(shape):
	if len(shape)>=3:
		return shape[len(shape)/2]
	else:
		return ((shape[0][0]+shape[1][0])/2,(shape[0][1]+shape[1][1])/2)
def adjustEdges(edges):
	blockEdges = []
	for edge in edges:
		
		coord = getCenterCoord(edge.getShape())
		print(len(net.getNeighboringEdges(coord[0],coord[1],5)))
		for neighborEdge,dist in net.getNeighboringEdges(coord[0],coord[1],18):
			if neighborEdge not in blockEdges:
				blockEdges.append(neighborEdge)	
	return blockEdges
def availableLane(coordList,shape, stepLength):
	if sumolib.geomhelper.distance(coordList[0],shape[0]) > sumolib.geomhelper.distance(coordList[-1],shape[0]):
		coordList.reverse()
	#if sumolib.geomhelper.distance(coordList[0],shape[0]) > stepLength or sumolib.geomhelper.distance(coordList[-1],shape[-1]) > stepLength:
		#print ("start %i, ende %i"%(sumolib.geomhelper.distance(coordList[0],shape[0]),sumolib.geomhelper.distance(coordList[-1],shape[-1])))		
	#	return False
	for i in range(1,len(coordList)):
		if sumolib.geomhelper.distance(coordList[i-1],coordList[i]) >stepLength:
			problemCoords.append([(coordList[i-1][0]+coordList[i][0])/2 ,(coordList[i-1][1]+coordList[i][1])/2])
			return False
	return True

net = sumolib.net.readNet('erlangen.net.xml')
path = "Erlangen/workingCoordinates"
carsList = os.listdir(path)
checkedEdges = []
blockedEdges = []
allEdges = net.getEdges()
problemCoords = []
for carFile in carsList:
	f = open('Erlangen/workingCoordinates/'+carFile,'r')
	#print(carFile)
	coordList = []
	for line in f:
		coords = line.split(",")
		coordList.append([float(coords[0]),float(coords[1].replace("\n",""))])

	lane = net.getNeighboringLanes(coordList[0][0],coordList[0][1])[0]
	if not availableLane(coordList,lane[0].getShape(True),80):
		if lane[0].getEdge() not in blockedEdges:
			blockedEdges.append(lane[0].getEdge())
	checkedEdges.append(lane[0].getEdge().getID())
	f.close()

removingLaneIds = []
#print(blockedEdges)
blockedEdges = adjustEdges(blockedEdges)
#print(blockedEdges)
for edge in blockedEdges:
	for lane in edge.getLanes():
		if lane.getID() not in removingLaneIds:
			removingLaneIds.append(lane.getID())
	
createNewNetFile(removingLaneIds)


print(len(checkedEdges))
print(len(removingLaneIds))
print(len(allEdges))

		



