import processing

params = { 'dataLabelField' : 'SectionID',
'inputFolder' : 'C:\\Users\\drew.bennett\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\pts_tools\\tests\\distress_processor\\example_data',
'outputFolder' : r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\tests\distress_processor\outputs',
'split': QgsProject.instance().mapLayersByName('split')[0],
'dataSubsectionField' : 'Sample Unit Id',
'dataLabelField' : 'SectionID',
'splitLabelField' : 'sect_label',
'splitSubsectionField' : 'subsection_id'
}

r = processing.runAndLoadResults('PTS tools:process_distress_folder',params)
print(r)

