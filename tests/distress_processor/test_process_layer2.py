import processing
import cProfile, pstats

import os

from console.console import _console
script = os.path.dirname(_console.console.tabEditorWidget.currentWidget().path)

if __name__=='__console__':
    params = {'dataLayer': 'C:\\Users\\drew.bennett\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\pts_tools\\tests\\distress_processor\\example_data.csv',
    'dataLabelField': 'SectionID',
    'dataSubsectionField': 'subsection_id',
    'splitLayer': QgsProject.instance().mapLayersByName('split copy')[0],
    'splitLabelField': 'SectionID', 
    'splitSubsectionField': 'Sample Unit Id'}
            
    processing.runAndLoadResults('PTS tools:process distress layer',params)
      