# -*- coding: utf-8 -*-


__author__ = 'drew'
__date__ = '2021-09-09'
__copyright__ = '(C) 2021 by drew'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


from qgis.PyQt.QtCore import QCoreApplication
from PyQt5.QtCore import QVariant
import numpy as np


from qgis.core import (QgsProcessing,
                       QgsFeature,
                       QgsProcessingContext,
                       QgsField,
                       QgsProcessingFeedback,
                       QgsProcessingFeatureBasedAlgorithm,
                       QgsProcessingParameterField,
                       QgsProcessingParameterDistance,
                       QgsWkbTypes

                       )


from pts_tools.curvature import section_interpolator


#import logging# logging doesn't seem to work well with this

class estimateCurvatureAlg(QgsProcessingFeatureBasedAlgorithm):

  
    def initParameters(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(QgsProcessingParameterDistance(
                name = 'spacing'
                ,description = self.tr('calculate curvature every:')
                ,defaultValue = 5
                ,parentParameterName = 'INPUT'#linked to crs of input
            ))


        #field with section length
        self.addParameter(QgsProcessingParameterField(name = 'lengthField'
                                                      ,description = self.tr('Treat section length as this field.')
                                                      ,optional = True
                                                     ,parentLayerParameterName='INPUT'
                                                     ,type = QgsProcessingParameterField.Numeric
                                                      ))



    def outputLayerType(self):
        return QgsProcessing.TypeVectorPoint

    def outputWkbType(self,inputWkbType):
        return QgsWkbTypes.Point 


    def inputLayerTypes(self):
        return [QgsProcessing.TypeVectorLine]
        
        
    def prepareAlgorithm(self, parameters, context, feedback):
    
        self.lengthField = self.field('lengthField',parameters,context)      

        self.spacing = self.parameterAsDouble(parameters,'spacing',context)#converts to crs units.

        
        source = self.parameterAsSource(parameters, 'INPUT', context)
        self.sinkFields = self.outputFields(source.fields())
         #sinkProperties
           
        return True


    def field(self,name, parameters, context):
        p = self.parameterAsFields(parameters,name,context)
        if len(p)>0:
            return p[0]


   # def processFeature(self, feature: QgsFeature, context: QgsProcessingContext, feedback: QgsProcessingFeedback):   
    def processFeature(self, feature, context, feedback):   

        i = section_interpolator.sectionHandler(feature.geometry())
        
        if i.enoughPoints():#may not have enough points in geometry to calculate curvatures
        
            atts = feature.attributes()#slow
            
            if self.lengthField is None:
                scale = 1
                length = i.geomLength
            else:
                scale = feature[self.lengthField]/feature.geometry().length()
                length = feature[self.lengthField]
            
            
            chainages = np.arange(0,length,self.spacing)
            distances = np.arange(0,i.geomLength,self.spacing*scale)
            
            points = i.points(distances)  
            radi = i.radi(distances)         

            return [self.makeFeat(atts,ch,radi[i],points[i]) for i,ch in enumerate(chainages)]
        
        
        else:
            return []
          
            

    
    def outputFields(self, inputFields):
        f = inputFields
        f.append(QgsField('chainage', QVariant.Double))
        f.append(QgsField('roc', QVariant.Double))

        return f
    

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'estimatecurvature'


    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Estimate curvature')



    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return 'Curvature'


    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'curvature'


    def tr(self, string):
        return QCoreApplication.translate('Processing', string)


    def outputName(self):
        return('Estimate curvature')


    def createInstance(self):
        return estimateCurvatureAlg()

		
    def shortHelpString(self):
        return '''<html><body>
        <p>Makes layer with points and estimated curvature at specified interval. </p>
        '''
        
        
        
    def makeFeat(self,atts,chainage,radius,point):
        f = QgsFeature(self.sinkFields)
        f.setAttributes(atts+[float(chainage),float(radius)])
        f.setGeometry(point)
        return f 