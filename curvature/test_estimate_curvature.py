# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 09:55:07 2023

@author: Drew.Bennett
"""

from pts_tools.shared_test import test_alg
from pts_tools import shared_test

from pts_tools.curvature import estimate_curvature_alg
from qgis.core import QgsProject
import unittest


#run and profile algorithms.
#haven't added them all yet.
class testEstimateCurvature(unittest.TestCase):
    
    def setUp(self):
        pass
    
    
    #test and profile split_by_chainage
    def testPolyFromLrs(self):
        
        params = { 'INPUT' : shared_test.networkWithMeasure, 
            'OUTPUT' : 'TEMPORARY_OUTPUT',
            'lengthField' : '',
            'spacing' : 5
            }
            
        
        pp = test_alg.profilePath(estimate_curvature_alg,'estimate_curvature_profile.prof')
        r = test_alg.profileAlg(algId = 'pts:estimatecurvature',params = params,profile = pp)
        layer = QgsProject.instance().mapLayer(r['OUTPUT'])
        self.assertTrue(layer.featureCount()>0)

        
        
   
if __name__ == '__console__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testEstimateCurvature)
    unittest.TextTestRunner().run(suite)