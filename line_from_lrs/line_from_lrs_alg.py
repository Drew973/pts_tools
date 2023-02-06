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

from qgis.core import (QgsProcessingFeatureBasedAlgorithm,QgsProcessingParameterField,QgsFeature,
                       QgsProcessingParameterFeatureSource,QgsProcessing,QgsFeatureRequest,QgsWkbTypes,QgsProcessingParameterBoolean,
                       QgsPointXY,QgsGeometry,QgsPoint
)





networkLabelField = 'network_label_field'

network = 'network'

startLabelField = 'start_label_field'
startMeasureField = 'start_measure_field'
startOffsetField = 'start_offset_field'
endLabelField = 'end_label_field'
endMeasureField = 'end_measure_field'
endOffsetField = 'end_offset_field'
widthField = 'width'


class lineFromLrsAlg(QgsProcessingFeatureBasedAlgorithm):
      
    def initParameters(self, config):
         self.addParameter(QgsProcessingParameterField(startLabelField, 'Field with start id',parentLayerParameterName='INPUT'))
         self.addParameter(QgsProcessingParameterField(startMeasureField, 'Field with start measure', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='INPUT'))
         self.addParameter(QgsProcessingParameterField(startOffsetField, 'Field with start offset', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='INPUT', optional=True))
        
         self.addParameter(QgsProcessingParameterField(endLabelField, 'Field with end id',parentLayerParameterName='INPUT'))
         self.addParameter(QgsProcessingParameterField(endMeasureField, 'Field with end measure', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='INPUT'))
         self.addParameter(QgsProcessingParameterField(endOffsetField, 'Field with end offset', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='INPUT'))
         
         self.addParameter(
             QgsProcessingParameterFeatureSource(
                 name = network
                 ,description = 'Layer with LRS'
                 ,types = [QgsProcessing.TypeVectorLine]
             ))
         
         self.addParameter(QgsProcessingParameterField(networkLabelField, 'LRS field with id',parentLayerParameterName=network))
         



    def prepareAlgorithm(self,parameters,context,feedback):
        self.networkLayer = self.parameterAsVectorLayer(parameters,network,context)
        
        self.startLabelField = self.field(startLabelField,parameters,context)
        self.startMeasureField = self.field(startMeasureField,parameters,context)
        self.startOffsetField = self.field(startOffsetField,parameters,context)

        self.endLabelField = self.field(endLabelField,parameters,context)
        self.endMeasureField = self.field(endMeasureField,parameters,context)
        self.endOffsetField = self.field(endOffsetField,parameters,context)

        self.networkLabelField = self.field(networkLabelField,parameters,context)

        self.widthField = self.field(widthField,parameters,context)

        return True
    
    
    #parameterAsFields returns [] if field not set by user.
    def field(self,name, parameters, context):
        p = self.parameterAsFields(parameters,name,context)
        if len(p)>0:
            return p[0]  
    
    
    #crap documentation for this. QgsProcessing enum seems to be working.
    def inputLayerTypes(self):
        return [QgsProcessing.TypeVector]
        
    
    def networkGeom(self,label,feedback):
        if isinstance(label,str):
            label = "'{lab}'".format(lab=label)
        req = QgsFeatureRequest()
        req.setFilterExpression('{labelField} = {lab}'.format(labelField = self.networkLabelField,lab = label))
        nf = [f.geometry() for f in self.networkLayer.getFeatures(req)]
       
        if len(nf)==1:
            return nf[0]
       
        if len(nf)>1:
          #  print('multiple network features with {f} = {lab}'.format(f=self.networkLabelField,lab =label ))
            feedback.reportError('multiple network features with {f} = {lab}'.format(f=self.networkLabelField,lab =label ),fatalError = False)
            
        if len(nf)==0:
          #  print('no network features with {f} = {lab}'.format(f=self.networkLabelField,lab =label ))
            feedback.reportError('no network features with {f} = {lab}'.format(f=self.networkLabelField,lab =label ),fatalError = False)
       


  # def processFeature(self, feature: QgsFeature, context: QgsProcessingContext, feedback: QgsProcessingFeedback) → object
    def processFeature(self, feature, context, feedback):
        
        startLabel = feature[self.startLabelField]
        startGeom = self.networkGeom(startLabel,feedback)
        
        if startGeom is not None:
            
            startMeasure = feature[self.startMeasureField]        
            startOffset = feature[self.startOffsetField]        
        
            if self.endLabelField:
                endLabel = feature[self.endLabelField]
            else:
                endLabel = startLabel
    
            endMeasure = feature[self.endMeasureField]        
            endOffset = feature[self.endOffsetField]        
    
            g = QgsGeometry()
            
            endGeom = self.networkGeom(endLabel,feedback)
            newFeat = QgsFeature()
            newFeat.setAttributes(feature.attributes())             
    
            
            if startLabel == endLabel and self.makeRectangle:
                p0 = interpolatePoint(startGeom,startMeasure,startOffset)#start
                p1 = interpolatePoint(startGeom,endMeasure,startOffset)
                p2 = interpolatePoint(startGeom,endMeasure,endOffset)#end
                p3 = interpolatePoint(startGeom,startMeasure,endOffset)
                points = [QgsPointXY(p.x(),p.y()) for p in [p0,p1,p2,p3]]
                g = QgsGeometry.fromPolygonXY([points])                
                newFeat.setGeometry(g)
                return [newFeat]
            
            
            if endGeom is not None:
                s = interpolatePoint(startGeom,startMeasure,startOffset)#start
                e = interpolatePoint(endGeom,endMeasure,endOffset)#end
                g = QgsGeometry.fromPolyline([s,e])
                newFeat.setGeometry(g)
                return [newFeat]
                
            

            newFeat.setGeometry(g)
            print(newFeat.geometry())
            
            return [newFeat]
        return []
    
    
    def displayName(self):
        return 'Line from LRS'
    
    
    def name(self):
        return 'line_from_lrs'
    
    
    def createInstance(self):
        return lineFromLrsAlg()
    
    
    def outputName(self):
        return 'OUTPUT'
    
        
    def outputLayerType(self):
        return QgsProcessing.TypeVector
    
    
    def outputCrs(self,inputCrs):
        return self.networkLayer.crs()
        
    
    def outputWkbType(self,inputWkbType):
        return QgsWkbTypes.LineStringM|QgsWkbTypes.Polygon|QgsWkbTypes.Point



    def shortHelpString(self):
        return '''<html><body>
       
        <p>Sets geometry to linestringM using linear reference system.</p>
      
        <p>LRS layer needs to have linestring geometry with m values (LinestringM).</p>
        
        <p>If start and end in different sections then makes linestringM with 2 points.</p>

        <p>If start and end in same section and start offset = end offset returns linestringM between measures.</p>
        <p>Negative offset is to left.</p>


     
        '''