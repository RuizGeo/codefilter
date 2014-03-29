# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
import time
#-------PostGIS--------#
import psycopg2
try:
    connection = psycopg2.connect("dbname= 'bd_pointscloud' user='postgres' host='localhost' password='mdt'")
except:
    print "I am unable to connect to the database"

cursor = connection.cursor()
#-----------------------#
layer = iface.activeLayer()
provider = layer.dataProvider()
spIndex = QgsSpatialIndex() #create spatial index object
#Percorrer as geometrias
iter = layer.getFeatures()
iniIter = time.time()
for feature in iter:
    #Calcula a media para os IDs selecionados
    cursor.execute("SELECT tan(AVG(p1.z)/AVG(ST_Distance(p.geom, p1.geom))) FROM point_cloud AS p, point_cloud AS p1 WHERE ST_DWithin(p1.geom,p.geom, 2.0) AND ST_Distance(p.geom, p1.geom) != 0 AND p.gid = %s" %feature.id())
    
print [i for i in cursor]
fimIter = time.time()
print 'Tempo iter: ',(fimIter - iniIter) , ' segundos'
