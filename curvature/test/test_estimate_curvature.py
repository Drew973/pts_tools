import unittest
import os

from pts_tools.shared_test import test_alg
from pts_tools import curvature

folder = os.path.dirname(curvature.__file__)
 

def profile():
    params = { 'INPUT' : os.path.join(folder,'test','network.gpkg|layername=network'), 
    'OUTPUT' : 'TEMPORARY_OUTPUT',
    'lengthField' : '',
    'spacing' : 5
    }
    
    f = os.path.join(folder,'test','estimate_curvature_profile.txt')
    test_alg.testAlg('PTS tools:estimate_curvature',params,f)


class testEstimateCurvature(unittest.TestCase):
    
    def setUp(self):
        pass
    
    
    #test and profile split_by_chainage
    def testProfile(self):
        profile()
    
    

if __name__ == '__console__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testEstimateCurvature)
    unittest.TextTestRunner().run(suite)