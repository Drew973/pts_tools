
from qgis.core import QgsProcessingAlgorithm,QgsProcessingOutputMultipleLayers,QgsProcessingParameterFile,QgsProcessingParameterNumber,QgsCoordinateReferenceSystem

from pts_tools.shared_functions import get_files
from pts_tools.load_mfv_images import details,group_functions




class loadMfvImagesAlg(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):

        self.addParameter(QgsProcessingParameterFile('inputFolder', 'Input folder',behavior=QgsProcessingParameterFile.Folder,extension='.csv'))
        self.addParameter(QgsProcessingParameterNumber('step', 'step for image ids',defaultValue=10,minValue=1))
        self.addOutput(QgsProcessingOutputMultipleLayers('OUTPUT', 'Output layers'))

      #  param = QgsProcessingParameterString('fields', 'fields')
      #  param.setMetadata({'widget_wrapper': {'class': fieldToTextMapper.fieldToTextWrapper}})
        #self.addParameter(param)
    
    
    def prepareAlgorithm(self, parameters, context, feedback):

        folder = self.parameterAsFile(parameters,'inputFolder',context)
        self.files = [f for f in get_files.getFiles(folder,['.tif'])]
        self.step = self.parameterAsInt(parameters,'step',context)
        return True


    def processAlgorithm(self, parameters, context, feedback):
        results = {'OUTPUT':[]}
        
        n = len(self.files)
        crs = QgsCoordinateReferenceSystem('EPSG:27700')
        
        
        for i,f in enumerate(self.files):
            feedback.setProgress(100*i/n)
          #  print(f)
            d = details.imageDetails(f)
            d.groups.append(imageIdToGroup(d.imageId,self.step))
            
            d.load(show=False,crs=crs)
            
            group = group_functions.findGroup(d.groups)
            group.setExpanded(False)
                    
            if feedback.isCanceled():
                return {}
            
            results['OUTPUT'].append(f)
            
        return results


  
    def name(self):
        return 'load_mfv_images'


    def displayName(self):
        return 'Load mfv images'


    def group(self):
        return ''
        #return 'pts_tools'

   # def groupId(self):
    #    return 'pts_tools'


    def createInstance(self):
        return loadMfvImagesAlg()



    def shortHelpString(self):
        return '''<html><body>
        <p>Attempts to load every tif file in folder.</p>
        <p>Layers are hidden on loading to avoid freeze.</p>
        <p>Grouped by type,run,image_id.</p>
        '''
               
def imageIdToGroup(imageId:int,step:int):
    s = imageId-imageId % step    
    return '{} to {}'.format(s,s+step)
    
    