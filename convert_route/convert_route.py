
from qgis.core import QgsProcessing,QgsProcessingAlgorithm
from qgis.core import QgsProcessingParameterField,QgsProcessingParameterVectorLayer,QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterFileDestination,QgsProcessingParameterBoolean
from . msb_model import msbModel
import os


FIELDS = ['label','direction','length','startNode','endNode','startDate','endDate','function']


class convertRoute(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        
        self.addParameter(QgsProcessingParameterFile('inputFile', 'File to convert',fileFilter='sec(*.sec);;sr(*.sr);;rte(*.rte)'))
        
        self.addParameter(QgsProcessingParameterFileDestination('outputFile', 'Save to file',fileFilter='sec(*.sec);;sr(*.sr);;rte(*.rte)',createByDefault=True),createOutput=True)

        self.addParameter(QgsProcessingParameterBoolean('reverseSecFileDirection', 'Load .sec file with reversed directions', defaultValue=False))


       # defaultNetwork = r'S:\Drew\hapms network\network_with_nodes\network_with_nodes.shp'
        defaultNetwork = None

        self.addParameter(QgsProcessingParameterVectorLayer('network', 'Layer with network', types=[QgsProcessing.TypeVector], defaultValue=defaultNetwork,optional=True))
        
        self.addParameter(QgsProcessingParameterField('label', 'Field with section label', type=QgsProcessingParameterField.String, parentLayerParameterName='network', defaultValue='sect_label',optional=True))
        self.addParameter(QgsProcessingParameterField('direction', 'Field with section direction', type=QgsProcessingParameterField.String, parentLayerParameterName='network', defaultValue='direc_code',optional=True))
        self.addParameter(QgsProcessingParameterField('length', 'Field with section length', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='network', defaultValue='sec_length',optional=True))
        self.addParameter(QgsProcessingParameterField('startNode', 'Field with start node', parentLayerParameterName='network', defaultValue='start_lrp_',optional=True))
        self.addParameter(QgsProcessingParameterField('endNode', 'Field with end node', parentLayerParameterName='network', defaultValue='end_lrp_co',optional=True))
        self.addParameter(QgsProcessingParameterField('startDate', 'Field with section start date', parentLayerParameterName='network', defaultValue='start_date',optional=True))
        self.addParameter(QgsProcessingParameterField('endDate', 'Field with section end date', parentLayerParameterName='network', defaultValue='s_end_date',optional=True))
        self.addParameter(QgsProcessingParameterField('function', 'Field with section function', type=QgsProcessingParameterField.String, parentLayerParameterName='network', defaultValue='funct_name',optional=True))




    def prepareAlgorithm(self, parameters, context, feedback):

        self.inputFile = self.parameterAsFile(parameters,'inputFile',context)

        self.outputFile = self.parameterAsFileOutput(parameters,'outputFile',context)
        
        #output file supposed to be created but isn't when folder non existant.
        #is open(file,'w') or qgis creating file? bug in qgis?
        #only creates files in existing folder.
        folder = os.path.dirname(self.outputFile)
        if not os.path.isdir(folder):
            os.mkdir(folder)
        

        self.layer = self.parameterAsVectorLayer(parameters,'network',context)

        self.reverseSecFileDirection = self.parameterAsBoolean(parameters,'reverseSecFileDirection',context)


        self.fields = {}        
        self.fields['label'] = self.parameterAsFields(parameters,'label',context)[0]
        self.fields['section_direction'] = self.parameterAsFields(parameters,'direction',context)[0]
        self.fields['length'] = self.parameterAsFields(parameters,'length',context)[0]
        self.fields['start_node'] = self.parameterAsFields(parameters,'startNode',context)[0]
        self.fields['end_node'] = self.parameterAsFields(parameters,'endNode',context)[0]
        self.fields['start_date'] = self.parameterAsFields(parameters,'startDate',context)[0]
        self.fields['end_date'] = self.parameterAsFields(parameters,'endDate',context)[0]
        self.fields['function'] = self.parameterAsFields(parameters,'function',context)[0]

   
        return True


#run before processAlgorithm,
    def checkParameterValues(self,parameters,context):
        s = super().checkParameterValues(parameters,context)
        if s[0] == False:
            return s
   
        ext = os.path.splitext(self.parameterAsFile(parameters,'outputFile',context))[-1]
        if ext=='.rte':
            #layer and fields required if output is rte

            if not self.parameterAsVectorLayer(parameters,'network',context):
                return False,'Layer required for writing rte files'
            
            if not self.parameterAsFields(parameters,'label',context):
                return False,'Label field required for writing rte files'

            if not self.parameterAsFields(parameters,'direction',context):
                return False,'section direction field required for writing rte files'
            
        return True,''   
        

    def processAlgorithm(self, parameters, context, feedback):
        model = msbModel()
        
        with open(self.inputFile,'r') as f:
            model.load(f,row=0,layer=self.layer,fields=self.fields,rev=self.reverseSecFileDirection)
          
                    
        with open(self.outputFile,'w') as f:
            model.save(f,self.layer,self.fields)
        
        
        return {'OUTPUT':self.outputFile}

  
    def name(self):
        return 'convert_route'


    def displayName(self):
        return 'Convert route'


    def group(self):
        return 'PTS tools'


    def groupId(self):
        return ''


    def createInstance(self):
        return convertRoute()


    def shortHelpString(self):
        return  r'''<html><body>
        <p>Converts routes between .sec,.sr  and .rte formats.</p>
        <p>A network is required to read and write rte files.</p>
        <p>A copy of the HAPMS network is at S:\Drew\hapms network\network_with_nodes</p>
        <p>Using this remotely can be slow. Copy to your pc for better performance. </p>
        
        </body></html>
        '''
        
     