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

from qgis.core import (QgsProcessingFeatureBasedAlgorithm,QgsProcessingParameterField,QgsFeature,
                       QgsProcessingParameterFeatureSource,QgsProcessing,QgsFeatureRequest,QgsWkbTypes,
                       )

from pts_tools.shared_functions.geometry_functions import interpolatePoint,otherCorners



networkLabelField = 'network_label_field'
network = 'network'
startLabelField = 'start_label_field'
startMeasureField = 'start_measure_field'
startOffsetField = 'start_offset_field'
endLabelField = 'end_label_field'
endMeasureField = 'end_measure_field'
endOffsetField = 'end_offset_field'
widthField = 'width'



class loadVcsAlg(QgsProcessingFeatureBasedAlgorithm):
      
    def initParameters(self, config):
        
        #delimited text fields treated as str until loaded into QGIS.
        
         self.addParameter(QgsProcessingParameterField(startLabelField, 'Field with start id',parentLayerParameterName='INPUT',defaultValue='start Section ID'))
       #  self.addParameter(QgsProcessingParameterField(startMeasureField, 'Field with start measure', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='INPUT'))
         self.addParameter(QgsProcessingParameterField(startMeasureField, 'Field with start measure', parentLayerParameterName='INPUT',defaultValue  ='start chainage (m)'))

        # self.addParameter(QgsProcessingParameterField(startOffsetField, 'Field with start offset', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='INPUT', optional=True))
         self.addParameter(QgsProcessingParameterField(startOffsetField, 'Field with start offset', parentLayerParameterName='INPUT', optional=True,defaultValue  ='start offset (m)'))

         self.addParameter(QgsProcessingParameterField(endLabelField, 'Field with end id',parentLayerParameterName='INPUT',defaultValue='end Section ID'))
         self.addParameter(QgsProcessingParameterField(endMeasureField, 'Field with end measure', parentLayerParameterName='INPUT',defaultValue  ='end chainage (m)'))
         self.addParameter(QgsProcessingParameterField(endOffsetField, 'Field with end offset', parentLayerParameterName='INPUT',optional=True,defaultValue  ='end offset (m)'))
         
         self.addParameter(QgsProcessingParameterField(widthField, 'Field with width', parentLayerParameterName='INPUT',defaultValue ='Width(m)'))

         
         
         self.addParameter(
             QgsProcessingParameterFeatureSource(
                 name = network
                 ,description = 'Layer with LRS'
                 ,types = [QgsProcessing.TypeVectorLine]
             ))
         
         self.addParameter(QgsProcessingParameterField(networkLabelField, 'LRS field with id',parentLayerParameterName=network))
         



    def prepareAlgorithm(self,parameters,context,feedback):
        self.networkLayer = self.parameterAsVectorLayer(parameters,network,context)
        
        if not QgsWkbTypes.hasM(self.networkLayer.wkbType()):
            #raise TypeError('LRS geometry needs M values')
            feedback.reportError('LRS geometry needs M values',fatalError=True)
            return False
        
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
            raise KeyError('multiple network features with {f} = {lab}'.format(f=self.networkLabelField,lab =label ))
            
        if len(nf)==0:
          #  print('no network features with {f} = {lab}'.format(f=self.networkLabelField,lab =label ))
            #feedback.reportError('no network features with {f} = {lab}'.format(f=self.networkLabelField,lab =label ),fatalError = False)
            raise KeyError('no network features with {f} = {lab}'.format(f=self.networkLabelField,lab =label ))


  # def processFeature(self, feature: QgsFeature, context: QgsProcessingContext, feedback: QgsProcessingFeedback) → object
    def processFeature(self, feature, context, feedback):
        
        try:
            
            if self.startOffsetField:
                startOffset = float(feature[self.startOffsetField])
            else:
                startOffset = 0
                
            startMeasure = float(feature[self.startMeasureField])
                
            startGeom = self.networkGeom(feature[self.startLabelField],feedback)
            s = interpolatePoint(startGeom,startMeasure,startOffset)
                    
            if self.endOffsetField:
                endOffset = float(feature[self.endOffsetField])
            else:
                endOffset = 0
        
            endGeom = self.networkGeom(feature[self.endLabelField],feedback)
            endMeasure = float(feature[self.endMeasureField])
    
            e = interpolatePoint(endGeom,endMeasure,endOffset)
    
    
            width = float(feature[self.widthField])
    
    
            newFeat = QgsFeature()
            newFeat.setAttributes(feature.attributes())
            newFeat.setGeometry(otherCorners(s,e,width,startLeft=True))
            
            return [newFeat]
         
        except Exception as e:
            feedback.reportError(str(e),fatalError = False)
            return []
     
    
    def displayName(self):
        return 'Load VCS'
    
    
    def name(self):
        return 'load_vcs'
    
    
    def createInstance(self):
        return loadVcsAlg()
    
    
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
       
        <p>Creates polygon layer from distress data and linear reference system.</p>
        <p>LRS layer needs to have linestringM geometry. m values can be added with PTS tools:add_measure.</p>
        <p>Negative offset is to left.</p>

        <p>Much faster when LRS is indexed on label field.</p>


        </body>
        </html>
        '''