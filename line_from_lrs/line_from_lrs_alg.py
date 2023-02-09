# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 15:07:23 2023

@author: Drew.Bennett
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 08:29:25 2023

@author: Drew.Bennett
"""





from qgis.core import (QgsProcessingAlgorithm,QgsProcessingParameterField,QgsFeature,
                       QgsProcessingParameterFeatureSource,QgsProcessing,QgsFeatureRequest,QgsWkbTypes,
                       QgsProcessingParameterFeatureSink,QgsGeometry,QgsPointXY
                       )

from pts_tools.shared_functions.geometry_functions import betweenMeasures



networkLabelField = 'network_label_field'
network = 'network'
startLabelField = 'label_field'
startMeasureField = 'start_measure_field'
startOffsetField = 'offset_field'
endMeasureField = 'end_measure_field'
endOffsetField = 'end_offset_field'



class lineFromLrsAlg(QgsProcessingAlgorithm):
      
    def initAlgorithm(self, config=None):
        
        #delimited text fields treated as str until loaded into QGIS.
        
         self.addParameter(QgsProcessingParameterFeatureSource('INPUT', 'Layer with data', types=[QgsProcessing.TypeVector], defaultValue=None))
         self.addParameter(QgsProcessingParameterField(startLabelField, 'Field with section id',parentLayerParameterName='INPUT',defaultValue='start Section ID'))
         self.addParameter(QgsProcessingParameterField(startMeasureField, 'Field with start measure', parentLayerParameterName='INPUT',defaultValue  ='start chainage (m)'))
         self.addParameter(QgsProcessingParameterField(endMeasureField, 'Field with end measure', parentLayerParameterName='INPUT',defaultValue  ='end chainage (m)'))
         self.addParameter(QgsProcessingParameterField(startOffsetField, 'Field with offset', parentLayerParameterName='INPUT',defaultValue  ='start offset (m)',optional=True))

         self.addParameter(
             QgsProcessingParameterFeatureSource(
                 name = network
                 ,description = 'Layer with LRS'
                 ,types = [QgsProcessing.TypeVectorLine]
             ))
         
         self.addParameter(QgsProcessingParameterField(networkLabelField, 'LRS field with id',parentLayerParameterName=network))
         
         self.addParameter(QgsProcessingParameterFeatureSink('OUTPUT', 'OUTPUT',type = QgsProcessing.TypeVectorPolygon))


    def prepareAlgorithm(self,parameters,context,feedback):
        try:
        
            self.inputLayer = self.parameterAsSource(parameters,'INPUT',context)
               
            self.networkLayer = self.parameterAsVectorLayer(parameters,network,context)            
            if not QgsWkbTypes.hasM(self.networkLayer.wkbType()):
                #raise TypeError('LRS geometry needs M values')
                feedback.reportError('LRS geometry needs M values',fatalError=True)
                return False
            
            self.startLabelField = self.field(startLabelField,parameters,context)
            self.startMeasureField = self.field(startMeasureField,parameters,context)
            self.startOffsetField = self.field(startOffsetField,parameters,context)
    
            self.endMeasureField = self.field(endMeasureField,parameters,context)
    
            self.networkLabelField = self.field(networkLabelField,parameters,context)
                        
            self.sink,self.sinkId = self.parameterAsSink(parameters,'OUTPUT',context,
            fields = self.inputLayer.fields(),
            crs = self.networkLayer.crs(),
            geometryType = QgsWkbTypes.LineStringM)
            return True


        except Exception as e:
            print(e)
            return False
            #self.sink,self.sinkId = (1,2)
       
       
     #  self.output = self.parameterAsOutputLayer(parameters,'OUTPUT',context)
        
#parameterAsSink
    
    
    #parameterAsFields returns [] if field not set by user.
    def field(self,name, parameters, context):
        p = self.parameterAsFields(parameters,name,context)
        if len(p)>0:
            return p[0]  
    
    
  #  #crap documentation for this. QgsProcessing enum seems to be working.
 #   def inputLayerTypes(self):
 #       return [QgsProcessing.TypeVector]
        
    
    def networkGeom(self,label):
        if isinstance(label,str):
            label = "'{lab}'".format(lab=label)
        req = QgsFeatureRequest()
        req.setFilterExpression('{labelField} = {lab}'.format(labelField = self.networkLabelField,lab = label))
        nf = [f.geometry() for f in self.networkLayer.getFeatures(req)]
       
        if len(nf)==1:
            return nf[0]
       
        if len(nf)>1:
          #  print('multiple network features with {f} = {lab}'.format(f=self.networkLabelField,lab =label ))
            #feedback.reportError('multiple network features with {f} = {lab}'.format(f=self.networkLabelField,lab =label ),fatalError = False)
            raise KeyError('multiple network features with {f} = {lab}'.format(f=self.networkLabelField,lab =label ))
            
        if len(nf)==0:
          #  print('no network features with {f} = {lab}'.format(f=self.networkLabelField,lab =label ))
            #feedback.reportError('no network features with {f} = {lab}'.format(f=self.networkLabelField,lab =label ),fatalError = False)
            raise KeyError('no network features with {f} = {lab}'.format(f=self.networkLabelField,lab =label ))



    def processAlgorithm(self,parameters,context,feedback):
        
        count = self.inputLayer.featureCount()
        r = QgsFeatureRequest().addOrderBy('"{}"'.format(self.startLabelField))
        i = 1
        lastLab = None
        geom = QgsGeometry()

        for f in self.inputLayer.getFeatures(r):        #order by label. only need to look up geom once this way.
            
          #  print(f[self.startLabelField])
            lab = f[self.startLabelField]
          
            if f[self.startLabelField] != lastLab:
                
                try:
                    geom = self.networkGeom(lab)
                    
                    
                except Exception as e:
                   # print(e)
                    feedback.reportError(str(e),fatalError = False)
                    geom = QgsGeometry()
                    #print(lab)
                lastLab = lab
              #  print(lab)
                
            #print(geom)#multiLinestringM
            if not geom.isEmpty():
                
                try:
                    s = float(f[self.startMeasureField])
                    e = float(f[self.endMeasureField])                    
                    
                    shortened = betweenMeasures(geom,s,e)
                    
                    if startOffsetField:
                        offset = float(f[self.startOffsetField])
                        g = shortened.offsetCurve(distance=offset,
                                                     segments=8,
                                                     joinStyle=QgsGeometry.JoinStyleRound,
                                                     miterLimit=1)   
                        
                    else:
                        offset = 0
                        g = shortened
                 
                   
                    newFeat = QgsFeature(f.fields())
                    newFeat.setAttributes(f.attributes())
                    newFeat.setGeometry(g)
                    self.sink.addFeature(newFeat)
              
                except Exception as e:
                       # print(repr(e))
                        feedback.reportError(repr(e),fatalError = False)
                
            
            feedback.setProgress(100*i/count)
            i += 1
        
        return {'OUTPUT':self.sinkId}
        
    
    def groupId(self):
        return 'geometryfromlrs'    
        
    
    def group(self):
        return 'Geometry from LRS'    
    
    def displayName(self):
        return 'Line from LRS'
    
    
    def name(self):
        return 'linefromlrs'
    
    
    def createInstance(self):
        return lineFromLrsAlg()
    

    def shortHelpString(self):
        return '''<html>
        <body>
       
        <p>Creates linestringM layer from input and linear reference system.</p>
        <p>Offset defaults to 0 if offset field unset. Negative offset is to right.</p>
        <p>LRS layer needs to have linestringM geometry. M(measure) values can be added with PTS tools:add_measure.</p>

        </body>
        </html>
        '''
