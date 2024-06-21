# -*- coding: utf-8 -*-
"""
Created on Fri May 24 13:28:18 2024

@author: Drew.Bennett
"""

from pts_tools.shared_test.test_alg import profileAlg




params = { 'input' : 'C:\\Users\\drew.bennett\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\pts_tools\\vcs\\test\\test_input_layer.gpkg|layername=test_input_layer',
          'lane':'lane',
          'wheelTrack':'wheelTrack',
          'startChain':'startChain',
          'endChain': 'endChain',
          'width' : 'width',
          'severity' : 'severity',
          'outputfile' : 'C:\\Users\\drew.bennett\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\pts_tools\\vcs\\test\\test_plot.pdf',
          'sec' : 'sec',
          'tp' : 'defectType' }


profileAlg(algId = 'pts:exportvcsschematic',params = params)
