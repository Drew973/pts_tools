# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 09:55:07 2023

@author: Drew.Bennett
"""

from pts_tools.shared_test import test_alg
from pts_tools import shared_test

from pts_tools.polygon_from_lrs import polygon_from_lrs_alg
import processing

import unittest
import os
from qgis.core import QgsProcessingException

#run and profile algorithms.
#haven't added them all yet.
class testPolygonFromLrs(unittest.TestCase):
    
    def setUp(self):
        pass
    
    
    #test and profile split_by_chainage
    def testPolyFromLrs(self):
        
        folder = os.path.dirname(polygon_from_lrs_alg.__file__)
        shared_test.networkWithMeasure
        
        params = { 'INPUT' : shared_test.testDistresses,
          'OUTPUT' : 'TEMPORARY_OUTPUT',
          'end_measure_field' : 'end Chainage (m)',
          'end_offset_field' : 'end offset',
          'network' : shared_test.networkDbWithMeasure,
          'network_label_field' : 'sect_label',
          'start_label_field' : 'start Section ID',
          'start_measure_field' : 'start Chainage (m)',
          'start_offset_field' : 'start offset',
         }
        
        pp = os.path.join(folder,'poly_from_lrs.prof')
        
        test_alg.profileAlg(algId = 'pts:polygonfromlrs',params = params,profile = pp)
        
        
        
    #test and profile split_by_chainage
    def testInvalidNetwork(self):
        params = { 'INPUT' : shared_test.testDistresses,
          'OUTPUT' : 'TEMPORARY_OUTPUT',
          'end_measure_field' : 'end Chainage (m)',
          'end_offset_field' : 'end offset',
          'network' : shared_test.networkWithNodes,
          'network_label_field' : 'sect_label',
          'start_label_field' : 'start Section ID',
          'start_measure_field' : 'start Chainage (m)',
          'start_offset_field' : 'start offset',
         }
        with self.assertRaises(QgsProcessingException):
            r = processing.runAndLoadResults('pts:polygonfromlrs',params)

if __name__ == '__console__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testPolygonFromLrs)
    unittest.TextTestRunner().run(suite)