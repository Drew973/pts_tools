
from qgis.core import QgsProcessing,QgsProcessingAlgorithm
from qgis.core import QgsProcessingParameterField,QgsProcessingParameterVectorLayer,QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterFolderDestination,QgsProcessingParameterBoolean,QgsProcessingParameterEnum,QgsProcessingOutputString
import os
import processing

FORMATS = ['.sec','.sr','.rte']


FIELDS = ['label','direction','length','startNode','endNode','startDate','endDate','function']


class convertRouteFolder(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        
        self.addParameter(QgsProcessingParameterFile('inputFolder', 'Folder to convert',behavior = QgsProcessingParameterFile.Folder))
        
        self.addParameter(QgsProcessingParameterFolderDestination('outputFolder', 'Save to folder'),createOutput=True)

        self.addParameter(QgsProcessingParameterEnum('convertTo','Convert to',FORMATS,defaultValue='.sr'))

        self.addParameter(QgsProcessingParameterBoolean('reverseSecFileDirection', 'Load .sec files with reversed directions', defaultValue=False))            

        #defaultNetwork = r'S:\Drew\hapms network\network_with_nodes\network_with_nodes.shp'
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

        self.addOutput(QgsProcessingOutputString('inputFiles','Input files'))
        self.addOutput(QgsProcessingOutputString('outputFiles','Ouput files'))


    #destination for inputFile given outputFolder and output extention
    def dest(self,inputFile,outputFolder,ext):
        
        p = os.path.basename(inputFile)
        name = os.path.splitext(p)[0]#name
        return os.path.join(outputFolder,name+ext)


    def prepareAlgorithm(self, parameters, context, feedback):

        inputFolder = self.parameterAsFile(parameters,'inputFolder',context)

        ext = FORMATS[self.parameterAsEnum(parameters,'convertTo',context)]
        
        outputFolder = self.parameterAsFile(parameters,'outputFolder',context)


        #{inputFile:outputFile}
        self.files = {f:self.dest(f,outputFolder,ext) for f in getFiles(inputFolder,FORMATS)}
        
        self.layer = self.parameterAsVectorLayer(parameters,'network',context)
        
        self.reverseSecFileDirection = self.parameterAsBoolean(parameters,'reverseSecFileDirection',context)



        self.fields = {}
        for f in FIELDS:
            self.fields[f] = self.parameterAsFields(parameters,f,context)[0]
  
    
        return True


    '''
    def checkParameterValues(self,parameters,context):
    
        s = super().checkParameterValues(parameters,context)
        if s[0] == False:
            return s
   
   
        ext1 = os.path.splitext(self.parameterAsFile(parameters,'inputFile',context))
        ext2 = os.path.splitext(self.parameterAsFile(parameters,'outputFile',context))
        
        if ext1=='.rte' or ext2=='.rte':
            
            #layer required if input or output is rte

            if self.parameterAsVectorLayer(parameters,'network',context) is None:
                return False,'Layer required for reading/writing rte files'
            
            if self.parameterAsFields(parameters,'label',context)[0] is None:
                return False,'Label field required for reading/writing rte files'

            if self.parameterAsFields(parameters,'section_direction',context)[0] is None:
                return False,'section direction field required for reading/writing rte files'
            
        return True,''   
        '''

    def processAlgorithm(self, parameters, context, feedback):
        
        print(self.files)
        n = len(self.files)
        
        feedback.setProgress(0)
              
        outputFiles = []
        inputFiles = []
        
        for i,k in enumerate(self.files):
            inputFiles.append(k)
            
            p = self.fields
            p.update(
            {'inputFile' : k,
            'network' : self.layer,
            'outputFile' : self.files[k],
            'reverseSecFileDirection' : self.reverseSecFileDirection,
            })
                    
            r = processing.run('PTS tools:convert_route',p,feedback=feedback,context=context)
            outputFiles.append(r['OUTPUT'])
            
            feedback.setProgress(100*i/n)
            
        return {'inputFiles':str(inputFiles),'outputFiles':str(outputFiles)}

  
    def name(self):
        return 'convert_route_folder'


    def displayName(self):
        return 'Convert route folder'


    def group(self):
        return 'PTS tools'


    def groupId(self):
        return ''


    def createInstance(self):
        return convertRouteFolder()


    def shortHelpString(self):
        return r'''<html><body>
        <p>Converts all routes in folder to desired format.</p>
        <p>Converts between .sec,.sr  and .rte formats.</p>
        <p>A network is required to write rte files.</p>
        <p>A copy of the HAPMS network is at S:\Drew\hapms network\network_with_nodes</p>
        <p>Using this remotely can be slow,Copy to your pc for better performance. </p>
        
        </body></html>
        '''
        
def getFiles(folder,exts=None):
    for root, dirs, files in os.walk(folder, topdown=False):
        for f in files:
            if os.path.splitext(f)[1] in exts or exts is None:
                yield os.path.join(root,f)
    