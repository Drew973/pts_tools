
params = { 'bottomLeft' : '430556.910861,487674.940067 [EPSG:4326]',
'bottomRight' : '430560.465652,487676.312890 [EPSG:4326]',
'inputLayer' : r'C:/Users/drew.bennett/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/pts_tools/reposition_image/test/origonal.tif',
'OUTPUT':r'C:/Users/drew.bennett/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/pts_tools/reposition_image/test/moved.tif',
'topLeft' : '430555.365299,487679.558569 [EPSG:4326]',
'topRight' : '430558.392782,487680.931391 [EPSG:4326]' }

r = processing.runAndLoadResults('PTS tools:reposition_image',params)
print(r)