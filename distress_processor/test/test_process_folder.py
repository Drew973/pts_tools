import os


from pts_tools.shared_test import test_alg
from pts_tools import distress_processor

folder = os.path.dirname(distress_processor.__file__)


def profile():

    params = { 'dataLabelField' : 'SectionID',
    'inputFolder' : os.path.join(folder,'test','example_data'),
    'outputFolder' : os.path.join(folder,'test','output'),
    'split': os.path.join(test_alg.sharedTestFolder,'split_network.gpkg|layername=split'),
    'dataSubsectionField' : 'Sample Unit Id',
    'dataLabelField' : 'SectionID',
    'splitLabelField' : 'sect_label',
    'splitSubsectionField' : 'subsection_id'
    }

    f = os.path.join(folder,'test','process_distress_folder_profile.txt')
    test_alg.testAlg('PTS tools:process_distress_folder',params,f)
    
    
if __name__=='__console__':
   profile()
  