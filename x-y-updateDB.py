import os, sys
if 'SUMO_HOME' in os.environ:
     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
     sys.path.append(tools)
else:   
     sys.exit("please declare environment variable 'SUMO_HOME'")


import sumolib
import mysql.connector

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
cur.execute("SELECT * FROM OpenCell WHERE lon BETWEEN %f and %f And lat between %f and %f LIMIT 0,104;"% (lonmin, lonmax, latmin, latmax))

# UPDATE SELECTED CELLS
for row in cur.fetchall():
	x, y = net.convertLonLat2XY(row[7], row[8])
	sql = "UPDATE OpenCell SET x = '%s',y = '%s' WHERE id = %s"
	val = (x, y, row[0])
	cur.execute(sql, val)

db.commit()
