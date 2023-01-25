# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 08:29:25 2023

@author: Drew.Bennett
"""

from qgis.core import QgsProcessingFeatureBasedAlgorithm,QgsProcessingParameterField,QgsFeature,QgsGeometry,QgsPoint,QgsWkbTypes,QgsProcessing


#add 
def addMeasure(geom,s,e):
    geomLen = geom.length()
    d = 0
    lastPt = None
    newPoints = []
    for pt in geom.vertices():
        if lastPt:
            d += lastPt.distance(pt)
        m = s+(e-s)*d/geomLen
        newPoints.append(QgsPoint(pt.x(),pt.y(),pt.z(),m=m))
        lastPt = pt
    return QgsGeometry.fromPolyline(newPoints)
    



startMeasureField = 'start_measure_field'
endMeasureField = 'end_measure_field'


class addMeasureAlg(QgsProcessingFeatureBasedAlgorithm):
      
    def initParameters(self, config):
         self.addParameter(QgsProcessingParameterField(startMeasureField, 'Field with start measure', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='INPUT', optional=True))
         self.addParameter(QgsProcessingParameterField('endMeasureField', 'Field with end measure', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='INPUT', optional=True))
        

    def prepareAlgorithm(self,parameters,context,feedback):
        self.startMeasureField = self.field(startMeasureField,parameters,context)
        self.endMeasureField = self.field(endMeasureField,parameters,context)
        return True
    
    
    #parameterAsFields returns [] if field not set by user.
    def field(self,name, parameters, context):
        p = self.parameterAsFields(parameters,name,context)
        if len(p)>0:
            return p[0]  
    
    
  # def processFeature(self, feature: QgsFeature, context: QgsProcessingContext, feedback: QgsProcessingFeedback) → object
    def processFeature(self, feature, context, feedback):
        
        #default to 0 if startMeasureField unspecified 
        #default to geom length if endMeasureField unspecified 
        
        if self.startMeasureField:
            s = feature[self.startMeasureField]
        else:
            s = 0
        
        if self.endMeasureField:
            e = feature[self.endMeasureField]
        else:
            e = feature.geometry().length()
     
        #newFeat = QgsFeature(feature)
        newFeat = QgsFeature()
        newFeat.setAttributes(feature.attributes())
        
        g = addMeasure(feature.geometry(),s,e)
       # print(g.asWkt())
        newFeat.setGeometry(g)
        return [newFeat]
    
    
    def displayName(self):
        return 'Add measure'
    
    
    def name(self):
        return 'add_measure'
    
    
    def createInstance(self):
        return addMeasureAlg()
    
    
    def outputName(self):
        return 'OUTPUT'
    
    
    def outputLayerType(self):
        return QgsProcessing.TypeVectorLine
        
    
    def outputWkbType(self,inputWkbType):
        if QgsWkbTypes.hasZ(inputWkbType):
            return QgsWkbTypes.LineStringZM
        else:
            return QgsWkbTypes.LineStringM
        
        
    def shortHelpString(self):
        return '''<html><body>
        <p>Adds or overwrites m values for each point of LineString geometry.</p>
        <p>M values are interpolated (using distance) between start measure and end measure.</p>
        <p>Start measure defaults to 0 and end measure to geometry length.</p>

        '''
    