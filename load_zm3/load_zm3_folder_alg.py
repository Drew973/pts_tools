# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 07:28:18 2024

@author: Drew.Bennett
"""

import glob
from os import path
from qgis.core import QgsVectorLayer,QgsProject, QgsProcessingContext


def layerFromZm3(file):
    uri = r'file:///{file}?&useHeader=no&xField={xField}&yField={yField}&zField={zField}&mField={mField}&crs={crs}'
    uri = uri.format( file = file,
                     crs = 'EPSG:27700',
                     xField = 'field_2',
                     yField = 'field_3',
                     zField = 'field_4',
                     mField ='field_1')
    layerName = path.splitext(path.basename(file))[0]#filename without extension
    return QgsVectorLayer(uri, layerName, "delimitedtext")



from qgis.core import QgsProcessingAlgorithm, QgsProcessingParameterFile, QgsProcessingOutputMultipleLayers


class loadZm3FolderAlg(QgsProcessingAlgorithm):
      
         
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile(name = 'folder',description = 'Folder to load',behavior = QgsProcessingParameterFile.Folder))
        self.addOutput(QgsProcessingOutputMultipleLayers(name = 'OUTPUT',description = 'output layers'))

    def prepareAlgorithm(self,parameters,context,feedback):
        self.folder = self.parameterAsFile(parameters,'folder',context)
        return True
    

    def processAlgorithm(self, parameters, context, feedback):
        pattern = self.folder + r'\**\*.zm3'
        files = [f for f in glob.glob(pattern,recursive = True)]
      #  print('files',files)
        ids = []
        self.layers = []
        for i,f in enumerate(files):
            layer = layerFromZm3(f)
            context.temporaryLayerStore().addMapLayer(layer)
            details = QgsProcessingContext.LayerDetails(layer.name(), context.project(), layer.name())
            details.forceName = True
            context.addLayerToLoadOnCompletion(layer.id(), details)
            ids.append(layer.id())
            self.layers.append(layer)
            feedback.setProgress(100*i/len(files))
        return {'OUTPUT':ids}
    
    #documentation says manually loading layers like this is bad practice. works though.
  #  def postProcessAlgorithm(self, context, feedback):
      #  QgsProject.instance().addMapLayers(self.layers)
    #    return {'OUTPUT':self.layers}

    def displayName(self):
        return 'Load zm3 folder'
    
    
    def name(self):
        return 'loadzm3folder'
    
    
    def groupId(self):
        return ''    
        
    
    def group(self):
        return ''
    
    
    def createInstance(self):
        return loadZm3FolderAlg()
    


    def shortHelpString(self):
        return '''<html>
        <body>
       
        <p>Loads all zm3 files in folder</p>

        </body>
        </html>
        '''