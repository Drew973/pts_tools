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
import processing


class processDistressLayer(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('datalayer', 'data layer', types=[QgsProcessing.TypeVector], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('sectionlabelfield', 'Data field with section label', type=QgsProcessingParameterField.Any, parentLayerParameterName='datalayer', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterField('fieldwithsubsectionid', 'Data field with subsection', type=QgsProcessingParameterField.Any, parentLayerParameterName='datalayer', allowMultiple=False, defaultValue=None))
      
        self.addParameter(QgsProcessingParameterVectorLayer('splitlayer', 'split layer', defaultValue=None))
        self.addParameter(QgsProcessingParameterField('splitLabelField', 'Split field with section label', type=QgsProcessingParameterField.Any, parentLayerParameterName='splitlayer', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterField('splitSubsectionField', 'split field with subsection', type=QgsProcessingParameterField.Any, parentLayerParameterName='splitlayer', allowMultiple=False, defaultValue=None))
       
        self.addParameter(QgsProcessingParameterFeatureSink('Output', 'OUTPUT', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))



    def prepareAlgorithm(self, parameters, context, feedback):

        return True



#join by attributes causing crash. see if creating attribute indexes helps.
    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(5, model_feedback)
        results = {}
        outputs = {}

        dest = processing.QgsProcessingUtils.generateTempFilename('distress.gpkg')
        


        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'combined',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # String
            'FORMULA': " concat( to_string( @sectionlabelfield  ),'_',to_string( @fieldwithsubsectionid  ) )",
            'INPUT': parameters['datalayer'],
            'OUTPUT': 'ogr:dbname=\'{dest}\' table="data" (geom)'.format(dest=dest)
        }
        outputs['concatData'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        #creating attribute indexes.
        alg_params = {'INPUT':outputs['concatData'],'FIELD':'combined'}
        processing.run('native:createattributeindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)


        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'combined',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # String
            'FORMULA': " concat( to_string( @splitLabelField   ),'_',to_string(  @splitSubsectionField   ) )",
            'INPUT': parameters['splitlayer'],
            'OUTPUT': 'ogr:dbname=\'{dest}\' table="split" (geom)'.format(dest=dest)
        }
        outputs['concatSplit'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
       
       
        #creating attribute indexes.
        alg_params = {'INPUT':outputs['concatSplit'],'FIELD':'combined'}
        processing.run('native:createattributeindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)


        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'combined',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'combined',
            'INPUT': outputs['concatSplit']['OUTPUT'],
            'INPUT_2': outputs['concatData']['OUTPUT'],
            'METHOD': 0,  # Create separate feature for each matching feature (one-to-many)
            'PREFIX': '',
            'OUTPUT': parameters['Output']
        }
  
  
        print(alg_params)
        
        
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Output'] = outputs['JoinAttributesByFieldValue']['OUTPUT']
        #results['Output'] = None

        
        return results



    def name(self):
        return 'process distress layer'

    def displayName(self):
        return 'process distress layer'

    def group(self):
        return 'PTS tools'

    def groupId(self):
        return ''

    def createInstance(self):
        return processDistressLayer()
