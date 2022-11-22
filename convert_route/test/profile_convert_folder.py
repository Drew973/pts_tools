import os

from pts_tools.shared_test import test_alg

from pts_tools import convert_route
testFolder = os.path.join(os.path.dirname(convert_route.__file__),'test')


def profileConvertFolder():
    
    p = { 'convertTo' : 2,
    'direction' : 'direc_code',
    'endDate' : 's_end_date',
    'endNode' : 'end_lrp_co',
    'function' : 'funct_name',
    'inputFolder' : os.path.join(testFolder,'inputs'),
    'label' : 'sect_label',
    'length' : 'sec_length',
    'network':os.path.join(test_alg.sharedTestFolder,'hapms_network','network_with_nodes.shp'),
    'outputFolder' : os.path.join(testFolder,'outputs','convert_folder'),
    'reverseSecFileDirection' : False,
    'startDate' : 'start_date',
    'startNode' : 'start_lrp_' }

    f = os.path.join(testFolder,'convert_route_profile.txt')
    print(f)
    test_alg.testAlg('PTS tools:convert_route_folder',p,f)

if __name__=='__console__':
    profileConvertFolder()
  