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
	
net = sumolib.net.readNet('erlangen.net.xml')
xmin,ymin,xmax,ymax = net.getBoundary()
lonmin, latmin = net.convertXY2LonLat(xmin, ymin)
lonmax, latmax = net.convertXY2LonLat(xmax, ymax)

routes = '<?xml version="1.0" encoding="UTF-8"?>\n<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n'
counter = 0
f = open('everyRoute.net.xml','w')
for edge in net.getEdges():
	routes = routes + '    <vehicle id="%i" depart="0.00" departSpeed="max">\n'% counter
	routes = routes + '        <route edges="'+edge.getID()+'"/>\n    </vehicle>\n'
	counter = counter + 1
routes = routes + '</routes>'
f.write(routes)
f.close()
	

