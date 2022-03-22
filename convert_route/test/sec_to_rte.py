
p = { 'direction' : 'direc_code',
'endDate' : 's_end_date',
'endNode' : 'end_lrp_co',
'function' : 'funct_name',
'inputFile' : 'C:\\Users\\drew.bennett\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\pts_tools\\convert_route\\test\\D0720.sec',
'label' : 'sect_label',
'length' : 'sec_length',
'network' : 'S:/Drew/hapms network/network_with_nodes/network_with_nodes.shp',
'outputFile' : 'C:/Users/drew.bennett/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/pts_tools/convert_route/test/test_output.rte',
'reverseSecFileDirection' : False,
'startDate' : 'start_date',
'startNode' : 'start_lrp_' }

processing.run('PTS tools:convert_route',p)