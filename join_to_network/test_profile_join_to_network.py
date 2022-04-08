import processing


params = { 'OUTPUT' : 'TEMPORARY_OUTPUT', 
'dataLayer' : 'file:///C:/Users/drew.bennett/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/pts_tools/tests/distress_processor/example_data/example_data.csv?type=csv&maxFields=10000&detectTypes=yes&geomType=none&subsetIndex=no&watchFile=no',
'endChainageField' : 'SectionEndCh',
'labelField' : 'SectionID',
'lengthField' : '', 
'networkLabelField' : 'sect_label',
'networkLayer' : 'C:/Users/drew.bennett/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/pts_tools/tests/distress_processor/network/network.shp', 
'startChainageField' : 'SectionStartCh' }


processing.runAndLoadResults('PTS tools:join_to_network',params)