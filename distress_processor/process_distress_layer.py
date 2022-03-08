"""
Model exported as python.
Name : process distress layer
Group : PTS tools
With QGIS : 32200
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsVectorLayer
from qgis.core import QgsWkbTypes
from qgis.core import QgsProcessingParameterVectorDestination
from qgis.core import QgsProcessingContext
from qgis.core import QgsProject


import processing

from osgeo import gdal
import sqlite3

from collections import OrderedDict


splitCombinedField = 'splitCombined'


class processDistressLayer(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('dataLayer', 'data layer', types=[QgsProcessing.TypeVector], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('dataLabelField', 'Data field with section label', type=QgsProcessingParameterField.Any, parentLayerParameterName='dataLayer', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterField('dataSubsectionField', 'Data field with subsection', type=QgsProcessingParameterField.Any, parentLayerParameterName='dataLayer', allowMultiple=False, defaultValue=None))
      
        self.addParameter(QgsProcessingParameterVectorLayer('splitLayer', 'split layer', defaultValue=None))
        self.addParameter(QgsProcessingParameterField('splitLabelField', 'Split field with section label', type=QgsProcessingParameterField.Any, parentLayerParameterName='splitLayer', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterField('splitSubsectionField', 'split field with subsection', type=QgsProcessingParameterField.Any, parentLayerParameterName='splitLayer', allowMultiple=False, defaultValue=None))
       
        op = QgsProcessingParameterVectorDestination('OUTPUT', 'OUTPUT', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='TEMPORARY_OUTPUT')
        self.addParameter(op,createOutput=True)

       


    def prepareAlgorithm(self, parameters, context, feedback):

        self.split = self.parameterAsVectorLayer(parameters,'splitLayer',context)
        self.data = self.parameterAsVectorLayer(parameters,'dataLayer',context)
        
        self.dataLabelField = self.parameterAsFields(parameters,'dataLabelField',context)[0]
        self.dataSubsectionField = self.parameterAsFields(parameters,'dataSubsectionField',context)[0]
        
        self.splitLabelField = self.parameterAsFields(parameters,'splitLabelField',context)[0]
        self.splitSubsectionField = self.parameterAsFields(parameters,'splitSubsectionField',context)[0]
       
        self.output = self.parameterAsOutputLayer(parameters,'OUTPUT',context)
       
        self.dataCombinedField = 'combined'

        self.fields = self.data.fields()
        self.fields.extend(self.split.fields())
        
        return True




    def checkParameterValues(self,parameters,context):
    
        s = super().checkParameterValues(parameters,context)
        if s[0] == False:
            return s
   
        data = self.parameterAsVectorLayer(parameters,'dataLayer',context)
        dataLabelField = self.parameterAsFields(parameters,'dataLabelField',context)[0]
        dataSubsectionField = self.parameterAsFields(parameters,'dataSubsectionField',context)[0]
        
        if not dataLabelField in data.fields().names():
            return False,'No field of data layer named {f} found'.format(f=dataLabelField)
 
        if not dataSubsectionField in data.fields().names():
            return False,'No field of data layer named {f} found'.format(f=dataSubsectionField)
 
        return True,''   
        

    def processAlgorithm(self, parameters, context, model_feedback):
    
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)

        feedback.setCurrentStep(0)
        self.split = importSplit(self.split,context,feedback,[self.splitLabelField,self.splitSubsectionField])
        
        if feedback.isCanceled():
            return {}
        feedback.setCurrentStep(1)
        
        self.importData(context,feedback)
        
        if feedback.isCanceled():
            return {}
        feedback.setCurrentStep(2)
        
        self.join(context,feedback) 
        
        if feedback.isCanceled():
            return {}
        feedback.setCurrentStep(3)
        
        self.export(context,feedback)
        
        context.addLayerToLoadOnCompletion(self.output,QgsProcessingContext.LayerDetails('Joined Layer', QgsProject.instance(), ''))
        return {'OUTPUT':self.output}


    def importData(self, context, feedback):
        if self.data.dataProvider().fieldNameIndex(self.dataCombinedField)==-1:#field not found

            e = 'concat("{f1}",{sep},"{f2}")'.format(f1=self.dataLabelField,f2=self.dataSubsectionField,sep="'_'")
       
            params = { 'FIELD_LENGTH' : 0, 
            'FIELD_NAME' : self.dataCombinedField,
            'FIELD_PRECISION' : 0,
            'FIELD_TYPE' : 2,
            'FORMULA' : e,
            'INPUT' : self.data,
            'OUTPUT' : 'TEMPORARY_OUTPUT' }

            r = processing.run('native:fieldcalculator',params,is_child_algorithm=True,context=context,feedback=feedback)
            
            self.data = r['OUTPUT']


    def join(self, context, feedback):
        
        params = { 'DISCARD_NONMATCHING' : False,
         'FIELD' : splitCombinedField,
         'FIELDS_TO_COPY' : [],
         'FIELD_2' : self.dataCombinedField,
         'INPUT' : self.split,
         'INPUT_2' : self.data,
         'METHOD' : 0,
         'OUTPUT' : 'TEMPORARY_OUTPUT',
         'PREFIX' : '' }

        self.joined = processing.run('native:joinattributestable',params,is_child_algorithm=True,context=context,feedback=feedback)['OUTPUT']


        
    def export(self, context, feedback):
    
        #toDrop = [name for name in self.joined.fields().names() if not name in self.fields.names()]
       
      #  with edit(self.joined):
       #     self.joined.dataProvider().deleteAttributes([toDrop])
      #  self.joined.updateFields()
       
     #  params = {
     #  }
       

        params = { 'FIELDS' : self.fields.names(),
        'INPUT' : self.joined,
        'OUTPUT' : self.output }
        
        processing.run('native:retainfields',params,is_child_algorithm=True,context=context,feedback=feedback)



    def name(self):
        return 'process_distress_layer'

    def displayName(self):
        return 'Process distress layer'

    def group(self):
        return 'PTS tools'

    def groupId(self):
        return ''

    def createInstance(self):
        return processDistressLayer()


    def shortHelpString(self):
        return '''<html><body>
        <p>Left joins split layer to data layer on dataLabelField=splitLabelField and dataSubsectionField=splitSubsectionField.</p>
        <p>Creates tempuary or uses existing geopackage with indexes on these fields for performance reasons.</p>
        <p>If layers are in geopackage this may be edited with new table added and/or indexes created.</p>
        </html></body>
        '''
        
        
        
def importSplit(split, context, feedback,fields):
    if split.dataProvider().fieldNameIndex(splitCombinedField)==-1:#field not found

        e = 'concat("{f1}",{sep},"{f2}")'.format(f1=fields[0],f2=fields[1],sep="'_'")
       
        params = { 'FIELD_LENGTH' : 0, 
            'FIELD_NAME' : splitCombinedField,
            'FIELD_PRECISION' : 0,
            'FIELD_TYPE' : 2,
            'FORMULA' : e,
            'INPUT' : split,
            'OUTPUT' : 'TEMPORARY_OUTPUT' }

        print(params)
        return processing.run('native:fieldcalculator',params,is_child_algorithm=True,context=context,feedback=feedback)['OUTPUT']
    else:
        return split
