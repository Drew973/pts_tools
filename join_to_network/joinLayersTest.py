from qgis import processing

p = { 'OUTPUT' : 'TEMPORARY_OUTPUT',
'dataLayer' : 'file:///C:/Users/drew.bennett/Documents/area%2014%20tool/example_data.csv?type=csv&maxFields=10000&detectTypes=yes&geomType=none&subsetIndex=no&watchFile=no',
'endChainageField' : 'SectionEndCh',
'labelField' : 'SectionID', 'lengthField' : 'Length', 
'networkLabelField' : 'sect_label',
'networkLayer' : 'C:/Users/drew.bennett/Documents/area 14 tool/network/network.shp', 'startChainageField' : 'SectionStartCh' }

p['OUTPUT']=r'C:\Users\drew.bennett\Documents\area 14 tool\test.gpkg'

r = processing.run('PTS tools:join_to_network', p)
print(r)
QgsProject.instance().addMapLayer(r['OUTPUT'])
