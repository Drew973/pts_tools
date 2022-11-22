import unittest
import os



from pts_tools.shared_test import test_alg
from pts_tools import curvature

folder = os.path.dirname(curvature.__file__)
    
    
def test():
    params = { 'INPUT' : os.path.join(folder,'test','network.gpkg|layername=network'), 
    'OUTPUT' : 'TEMPORARY_OUTPUT',
    'lengthField' : '',
    'resolution' : 5
    }
    f = os.path.join(folder,'test','extract_curvature_profile.txt')
    test_alg.testAlg('PTS tools:extract_curved',params,f)



class testExtractCurvature(unittest.TestCase):
    
    def setUp(self):
        pass

    #test and profile split_by_chainage
    def testProfile(self):
        test()
    

if __name__ == '__console__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testExtractCurvature)
    unittest.TextTestRunner().run(suite)