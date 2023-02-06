# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 08:02:43 2023


@author: Drew.Bennett


TODO:
    sides of rectangle should be offset to linestring. NOT RECTANGLE.
    distresses can be hundreds of meters long.
    width field irrelevant.
    
    
    
    probabaly easier as QgsProcessingAlgorithm
    
    
    iterate through input in order of section.
    only need to look up network geom and make offsets when different to last input.
    
    rename to polygon_from _lrs?
    
    


"""

from qgis.core import (QgsProcessingAlgorithm,QgsProcessingParameterField,QgsFeature,
                       QgsProcessingParameterFeatureSource,QgsProcessing,QgsFeatureRequest,QgsWkbTypes,
                       QgsProcessingParameterFeatureSink,QgsGeometry,QgsPointXY
                       )

from pts_tools.shared_functions.geometry_functions import betweenMeasures



networkLabelField = 'network_label_field'
network = 'network'
startLabelField = 'start_label_field'
startMeasureField = 'start_measure_field'
startOffsetField = 'start_offset_field'
#endLabelField = 'end_label_field'
endMeasureField = 'end_measure_field'
endOffsetField = 'end_offset_field'
widthField = 'width'



class polygonFromLrsAlg(QgsProcessingAlgorithm):
      
    def initAlgorithm(self, config=None):
        
        #delimited text fields treated as str until loaded into QGIS.
        
         self.addParameter(QgsProcessingParameterFeatureSource('INPUT', 'Layer with data', types=[QgsProcessing.TypeVector], defaultValue=None))
         self.addParameter(QgsProcessingParameterField(startLabelField, 'Field with start id',parentLayerParameterName='INPUT',defaultValue='start Section ID'))
       #  self.addParameter(QgsProcessingParameterField(startMeasureField, 'Field with start measure', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='INPUT'))
         self.addParameter(QgsProcessingParameterField(startMeasureField, 'Field with start measure', parentLayerParameterName='INPUT',defaultValue  ='start chainage (m)'))
         self.addParameter(QgsProcessingParameterField(startOffsetField, 'Field with start offset', parentLayerParameterName='INPUT',defaultValue  ='start offset (m)'))
         self.addParameter(QgsProcessingParameterField(endMeasureField, 'Field with end measure', parentLayerParameterName='INPUT',defaultValue  ='end chainage (m)'))
         self.addParameter(QgsProcessingParameterField(endOffsetField, 'Field with end offset', parentLayerParameterName='INPUT',defaultValue  ='end offset (m)'))
         
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
    
          #  self.endLabelField = self.field(endLabelField,parameters,context)
            self.endMeasureField = self.field(endMeasureField,parameters,context)
            self.endOffsetField = self.field(endOffsetField,parameters,context)
    
            self.networkLabelField = self.field(networkLabelField,parameters,context)
                        
            self.sink,self.sinkId = self.parameterAsSink(parameters,'OUTPUT',context,
            fields = self.inputLayer.fields(),
            crs = self.networkLayer.crs(),
            geometryType = QgsWkbTypes.Polygon)
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
        
        r = QgsFeatureRequest()
        r = r.addOrderBy('"{}"'.format(self.startLabelField))
        i = 1

        
        lastLab = None
        geom = QgsGeometry()



        #order by label. only need to look up geom once this way.
        for f in self.inputLayer.getFeatures(r):
            
            
          #  print(f[self.startLabelField])
            lab = f[self.startLabelField]
          
            if f[self.startLabelField] != lastLab:
                
                try:
                    geom = self.networkGeom(lab)
                    
                    
                except Exception as e:
                    print(e)
                    feedback.reportError(str(e),fatalError = False)
                    geom = QgsGeometry()
                lastLab = lab
           #     print(lab)
                
                
            if not geom.isEmpty():
                try:
                    s = float(f[self.startMeasureField])
                    e = float(f[self.endMeasureField])
                   # print('s',s,'e',e)
                    
                    points = []
                    shortened = betweenMeasures(geom,s,e)
                    shortened = QgsGeometry().fromPolylineXY(shortened.asPolyline())
                    
                    
                   # print('shortened',shortened)
                    
                    so = float(f[self.startOffsetField])
                    eo = float(f[self.endOffsetField])
                    
                  #  print('start offset',so)
                    
                    left = shortened.offsetCurve(distance=so,
                                                 segments=8,
                                                 joinStyle=QgsGeometry.JoinStyleRound,
                                                 miterLimit=1)
                    
                    #print('left',left)
                    
                    points += [v for v in left.vertices()]
                    
                    
                    right = shortened.offsetCurve(distance=eo,
                                          segments=8,
                                          joinStyle=QgsGeometry.JoinStyleRound,
                                          miterLimit=1)
                    
                    points += reversed([v for v in right.vertices()])
                    
                    if points:
                        points.append(points[0])
                        
                        
                        points = [QgsPointXY(pt.x(),pt.y()) for pt in points]
                        
                        #QgsGeometry.fromPolyline(points)
                    
                        newFeat = QgsFeature(f.fields())
                        newFeat.setAttributes(f.attributes())
                        newFeat.setGeometry(QgsGeometry.fromPolygonXY([points]))
                        self.sink.addFeature(newFeat)
              
                except Exception as e:
                        print(e)
                        feedback.reportError(str(e),fatalError = False)
                
            
            feedback.setProgress(100*i/count)
            i += 1
        
        return {'OUTPUT':self.sinkId}
        
    
    
    def displayName(self):
        return 'Polygon From LRS'
    
    
    def name(self):
        return 'polygon_from_lrs'
    
    
    def createInstance(self):
        return polygonFromLrsAlg()
    
    
    def outputName(self):
        return 'OUTPUT'
      #  return self.networkLayer.name()
    
    #->QgsProcessing.SourceType
    def outputLayerType(self):
        return QgsProcessing.TypeVectorPolygon
       # return QgsProcessing.TypeVectorAnyGeometry
    
    
    def outputCrs(self,inputCrs):
        return self.networkLayer.crs()
          
  
    def outputWkbType(self,inputWkbType):
        return QgsWkbTypes.Polygon


    def shortHelpString(self):
        return '''<html>
        <body>
       
        <p>Creates polygon layer from input and linear reference system.</p>
        <p>LRS layer needs to have linestringM geometry. M values can be added with PTS tools:add_measure.</p>
        <p>Negative offset is to right.</p>

        </body>
        </html>
        '''