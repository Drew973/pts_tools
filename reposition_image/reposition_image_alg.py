
from qgis.core import (QgsProcessingAlgorithm,QgsCoordinateReferenceSystem,
                       QgsProcessingMultiStepFeedback,QgsProcessingParameterRasterDestination,QgsProcessingContext,
QgsProcessingParameterRasterLayer,QgsProcessingParameterPoint)

from qgis import processing



class repositionImage(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        
        self.addParameter(QgsProcessingParameterRasterLayer('inputLayer','Raster image to reposition'))
        self.addParameter(QgsProcessingParameterRasterDestination('OUTPUT','output file',createByDefault=True),createOutput=True)
        self.addParameter(QgsProcessingParameterPoint('topLeft','Position for top left of image'))
        self.addParameter(QgsProcessingParameterPoint('topRight','Position for top right of image'))
        self.addParameter(QgsProcessingParameterPoint('bottomLeft','Position for bottom left of image'))
        self.addParameter(QgsProcessingParameterPoint('bottomRight','Position for bottom right of image'))
        


#output layer only gets loaded with self.parameterAsOutputLayer
    def prepareAlgorithm(self, parameters, context, feedback):
        self.crs = QgsCoordinateReferenceSystem('ESPG:27700')
        #points will be reprojected to this
        
        self.layer = self.parameterAsRasterLayer(parameters,'inputLayer',context)
        self.dest = self.parameterAsOutputLayer(parameters,'OUTPUT',context)
        self.topLeft = self.parameterAsPoint(parameters,'topLeft',context,self.crs) #QgsPointXy
        self.topRight = self.parameterAsPoint(parameters,'topRight',context,self.crs) #QgsPointXy
        self.bottomLeft = self.parameterAsPoint(parameters,'bottomLeft',context,self.crs) #QgsPointXy
        self.bottomRight = self.parameterAsPoint(parameters,'bottomRight',context,self.crs) #QgsPointXy

        return True



    def processAlgorithm(self, parameters, context, feedback):
        
        feedback = QgsProcessingMultiStepFeedback(2, feedback)

        params = {'EXTRA' : '--config GTIFF_WRITE_TOWGS84 NO -of GTiff -co PROFILE=BASELINE', 'INPUT' : self.layer,'TARGET_CRS' : 'ESPG:27700','OUTPUT':'TEMPORARY_OUTPUT'}
        r = processing.run('gdal:translate',params,context=context,feedback=feedback,is_child_algorithm=True)
       
        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
        
        #invalid command will cause layer to not load.
        s = '-gcp 0 0 {tlx} {tly} -gcp {w} 0 {trx} {tr} -gcp 0 {h} {blx} {bly} -gcp {w} {h} {brx} {bry} -a_srs EPSG:27700'
        s = s.format(w=self.layer.width(),h=self.layer.height(),tlx=self.topLeft.x(),tly=self.topLeft.y(),
                     trx=self.topRight.x(),tr=self.topRight.y(),blx=self.bottomLeft.x(),bly=self.bottomLeft.y(),
                     brx=self.bottomRight.x(),bry=self.bottomRight.y())
        
        params = {'EXTRA' : s, 'INPUT' : r['OUTPUT'],'TARGET_CRS' : 'ESPG:27700','OUTPUT':self.dest }
        r = processing.run('gdal:translate',params,context=context,feedback=feedback,is_child_algorithm=True)
        
        
        
        #without this layer is loaded with processing.runAndLoadResults but not through gui. Don't know why.       
        details = QgsProcessingContext.LayerDetails('repositioned',context.project(),'OUTPUT')
        context.addLayerToLoadOnCompletion(r['OUTPUT'],details)
    
        return {'OUTPUT':self.dest}


    def name(self):
        return 'reposition_image'


    def displayName(self):
        return 'Reposition image'


    def group(self):
        return 'PTS tools'


    def groupId(self):
        return ''


    def createInstance(self):
        return repositionImage()


    def shortHelpString(self):
        return r'''<html><body>
        <p>reposition raster layer by specifying corners. </p>
        
        </body></html>
        '''
        
