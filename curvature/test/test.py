import processing

params = { 'INPUT' : 'C:/Users/drew.bennett/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/pts_tools/extract_by_curvature/test/network.gpkg|layername=network', 
'OUTPUT' : 'TEMPORARY_OUTPUT',
'lengthField' : '',
'resolution' : 5,
'threshold' : 500 }

processing.runAndLoadResults('PTS tools:extract_curved',params)