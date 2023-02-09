# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 12:32:00 2023

@author: Drew.Bennett
"""

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
                       QgsProcessingParameterFeatureSink,QgsGeometry
                       )

from pts_tools.shared_functions.geometry_functions import interpolatePoint



networkLabelField = 'network_label_field'
network = 'network'
startLabelField = 'label_field'
startMeasureField = 'measure_field'
startOffsetField = 'offset_field'



class pointFromLrsAlg(QgsProcessingAlgorithm):
      
    def initAlgorithm(self, config=None):
        
        #delimited text fields treated as str until loaded into QGIS.
        
         self.addParameter(QgsProcessingParameterFeatureSource('INPUT', 'Layer with data', types=[QgsProcessing.TypeVector], defaultValue=None))
         self.addParameter(QgsProcessingParameterField(startLabelField, 'Field with section id',parentLayerParameterName='INPUT',defaultValue='section'))
         self.addParameter(QgsProcessingParameterField(startMeasureField, 'Field with measure', parentLayerParameterName='INPUT',defaultValue = 'chainage'))
         self.addParameter(QgsProcessingParameterField(startOffsetField, 'Field with offset', parentLayerParameterName='INPUT',defaultValue = '',optional=True))
         
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
        
            self.networkLabelField = self.field(networkLabelField,parameters,context)
                        
            self.sink,self.sinkId = self.parameterAsSink(parameters,'OUTPUT',context,
            fields = self.inputLayer.fields(),
            crs = self.networkLayer.crs(),
            geometryType = QgsWkbTypes.Point)
            return True


        except Exception as e:
            print(e)
            return False
       
    
    
    #parameterAsFields returns [] if field not set by user.
    def field(self,name, parameters, context):
        p = self.parameterAsFields(parameters,name,context)
        if len(p)>0:
            return p[0]  
    
    
    
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
                    print(e)
                    feedback.reportError(str(e),fatalError = False)
                    geom = QgsGeometry()
                lastLab = lab
           #     print(lab)
                
                
            if not geom.isEmpty():
                try:
                    s = float(f[self.startMeasureField])
                    if self.startOffsetField:
                        offset = float(f[self.startOffsetField])
                    else:
                        offset = 0

                    newFeat = QgsFeature(f.fields())
                    newFeat.setAttributes(f.attributes())
                    newFeat.setGeometry(interpolatePoint(geom,s,offset))
                    self.sink.addFeature(newFeat)
              
                except Exception as e:
                        print(e)
                        feedback.reportError(str(e),fatalError = False)
                
            
            feedback.setProgress(100*i/count)
            i += 1
        
        return {'OUTPUT':self.sinkId}
        
    
    
    def displayName(self):
        return 'Point from LRS'
    
    
    def name(self):
       # return 'point_from_lrs'
        return 'pointfromlrs'

    
    def groupId(self):
        return 'geometryfromlrs'    
        
    
    def group(self):
        return 'Geometry from LRS'
        
        
    def createInstance(self):
        return pointFromLrsAlg()
    

    def shortHelpString(self):
        return '''<html>
        <body>
       
        <p>Creates point layer from input and linear reference system.</p>
        <p>LRS layer needs to have linestringM geometry. M values can be added with PTS tools:add_measure.</p>
        <p>Negative offset is to right.</p>

        </body>
        </html>
        '''