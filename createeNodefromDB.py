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


class ENodeB:
	def __init__(self, id, x, y, closestIds):
	    self.id = id
	    self.x = x
	    self.y = y
	    self.closestIds = closestIds
	
	def addCloseNodeId(self, ids):
	    self.closestIds = ids

def myMaxDistance(eNodeBIdsWithDist):
	distValue = eNodeBIdsWithDist[0][1]
	listLocation = 0
	for i in range(1,len(eNodeBIdsWithDist)):
		if eNodeBIdsWithDist[i][1] > distValue:
			distValue = eNodeBIdsWithDist[i][1]
			listLocation = i
	return listLocation,distValue	

def getDistance(x1,y1,x2,y2):
	return math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )

def getClosestENodeBs(radius,minNumOfENodeBs,node, allENodeBs):
	
	closestENodeBIdsWithDist = []
	eNodeBIds = []
	#for i in range(0,numOfEnodeBs):
	
	for aNode in allENodeBs:
		if aNode.id != node.id:
			#first eNodeBs directly in List
			if len(closestENodeBIdsWithDist) < minNumOfENodeBs:
				#print("nodeId %d, aNodeId %d"%(len(eNodeBIds),numOfENodeBs))
				#print("len(eNodeBIds) %d, numOfENodeBs %d\n"%(len(eNodeBIds),numOfENodeBs))
				closestENodeBIdsWithDist.append([aNode.id,getDistance(aNode.x,aNode.y,node.x, node.y)])
			#check if distance of new eNodeB is smaller than the ones in the list 
			elif getDistance(aNode.x,aNode.y,node.x, node.y)< myMaxDistance(closestENodeBIdsWithDist)[1]:
					#replace biggest entry with new Node
					closestENodeBIdsWithDist.pop(myMaxDistance(closestENodeBIdsWithDist)[0])
					closestENodeBIdsWithDist.append([aNode.id,getDistance(aNode.x,aNode.y,node.x, node.y)])
	for aNode in allENodeBs:
		if aNode.id != node.id:
			if getDistance(aNode.x,aNode.y,node.x, node.y)< radius and [aNode.id,getDistance(aNode.x,aNode.y,node.x, node.y)] not in closestENodeBIdsWithDist:
					#addNodes which are inside the radius
					closestENodeBIdsWithDist.append([aNode.id,getDistance(aNode.x,aNode.y,node.x, node.y)])
	
	for elem in closestENodeBIdsWithDist:
		eNodeBIds.append(elem[0])
	return eNodeBIds


def getX2PairsList(allENodeBs):
	pairsList = []
	for node in allENodeBs:
		node.addCloseNodeId(getClosestENodeBs(500,3,node,allENodeBs))
		for closestNodeId in node.closestIds:
			if ([node.id,closestNodeId] not in pairsList) and ([closestNodeId,node.id] not in pairsList):
				pairsList.append([node.id,closestNodeId])
	return pairsList

def getX2PairsListFromFile(filename):
	pairsList = []
	f = open(filename,'r')
	for line in f:
		result = re.search('eNodeB([0-9]+).*eNodeB([0-9]+)',line)
		if result != None and [int(result.group(1)),int(result.group(2))] not in pairsList:
			 pairsList.append([int(result.group(1)),int(result.group(2))])
	f.close()
	return pairsList



def getX2Dict(pairsList):
	x2Dict ={}
	for pair in pairsList:
		if pair[0] not in x2Dict:
			x2Dict[pair[0]] = [pair[1]]
		elif pair[1] not in x2Dict[pair[0]]:
			x2Dict[pair[0]].append(pair[1])

		if pair[1] not in x2Dict:
			x2Dict[pair[1]] = [pair[0]]
		elif pair[0] not in x2Dict[pair[1]]:
			x2Dict[pair[1]].append(pair[0])
	return x2Dict

def getNumX2AppsPerNode(x2Dict):
	x2AppsPerNode = "\n#x2AppsPerNode\n"
	for k, v in x2Dict.items():
		x2AppsPerNode = x2AppsPerNode + "*.eNodeB%d.numX2Apps = %d\n"%(k,len(v))
	return x2AppsPerNode

def getX2Clients(x2Dict):
	x2Clients = "\n#X2 Clients\n"
	for serverNode, clientNodes in x2Dict.items():
		length = len(clientNodes)
		i = 0
		while i<length:
			j = 0
			while "eNodeB%d%%x2ppp%d"%(clientNodes[i],j) in x2Clients:
				j = j + 1
			x2Clients = x2Clients + "*.eNodeB%d.x2App[%d].client.connectAddress = \"eNodeB%d%%x2ppp%d\"\n"%(serverNode,i,clientNodes[i],j)
		#*.eNodeB1.x2App[0].client.connectAddress = "eNodeB2%x2ppp0" 
			i=i+1

	return x2Clients
	

			
	

