# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 09:48:36 2024

@author: Drew.Bennett
"""


from pts_tools.shared_test.test_alg import profileAlg



params = { 'input' : 'C:\\Users\\drew.bennett\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\pts_tools\\vcs\\M18 - Site Sheets.xlsx',
 'network' : 'C:/Users/drew.bennett/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/pts_tools/shared_test/network_with_m.gpkg|layername=output',
 'networkSec' : 'sect_label',
 'output' : 'TEMPORARY_OUTPUT' }


profileAlg(algId = 'pts:importvcsspreadsheet',params = params)

