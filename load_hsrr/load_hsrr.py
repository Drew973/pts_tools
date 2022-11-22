
from qgis.core import (QgsProcessing,QgsProcessingAlgorithm,QgsProcessingParameterFeatureSink,
                       QgsCoordinateTransform,QgsGeometry,QgsPointXY,QgsProject,QgsWkbTypes,
                       QgsProcessingParameterFile,QgsFields,QgsField,QgsFeature,QgsCoordinateReferenceSystem)

#from PyQt5.QtCore import QVariant
import os


from pts_tools.load_hsrr import parse_readings



def filterFiles(folder,ext):
    res=[]
    for root, dirs, files in os.walk(folder):
        res+=[os.path.normpath(os.path.join(root,f)) for f in files if os.path.splitext(f)[-1]==ext]
    return res



class loadHsrr(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile('inputFile', 'File to load',fileFilter='xls(*.xls)',behavior= QgsProcessingParameterFile.Folder))
       #self.addParameter(QgsProcessingParameterFeatureSink('OUTPUT',createByDefault=True,optional=True))
        self.addParameter(QgsProcessingParameterFeatureSink('OUTPUT','',type=QgsProcessing.TypeVectorLine,createByDefault=True,optional=True))



    def prepareAlgorithm(self, parameters, context, feedback):

        self.folder = self.parameterAsFile(parameters,'inputFile',context)
        
        self.files = filterFiles(self.folder,'.xls')
        
        '''
        self.inputFile = self.parameterAsFile(parameters,'inputFile',context)
       
        self.fields = QgsFields()
        self.fields.append(QgsField('start_ch',QVariant.Double))
        self.fields.append(QgsField('end_ch',QVariant.Double))
        self.fields.append(QgsField('raw_ch',QVariant.Double))
        self.fields.append(QgsField('time',QVariant.DateTime))
        self.fields.append(QgsField('rl',QVariant.Double))

        inputCrs = QgsCoordinateReferenceSystem("EPSG:4326")
        outputCrs = QgsCoordinateReferenceSystem("EPSG:27700")
        self.transform = QgsCoordinateTransform(inputCrs,outputCrs,QgsProject.instance())
        '''
        
        self.sink,self.destId =  self.parameterAsSink(parameters,'OUTPUT',context,parse_readings.fields,QgsWkbTypes.LineString,QgsCoordinateReferenceSystem("EPSG:27700"))

       # parameterAsLayer

        #self.outputFile = self.parameterAsFileOutput(parameters,'outputFile',context)
        return True



    def processAlgorithm(self, parameters, context, feedback):
        
        for i,file in enumerate(self.files):
            self.sink.addFeatures(parse_readings.parseReadings(file))
            feedback.setProgress(i*100/len(self.files))
    
        del self.sink
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
        
     