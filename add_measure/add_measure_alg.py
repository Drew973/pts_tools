# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 08:29:25 2023

@author: Drew.Bennett
"""

from qgis.core import (QgsProcessingFeatureBasedAlgorithm,QgsProcessingParameterField,QgsFeature,QgsGeometry,QgsPoint,
QgsWkbTypes,QgsProcessing,QgsProcessingParameterNumber,QgsProcessingParameterExpression,QgsPropertyDefinition,QgsExpression)


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
       #  self.addParameter(QgsProcessingParameterField(startMeasureField, 'Field with start measure', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='INPUT', optional=True))
    #     self.addParameter(QgsProcessingParameterField('endMeasureField', 'Field with end measure', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='INPUT', optional=True))
        
        #QgsPropertyDefinition(name: str, description: str, type: QgsPropertyDefinition.StandardPropertyTemplate, origin: str = ‘’, comment: str = ‘’)
        #QgsPropertyDefinition(name: str, dataType: QgsPropertyDefinition.DataType, description: str, helpText: str, origin: str = ‘’, comment: str = ‘’) 
         #definition = QgsPropertyDefinition('','',QgsPropertyDefinition.Double, '', '') 
         #e#ndParam = QgsProcessingParameterNumber('number', 'Field with end measure', optional=True)
        # endParam.setIsDynamic(True)
        # endParam.setDynamicPropertyDefinition(definition)
       #  self.addParameter(endParam)
         
         self.addParameter(QgsProcessingParameterExpression('startMeasure', 'Start measure',parentLayerParameterName='INPUT',defaultValue = '0'))

         self.addParameter(QgsProcessingParameterExpression('endMeasure', 'End measure',parentLayerParameterName='INPUT',defaultValue = '$length'))

        

    def prepareAlgorithm(self,parameters,context,feedback):
        self.startMeasureField = self.field(startMeasureField,parameters,context)
        self.endMeasureField = self.field(endMeasureField,parameters,context)
        
        self.startMeasureExpression = QgsExpression(self.parameterAsExpression(parameters,'startMeasure',context))
        self.startMeasureExpression.prepare(context.expressionContext())
        
        if not self.startMeasureExpression.isValid():
            feedback.reportError('Start measure expression invalid',fatalError = True)
            return False
        
        self.endMeasureExpression = QgsExpression(self.parameterAsExpression(parameters,'endMeasure',context))
        self.endMeasureExpression.prepare(context.expressionContext())
        
        
        if not self.endMeasureExpression.isValid():
            feedback.reportError('End measure expression invalid',fatalError = True)
            return False
        
        return True
    
    
    #parameterAsFields returns [] if field not set by user.
    def field(self,name, parameters, context):
        p = self.parameterAsFields(parameters,name,context)
        if len(p)>0:
            return p[0]  
    
    
  # def processFeature(self, feature: QgsFeature, context: QgsProcessingContext, feedback: QgsProcessingFeedback) → object
    def processFeature(self, feature, context, feedback):

  
        try:
            s = self.startMeasureExpression.evaluate(context.expressionContext())

            if s is None:
                raise ValueError('Start measure expression evaluated to None.')
            s = float(s)
            
            e = self.endMeasureExpression.evaluate(context.expressionContext())
            print(e)
            if e is None:
                raise ValueError('End measure expression evaluated to None.')
            e = float(e)
            
        
            #newFeat = QgsFeature(feature)
            newFeat = QgsFeature()
            newFeat.setAttributes(feature.attributes())
            
            g = addMeasure(feature.geometry(),s,e)
           # print(g.asWkt())
            newFeat.setGeometry(g)
            return [newFeat]
    
    
        except Exception as e:
            feedback.reportError(repr(e),fatalError = False)
            return []
    
    
    def displayName(self):
        return 'Add measure'
    
    
    def name(self):
        return 'addmeasure'
    
    
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
        <p>Skips features where start/end measure could not be converted to float.</p>

        '''
    