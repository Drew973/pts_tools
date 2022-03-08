import processing

params = { 'INPUT' : 'C:/Users/drew.bennett/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/pts_tools/curvature/test/network.gpkg|layername=network', 
'OUTPUT' : 'TEMPORARY_OUTPUT',
'lengthField' : '',
'spacing' : 5
}

processing.runAndLoadResults('PTS tools:estimate_curvature',params)