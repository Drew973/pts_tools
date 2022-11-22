import os


from pts_tools.shared_test import test_alg
from pts_tools import distress_processor

folder = os.path.dirname(distress_processor.__file__)


def profile():
    
    params = { 'OUTPUT' : 'TEMPORARY_OUTPUT',
    'dataLayer' : os.path.join(folder,'test','example_data','example_data.csv'), 
    'dataSubsectionField' : 'Sample Unit Id',
    'dataLabelField' : 'SectionID',
    'splitLabelField' : 'sect_label',
    'splitSubsectionField' : 'subsection_id',
    'splitLayer' : os.path.join(test_alg.sharedTestFolder,'split_network.gpkg|layername=split') }

    f = os.path.join(folder,'test','process_distress_layer_profile.txt')
    test_alg.testAlg('PTS tools:process_distress_layer',params,f)
    
    
    
if __name__=='__console__':
   profile()
  