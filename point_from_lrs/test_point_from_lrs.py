# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 09:55:07 2023

@author: Drew.Bennett
"""

from pts_tools.shared_test import test_alg
from pts_tools import shared_test

from pts_tools.point_from_lrs import point_from_lrs_alg
import processing

import unittest
import os
from qgis.core import QgsProcessingException,QgsProject

#run and profile algorithms.
#haven't added them all yet.
class testPointFromLrs(unittest.TestCase):
    
    def setUp(self):
        pass
    
    
    #test and profile split_by_chainage
    def testPolyFromLrs(self):
        
        folder = os.path.dirname(point_from_lrs_alg.__file__)
                
        params = { 'INPUT' : shared_test.testDistresses,
        'OUTPUT' : 'TEMPORARY_OUTPUT',
        'network' : shared_test.networkWithMeasure,
        'network_label_field' : 'sect_label',
        'label_field' : 'start Section ID',
        'measure_field' : 'start Chainage (m)',
        'offset_field' : '' }
        
        pp = os.path.join(folder,'point_from_lrs.prof')
        r = test_alg.profileAlg(algId = 'pts:pointfromlrs',params = params,profile = pp)
        layer = QgsProject.instance().mapLayer(r['OUTPUT'])
        self.assertTrue(layer.featureCount()>0)
        
        
if __name__ == '__console__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testPointFromLrs)
    unittest.TextTestRunner().run(suite)