net = sumolib.net.readNet('erlangen.net.xml')
xmin,ymin,xmax,ymax = net.getBoundary()
lonmin, latmin = net.convertXY2LonLat(xmin, ymin)
lonmax, latmax = net.convertXY2LonLat(xmax, ymax)
lonmax = lonmax-0.002

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


submodules = "submodules:\n"
connections = "\nconnections:\n"
counter = 1
margin= 25
allENodeBs = []
pois ="\n\n#POIs/Enodes\n"
ini = "\n# Enable handover\n**.enableHandover = true\n**.broadcastMessageInterval = 0.5s\n# X2 and SCTP configuration\n"
# UPDATE SELECTED CELLS
for row in cur.fetchall():
	xSumo = row[15]
	ySumo = row[16]
	x = row[15] - xmin + margin
	y = (ymax - ymin) - (row[16] - ymin) + margin
	allENodeBs.append(ENodeB(counter,x,y,[]))
	submodules = submodules+"\t eNodeB%d: eNodeB {\n\t\t@display(\"p=%f,%f;r=500,green,green,1\");\n\t}\n"% (counter, x, y)
	connections = connections +("\tpgw.pppg++ <--> Eth100G { @display(\"ls=black,0,d\"); } <--> eNodeB%d.ppp;\n"% counter)
	ini = ini+"**.eNodeB%d.macCellId = %d\n**.eNodeB%d.macNodeId = %d\n"%(counter,counter,counter,counter)
	pois = pois + "<poly id=\"9999999999999%d\" type=\"eNodeB\" color=\"0.00,0.50,0.00\" fill=\"1\" layer=\"5\" shape=\"%8.2f,%8.2f %8.2f,%8.2f %8.2f,%8.2f %8.2f,%8.2f %8.2f,%8.2f\"/>\n"%(counter,xSumo,ySumo,xSumo,ySumo+20,xSumo+20,ySumo+20,xSumo+20,ySumo,xSumo,ySumo)
	counter = counter + 1
#add x2 connections 
ini = ini + "**.eNodeBCount = %d\n"%(len(allENodeBs))

if os.path.isfile("manualEnodeX2Connections.txt"):
	#pairsList = getX2PairsListFromFile("manualEnodeX2Connections.txt")
	print("Take Connections from File")
	pairsList =getX2PairsListFromFile("manualEnodeX2Connections.txt")
else:
	pairsList = getX2PairsList(allENodeBs)

connections = connections + ("\n\t//# X2 connections \n")

for pair in pairsList:
	connections = connections + "\teNodeB%d.x2++ <--> Eth100G { @display(\"ls=grey25,1,d\"); }<--> eNodeB%d.x2++; \n"% (pair[0],pair[1])

#print(pairsList)	
x2Dict = getX2Dict(pairsList)
#print(x2Dict)

x2AppsPerNode = getNumX2AppsPerNode(x2Dict)

x2Clients = getX2Clients(x2Dict)

#print(x2Clients)
#for key, value in x2Dict:
#	print("id")
#print(x2Dict)	

	
#for i in range(1,counter-1):
#	for j in range (i+1,counter):
#		connections = connections + "\teNodeB%d.x2++ <--> Eth10G <--> eNodeB%d.x2++; \n"% (i,j)

connections = connections 
f= open("enodes.txt","w+")
f.write(submodules+connections+ini+x2AppsPerNode+x2Clients+pois)
f.close()


# Enable handover
#**.enableHandover = true
#**.broadcastMessageInterval = 0.5s

# X2 and SCTP configuration
#*.eNodeB*.numX2Apps = 1    # one x2App per peering eNodeB
#*.eNodeB*.x2App[*].server.localPort = 5000 + ancestorIndex(1) # Server ports (x2App[0]=5000, x2App[1]=5001, ...)
#*.eNodeB1.x2App[0].client.connectAddress = "eNodeB2%x2ppp0" 
#*.eNodeB2.x2App[0].client.connectAddress = "eNodeB1%x2ppp0" 
#**.sctp.nagleEnabled = false         # if true, transmission of small packets will be delayed on the X2
#**.sctp.enableHeartbeats = false

#*.eNodeB1.x2App[0].client.connectAddress = "eNodeB2%x2ppp0" 
#*.eNodeB1.x2App[1].client.connectAddress = "eNodeB3%x2ppp0"
#*.eNodeB2.x2App[0].client.connectAddress = "eNodeB1%x2ppp0" 
#*.eNodeB2.x2App[1].client.connectAddress = "eNodeB3%x2ppp1"
#*.eNodeB3.x2App[0].client.connectAddress = "eNodeB1%x2ppp1" 
#*.eNodeB3.x2App[1].client.connectAddress = "eNodeB2%x2ppp1"

