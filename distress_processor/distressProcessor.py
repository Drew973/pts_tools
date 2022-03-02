
from qgis.core import QgsProcessing,QgsProcessingContext,QgsProject
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterFeatureSource
from qgis.core import QgsProcessingParameterFolderDestination
from qgis.core import QgsProcessingOutputMultipleLayers
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterBoolean

import processing

from . import getFiles
#from . import fieldToTextMapper

import os

class distressProcessorAlg(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):

        self.addParameter(QgsProcessingParameterFile('inputFolder', 'Input folder',behavior=QgsProcessingParameterFile.Folder,extension='.csv'))
       
        self.addParameter(QgsProcessingParameterFolderDestination('outputFolder', 'Output folder'))

        self.addParameter(QgsProcessingParameterFeatureSource('split', 'Split layer', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
    
        self.addParameter(QgsProcessingParameterField('splitLabelField', 'Field of split layer with section label', parentLayerParameterName='split'))

        self.addParameter(QgsProcessingParameterString('dataLabelField', 'CSV field with section label.'))
        
        self.addParameter(QgsProcessingParameterField('splitSubsectionField', 'Field of split layer with subsection id', parentLayerParameterName='split',defaultValue='subsection_id'))
        self.addParameter(QgsProcessingParameterString('dataSubsectionField', 'CSV field with subsection id.'))
       
        self.addParameter(QgsProcessingParameterBoolean('loadOnCompletion', 'Open output files after running algorithm',defaultValue=True))


        #https://www.faunalia.eu/en/blog/2019-07-02-custom-processing-widget for custom widget.

        self.addOutput(QgsProcessingOutputMultipleLayers('OUTPUT', 'Output layers'))
        self.addOutput(QgsProcessingOutputMultipleLayers('UNJOINED', 'Unjoined layers'))

      #  param = QgsProcessingParameterString('fields', 'fields')
      #  param.setMetadata({'widget_wrapper': {'class': fieldToTextMapper.fieldToTextWrapper}})
        #self.addParameter(param)
    
    
    def prepareAlgorithm(self, parameters, context, feedback):

        #self.split = self.parameterAsSource(parameters,'split',context)
        self.split = self.parameterAsVectorLayer(parameters,'split',context)
        
        #self.split = self.parameterAsCompatibleSourceLayerPath(parameters,'split',context,['gpkg'],'gpkg')

        folder = self.parameterAsFile(parameters,'inputFolder',context)
        self.csvs = [c for c in getFiles.getFiles(folder,'.csv')]

        self.outputFolder = self.parameterAsFile(parameters,'outputFolder',context)
        
        self.splitLabelField = self.parameterAsFields(parameters,'splitLabelField',context)[0]
        self.splitSubsectionField = self.parameterAsFields(parameters,'splitSubsectionField',context)[0]

        self.dataLabelField = self.parameterAsFields(parameters,'dataLabelField',context)[0]
        self.dataSubsectionField = self.parameterAsFields(parameters,'dataSubsectionField',context)[0]
        
        self.loadOnCompletion = self.parameterAsBoolean(parameters,'loadOnCompletion',context)
        return True


    def processAlgorithm(self, parameters, context, model_feedback):
     
        feedback = QgsProcessingMultiStepFeedback(len(self.csvs)+1, model_feedback)

        results = {'OUTPUT':[],'UNJOINED':[]}

        feedback.setProgress(0)
        feedback.setCurrentStep(0)
        
        self.importSplit(context,feedback)
                
        for i,f in enumerate(self.csvs):
                      
            dest = outputName(f,self.outputFolder)
                        
            p = {'dataLayer':f,
            'dataLabelField':self.dataLabelField,
            'dataSubsectionField':self.dataSubsectionField,
            'splitLayer':self.split,
            'splitLabelField':self.splitLabelField,
            'splitSubsectionField':self.splitSubsectionField
            ,'OUTPUT':dest
            }
            
            feedback.setCurrentStep(i)
           # feedback.setProgress(i+1/len(self.csvs))
          
            if feedback.isCanceled():
                break
            
            try:
                r = processing.run('PTS tools:process_distress_layer',p,feedback=feedback, is_child_algorithm=True)
                if 'OUTPUT' in r:
                    results['OUTPUT'].append(r['OUTPUT'])
                    
                    if self.loadOnCompletion:
                        context.addLayerToLoadOnCompletion(r['OUTPUT'],QgsProcessingContext.LayerDetails(dest, QgsProject.instance(), ''))
                    
                else:
                    results['UNJOINED'].append(f)
                    
            except Exception as e:
                results['UNJOINED'].append(f)
            
        return results


  
#
    def name(self):
        return 'process_distress_folder'


    def displayName(self):
        return 'Process distress folder'


    def group(self):
        return ''
        #return 'pts_tools'

   # def groupId(self):
    #    return 'pts_tools'


    def shortHelpString(self):
        return """<html><body><p></p>
<br></body></html>"""


    def createInstance(self):
        return distressProcessorAlg()




    def importSplit(self,context,feedback):
        if self.split.storageType()!='GPKG':
    
            alg_params = {'LAYERS': [self.split],
                          'OUTPUT':  processing.QgsProcessingUtils.generateTempFilename('distress.gpkg'),
                          'OVERWRITE': False,  # Important!
                          'SAVE_STYLES': False,
                          'SAVE_METADATA': False,
                          'SELECTED_FEATURES_ONLY': False}
                          
                  
            self.split = processing.run("native:package", alg_params,is_child_algorithm=True,context=context,feedback=feedback)['OUTPUT_LAYERS'][0]


    def shortHelpString(self):
        return '''<html><body>
        <p>Attempts to run "Process distress layer" for each csv in input folder (including subdirectories).</p>
        <p>Exports to shapefiles in output folder.</p>
        '''
        
        
        
def outputName(f,folder):
    a = os.path.splitext(os.path.basename(f))[0]
    return os.path.join(folder,a)+'.shp'

def outputName2(f,folder):
    a = os.path.splitext(os.path.basename(f))[0]
    return os.path.join(folder,'outputs')+'.gpkg|layername={table}'.format(table=a)


'''
from processing.gui.wrappers import WidgetWrapper


class DateTimeWidget(WidgetWrapper):
    """
    QDateTimeEdit widget with calendar pop up
    """

    def createWidget(self):
        self._combo = QDateTimeEdit()
        self._combo.setCalendarPopup(True)

        today = QDate.currentDate()
        self._combo.setDate(today)

        return self._combo

    def value(self):
        date_chosen = self._combo.dateTime()
        return date_chosen.toString(Qt.ISODate)
'''

        
