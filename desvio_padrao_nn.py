from osgeo import ogr
from PyQt4.QtCore import *
import time
import sys

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
fit = provider.getFeatures() #gets all features in layer
# insert features to index
feat = QgsFeature()
while fit.nextFeature(feat):
    spIndex.insertFeature(feat)
#Percorrer as geometrias
iter = layer.getFeatures()
iniGeom = time.time()
for feature in iter:
    #Obter propriedades da geometria
    geom = feature.geometry()
    #A partir do ponto obter os mais proximos, retorna o ID das colunas
    nearestIds = spIndex.nearestNeighbor(geom.asPoint(),2)
    #Retorna uma tupla dos IDs das linhas selecionadas
    t = tuple([int(i) for i in nearestIds])
    #Calcula a media para os IDs selecionados
    cursor.execute("SELECT AVG(z) FROM point_cloud WHERE gid in %s" % (t,))
    #Transforma o valor em float
    float([str(i).split("'")[1] for i in cursor][0])
 
print float([str(i).split("'")[1] for i in cursor][0])
fimGeom = time.time()
print 'Tempo Geom: ',(fimGeom - iniGeom) , ' segundos'
