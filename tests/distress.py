import processing
from qgis.core import QgsProject


split = QgsProject.instance().mapLayersByName('split')[0]

p = { 'field1' : 'SectionID', 'field2' : 'Sample Unit Id', 'field3' : 'a', 
'inputFolder' : 'C:\\Users\\drew.bennett\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\distress_processor\\test',
'outputFolder' : 'TEMPORARY_OUTPUT',
'split' : split,
'splitFields' : ['sect_label','subsection_id'] }


#p['field1']='a'
r = processing.run('PTS tools:distress_processor',p)
#seems to be working.
#layer needs loading through.

#for layer in r['OUTPUT']:
 #   QgsProject.instance().addMapLayer(layer, True)
    #'Joined_layer_b4b3d193_4487_4359_869e_02fa33585191'
    #QgsProject.instance().mapLayer('Joined_layer_b4b3d193_4487_4359_869e_02fa33585191')