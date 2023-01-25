
from qgis.core import (QgsProcessingAlgorithm,QgsProcessingParameterFeatureSink, QgsWkbTypes,
                       QgsProcessingParameterFile,QgsCoordinateReferenceSystem)


from pts_tools.load_hsrr import parse_readings


#import os

#def filterFiles(folder,ext):
 #   res=[]
 #   for root, dirs, files in os.walk(folder):
 #       res+=[os.path.normpath(os.path.join(root,f)) for f in files if os.path.splitext(f)[-1]==ext]
 #   return res



class loadHsrr(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile('inputFile', 'File to load',fileFilter='xls(*.xls)',behavior= QgsProcessingParameterFile.File))
        self.addParameter(QgsProcessingParameterFeatureSink('OUTPUT'))
      #  self.addParameter(QgsProcessingParameterFeatureSink('OUTPUT','',type=QgsProcessing.TypeVectorLine,createByDefault=True,optional=True))



    def prepareAlgorithm(self, parameters, context, feedback):
        self.file = self.parameterAsFile(parameters,'inputFile',context)
        self.sink,self.destId =  self.parameterAsSink(parameters,'OUTPUT',context,parse_readings.fields,QgsWkbTypes.LineString,QgsCoordinateReferenceSystem("EPSG:27700"))
       # parameterAsLayer
        #self.outputFile = self.parameterAsFileOutput(parameters,'outputFile',context)
        return True



    def processAlgorithm(self, parameters, context, feedback):
        feedback.setProgress(0)
        self.sink.addFeatures(parse_readings.parseReadings(self.file))
        feedback.setProgress(100)
       # del self.sink
        return {'OUTPUT':self.destId}
  
    
    '''
    def makeFeature(self,startCh,endCh,rawCh,time,rl,startLat,startLon,endLat,endLon):
        f = QgsFeature(self.fields)
        f['start_ch'] = startCh
        f['end_ch'] = endCh
        f['raw_ch'] = rawCh
        f['time'] = time
        f['rl'] = rl
        g = QgsGeometry.fromPolylineXY([QgsPointXY(startLon,startLat),QgsPointXY(endLon,endLat)])
        g.transform(self.transform)
        f.setGeometry(g)
        return f
    '''
    
    def name(self):
        return 'load_hsrr'


    def displayName(self):
        return 'Load hsrr readings'


    def group(self):
        return 'PTS tools'


    def groupId(self):
        return ''


    def createInstance(self):
        return loadHsrr()


    def shortHelpString(self):
        return  r'''<html><body>
        
        <p>Loads hsrr spreadsheets to new layer. </p>
        
        </body></html>
        '''
        
     