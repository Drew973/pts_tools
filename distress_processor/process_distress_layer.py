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


class processDistressLayer(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('dataLayer', 'data layer', types=[QgsProcessing.TypeVector], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('dataLabelField', 'Data field with section label', type=QgsProcessingParameterField.Any, parentLayerParameterName='dataLayer', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterField('dataSubsectionField', 'Data field with subsection', type=QgsProcessingParameterField.Any, parentLayerParameterName='dataLayer', allowMultiple=False, defaultValue=None))
      
        self.addParameter(QgsProcessingParameterVectorLayer('splitLayer', 'split layer', defaultValue=None))
        self.addParameter(QgsProcessingParameterField('splitLabelField', 'Split field with section label', type=QgsProcessingParameterField.Any, parentLayerParameterName='splitLayer', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterField('splitSubsectionField', 'split field with subsection', type=QgsProcessingParameterField.Any, parentLayerParameterName='splitLayer', allowMultiple=False, defaultValue=None))
       
        op = QgsProcessingParameterVectorDestination('OUTPUT', 'OUTPUT', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='TEMPORARY_OUTPUT',optional=True)
        self.addParameter(op,createOutput=True)


    def prepareAlgorithm(self, parameters, context, feedback):

        self.split = self.parameterAsVectorLayer(parameters,'splitLayer',context)
        self.data = self.parameterAsVectorLayer(parameters,'dataLayer',context)
        
        self.dataLabelField = self.parameterAsFields(parameters,'dataLabelField',context)[0]
        self.dataSubsectionField = self.parameterAsFields(parameters,'dataSubsectionField',context)[0]
        
        self.splitLabelField = self.parameterAsFields(parameters,'splitLabelField',context)[0]
        self.splitSubsectionField = self.parameterAsFields(parameters,'splitSubsectionField',context)[0]
       
        self.output = self.parameterAsOutputLayer(parameters,'OUTPUT',context)

        self.temp = gpkgDest(self.split,self.data)
       
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
    
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)

        feedback.setCurrentStep(1)
        self.importLayers(context,feedback)
        
        if feedback.isCanceled():
            return {}
            
        feedback.setCurrentStep(2)
        
        
        self.createIndexes()
        self.join(context,feedback) 
        
        results = {'OUTPUT':self.output}
        
        context.addLayerToLoadOnCompletion(self.output,QgsProcessingContext.LayerDetails('Joined Layer', QgsProject.instance(), ''))
        return results


  #import layers into single geopackage if necessary
    def importLayers(self, context, feedback):

        layers = []#layers to import
        keys = []
        
        
        if gpkgPath(self.split) != self.temp:
            layers.append(self.split)
            keys.append('split')
            
        if gpkgPath(self.data) != self.temp:
            layers.append(self.data)
            keys.append('data')
        
        
        if layers:
            alg_params = {'LAYERS': layers,
                      'OUTPUT': self.temp,
                      'OVERWRITE': False,  # Important!
                      'SAVE_STYLES': False,
                      'SAVE_METADATA': False,
                      'SELECTED_FEATURES_ONLY': False}
                      
              
            r = processing.run("native:package", alg_params,is_child_algorithm=True,context=context,feedback=feedback)['OUTPUT_LAYERS']
       
        if 'split' in keys:
            i = keys.index('split')
            self.split = r[i]
          
        if 'data' in keys:
            i = keys.index('data')
            self.data = r[i]
            

        self.splitTable = gpkgTable(self.split,feedback)
        self.dataTable = gpkgTable(self.data,feedback)



    #create indexes on used fields
    def createIndexes(self):
        
        c = 'create index if not exists "{name}" on "{table}"("{col}")'
        
        with sqlite3.connect(self.temp) as con:
            con.execute(c.format(table=self.splitTable,col=self.splitLabelField,name='split1'))
            con.execute(c.format(table=self.splitTable,col=self.splitSubsectionField,name='split2'))
            con.execute(c.format(table=self.dataTable,col=self.dataLabelField,name='data1'))
            con.execute(c.format(table=self.dataTable,col=self.dataSubsectionField,name='data2'))
            
            
    #run join query geopackage and export to output
    def join(self,context,feedback):
        #names for split and data?
        q = 'select "{split}".*, "{data}".* from "{split}" left join "{data}" on "{split}"."{s1}"="{data}"."{d1}" and "{split}"."{s2}"="{data}"."{d2}"'
        q = q.format(s1=self.splitLabelField,s2=self.splitSubsectionField,d1=self.dataLabelField,d2=self.dataSubsectionField,split=self.splitTable,data=self.dataTable)
              
        alg_params = { 'DIALECT' : 0,
         'INPUT' : self.temp,
         'OPTIONS' : '-unsetFid',#by default gdal tries to use column named fid as feature id,causing unique constraint to fail.
         'OUTPUT' : self.output,
         'SQL' : q }

        return processing.run('gdal:executesql',alg_params,is_child_algorithm=True,context=context,feedback=feedback)



    def name(self):
        return 'process distress layer'

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
        

#if split is geopackage use that. 
#if data is use that.
#else make new geopackage.
def gpkgDest(data,split):

    if split.storageType()=='GPKG':
        return gpkgPath(split)
    
    if data.storageType()=='GPKG':
        return gpkgPath(data)
        
    return processing.QgsProcessingUtils.generateTempFilename('distress.gpkg')
  
  
def gpkgPath(layer):
    return layer.dataProvider().dataSourceUri().split('|layername')[0]
    
    
def gpkgTable(layer,feedback):
    if isinstance(layer,str):
        s = layer
    else:  
        s = layer.source()
       
    p = s.split('|layername=')
     
    if len(p)<2: 
        feedback.reportError('table not found for layer '+str(layer))
   
    else:
       return p[1]    
    
    


