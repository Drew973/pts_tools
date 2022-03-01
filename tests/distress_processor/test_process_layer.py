import processing
import cProfile, pstats

import os

from console.console import _console
script = os.path.dirname(_console.console.tabEditorWidget.currentWidget().path)


def test1(split,data):
    
    params = { 'OUTPUT' : 'TEMPORARY_OUTPUT',
    'dataLayer' : data, 
    'dataSubsectionField' : 'Sample Unit Id',
    'dataLabelField' : 'SectionID',
    'splitLabelField' : 'sect_label',
    'splitSubsectionField' : 'subsection_id',
    'splitLayer' : split }

    processing.runAndLoadResults('PTS tools:process distress layer',params)


if __name__=='__console__':

    data = QgsProject.instance().mapLayersByName('data copy')[0]
    split = QgsProject.instance().mapLayersByName('split copy')[0]
    
    with cProfile.Profile() as profiler:
        test1(split,data)
        
    f = os.path.join(script,'test2Profile.txt')
   
    profiler.dump_stats(f)
        
    with open(f, 'w') as to:
        stats = pstats.Stats(profiler, stream=to)
        stats.sort_stats('cumtime')
        stats.print_stats()
        
  