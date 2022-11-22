
from qgis import processing
import pts_tools
import os

from pts_tools.shared_test.test_alg import testAlg

toolsFolder = os.path.dirname(pts_tools.__file__)
testFolder = os.path.join(toolsFolder,'join_to_network','test')


class testJoinToNetwork(unittest.TestCase):
    
    def setUp(self):
        pass
    
    
    #test and profile split_by_chainage
    def test1(self):
        params = { 'OUTPUT' : 'TEMPORARY_OUTPUT', 
        'dataLayer' : os.path.join(testFolder,'example_data.csv'),
        'endChainageField' : 'SectionEndCh',
        'labelField' : 'SectionID',
        'lengthField' : '', 
        'networkLabelField' : 'sect_label',
        'networkLayer' : os.path.join(toolsFolder,'shared_test','hapms_network','network_with_nodes.shp'),
        'startChainageField' : 'SectionStartCh' }
        
        f = os.path.join(testFolder,'join_to_network_profile.txt')
        
        testAlg('PTS tools:join_to_network',params,f)


if __name__ == '__console__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testJoinToNetwork)
    unittest.TextTestRunner().run(suite)