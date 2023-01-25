

import unittest
import os


from pts_tools.shared_test import test_alg

import os
from pts_tools import add_measure

 

def profile():
        
    params = { 'INPUT' : test_alg.networkWithNodes,
        'OUTPUT' : 'TEMPORARY_OUTPUT',
        'endMeasureField' : 'sec_length',
        'start_measure_field' : '' }

    
    f = os.path.join(os.path.dirname(add_measure.__file__),'add_measure.prof')
    test_alg.testAlg('PTS tools:add_measure',params,f)
    os.path.dirname(add_measure.__file__)


class testEstimateCurvature(unittest.TestCase):
    
    def setUp(self):
        pass
    
    
    #test and profile split_by_chainage
    def testProfile(self):
        profile()
    
#generate filepath for profile
def profileFile(module):
    return os.path.normpath(os.path.join(os.path.dirname(module.__file__),'profile.prof'))
    
    


if __name__ == '__console__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testEstimateCurvature)
    unittest.TextTestRunner().run(suite)