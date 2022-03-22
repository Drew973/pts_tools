
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingParameterFile,QgsProcessingOutputMultipleLayers
from qgis.core import QgsProcessingParameterNumber
import os
import csv


FORMATS = ['.sec','.sr','.rte']


FIELDS = ['label','direction','length','startNode','endNode','startDate','endDate','function']


class loadRasters(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        
        self.addParameter(QgsProcessingParameterFile('input', 'csv with ImageType,FileName,FilePath'))
        self.addOutput(QgsProcessingOutputMultipleLayers('outputs','Output layers'))
        self.addParameter(QgsProcessingParameterNumber('max', 'maximum number of images to load',minValue=1,optional=True))



    def prepareAlgorithm(self, parameters, context, feedback):
        self.file = self.parameterAsFile(parameters,'input',context)
        self.max = self.parameterAsNumber(parameters,'max',context)
        self.outputLayers = []
        return True



    def processAlgorithm(self, parameters, context, feedback):
        n = len(self.files)
        
        feedback.setProgress(0)
        
        groups = []
        names = []
        files = []
    
        
        with open(self.file,'r') as f:
            reader = csv.DictReader(f)
            for i,r in enumerate(reader):
                groups.append(r['ImageType'])
                names.append(r['FileName'])
                files.append(r['FilePath'])

                if not self.max is None:
                    if i>self.max:
                        break

        print(groups,names,files)
        
        for i,file in enumerate(files):            
            feedback.setProgress(100*i/n)
            self.loadImage(groups[i],names[i],files[i])
            
        return {'outputs':self.outputLayers}


  
    def loadImage(self,group,name,file):
        layer = None
        self.outputLayers.append(layer)



    def name(self):
        return 'load_images'


    def displayName(self):
        return 'Load MFV images'


    def group(self):
        return 'PTS tools'


    def groupId(self):
        return ''


    def createInstance(self):
        return loadRasters()


    def shortHelpString(self):
        return r'''<html><body>
        <p>Loads images as raster layers given  
         csv with ImageType,FileName,FilePath. Finds and loads these. </p>
        
        </body></html>
        '''
        
