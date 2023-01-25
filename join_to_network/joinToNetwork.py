"""
Model exported as python.
Name : Join to network
Group : 
With QGIS : 32200
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterVectorDestination

import processing


class joinToNetworkAlgorithm(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('networkLayer', 'Layer with network', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('networkLabelField', 'Field with section label', type=QgsProcessingParameterField.String, parentLayerParameterName='networkLayer', allowMultiple=False, defaultValue=None))
        
        self.addParameter(QgsProcessingParameterVectorLayer('dataLayer', 'Layer with data', types=[QgsProcessing.TypeVector], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('labelField', 'Data field with section label', type=QgsProcessingParameterField.String, parentLayerParameterName='dataLayer', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterField('startChainageField', 'Field with start chainage', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='dataLayer', allowMultiple=False, defaultValue=None))#type=QgsProcessingParameterField.Numeric
        self.addParameter(QgsProcessingParameterField('endChainageField', 'Field with end chainage', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='dataLayer', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterField('lengthField', 'Field with section length', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='dataLayer', allowMultiple=False, defaultValue=None,optional=True))
        
        #self.addParameter(QgsProcessingParameterFeatureSink('OUTPUT', 'Joined layer', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        #self.addParameter(QgsProcessingParameterFeatureSink('OUTPUT', 'Joined layer', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
       
       # self.addParameter(QgsProcessingParameterBoolean('includeGaps', 'Include gaps',  defaultValue=False))

        op = QgsProcessingParameterVectorDestination('OUTPUT', 'OUTPUT', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='TEMPORARY_OUTPUT',optional=True)
        self.addParameter(op,createOutput=True)

    def prepareAlgorithm(self,parameters,context,feedback):
        self.networkLayer = self.parameterAsVectorLayer(parameters,'networkLayer',context)
        self.networkLabelField = self.parameterAsFields(parameters,'networkLabelField',context)[0]

        self.dataLayer = self.parameterAsVectorLayer(parameters,'dataLayer',context)
        self.labelField = self.parameterAsFields(parameters,'labelField',context)[0]
        self.startChainageField = self.parameterAsFields(parameters,'startChainageField',context)[0]
        self.endChainageField = self.parameterAsFields(parameters,'endChainageField',context)[0]
                
        fields = self.networkLayer.fields()
        fields.extend(self.dataLayer.fields())
        #self.sink,self.destId =  self.parameterAsSink(parameters,'OUTPUT',context,fields)
        self.output = self.parameterAsOutputLayer(parameters,'OUTPUT',context)
       
       
        f = self.parameterAsFields(parameters,'lengthField',context)
        if f:
            self.lengthField = f[0]
        else:
            self.lengthField = None
        
        
      #  self.gaps = self.parameterAsBoolean(parameters,'includeGaps',context)
        
        #self.joinedLayer = self.parameterAsVectorLayer(parameters,'JoinedLayer',context)
        return True

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}



        # Join attributes by field value
        #seems to need vectorlayer rather than feature source
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': self.networkLabelField,
            'FIELDS_TO_COPY': [''],
            'FIELD_2': self.labelField,
            'INPUT': self.networkLayer,
            'INPUT_2': self.dataLayer,
            'METHOD': 0,  # Create separate feature for each matching feature (one-to-many)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)


        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}


        #set geometry through "geometry by expression"

            #expression for geometry
        if self.lengthField is None:
            e = '''if ({ech}>={sch},
            line_substring($geometry,{sch},{ech}),
            reverse(line_substring($geometry,{ech},{sch}))
            )'''.format(sch=self.startChainageField,ech=self.endChainageField)
            
            
        else:
            e = '''if ({ech}>={sch},
            line_substring($geometry,{sch}*$length/{length},{ech}*$length/{length}),
            reverse(line_substring($geometry,{ech}*$length/{length},{sch}*$length/{length}))
            )'''.format(sch=self.startChainageField,ech=self.endChainageField,length=self.lengthField)
        
                
        # 
        alg_params = {
            'EXPRESSION': e,
            'INPUT': outputs['JoinAttributesByFieldValue']['OUTPUT'],
            'OUTPUT_GEOMETRY': 1,  # Line
            'WITH_M': False,
            'WITH_Z': False,
            'OUTPUT': self.output
        }
        
        
        
        outputs['GeometryByExpression'] = processing.run('native:geometrybyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        #context.addLayerToLoadOnCompletion(self.output,QgsProcessingContext.LayerDetails('Joined Layer', QgsProject.instance(), ''))


        results['OUTPUT'] = self.output
        return results



    def name(self):
        return 'join_to_network'



    def displayName(self):
        return 'Join to network'


    def group(self):
        return ''


    def groupId(self):
        return ''


    def createInstance(self):
        return joinToNetworkAlgorithm()


    def shortHelpString(self):
        return """<html><body>
        
        <p>Joins a layer with the road network to a layer with data. Geometry is calculated from start and end chainage fields of the data.</p>
        <p>CSVs need importing into QGIS for column types to be recognised.</p>
        
        
<br></body></html>

"""