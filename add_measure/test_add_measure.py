

import unittest
import os


from pts_tools import shared_test

from pts_tools.shared_test.test_alg import profileAlg

from pts_tools import add_measure
from qgis.core import QgsProject
 


        


class testAddMeasure(unittest.TestCase):
    
    def setUp(self):
        pass
    
    
    #test and profile split_by_chainage
    def testProfile(self):
        
        pp = profilePath(add_measure)

        params = { 'INPUT' : shared_test.networkWithNodes,
            'OUTPUT' : 'TEMPORARY_OUTPUT',
            'endMeasureField' : 'sec_length',
            'start_measure_field' : '' }

        r = profileAlg('pts:addmeasure',params,pp)
        layer = QgsProject.instance().mapLayer(r['OUTPUT'])
       #self.assertTrue(layer.featureCount()>0)
        self.assertEqual(layer.featureCount(),21796)

    
    
#generate filepath for profile given module.
def profilePath(module):
    return os.path.normpath(os.path.join(os.path.dirname(module.__file__),'profile.prof'))
    
    
if __name__ == '__console__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testAddMeasure)
    unittest.TextTestRunner().run(suite)