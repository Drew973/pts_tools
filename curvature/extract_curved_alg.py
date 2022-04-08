# -*- coding: utf-8 -*-


__author__ = 'drew'
__date__ = '2021-09-09'
__copyright__ = '(C) 2021 by drew'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


from qgis.PyQt.QtCore import QCoreApplication
from PyQt5.QtCore import QVariant


from qgis.core import (QgsProcessing,
                       QgsFeature,
                       QgsProcessingContext,
                       QgsField,
                       QgsProcessingFeedback,
                       QgsProcessingFeatureBasedAlgorithm,
                       QgsProcessingParameterField,
                       QgsProcessingParameterDistance,
                       )


from pts_tools.curvature import section_interpolator
from pts_tools.shared_functions import substring


#import logging# logging doesn't seem to work well with this

class extractCurvedAlg(QgsProcessingFeatureBasedAlgorithm):

  
    def initParameters(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(QgsProcessingParameterDistance(
                name = 'resolution'
                ,description = self.tr('Resolution. Smaller values will take longer to process.')
                ,defaultValue = 5
                ,parentParameterName = 'INPUT'#linked to crs of input
            ))
                                                      

        self.addParameter(
            QgsProcessingParameterDistance(
                name = 'threshold'
                ,description = self.tr('Extract parts with radius of curvature <')
                ,defaultValue = 500
                ,parentParameterName = 'INPUT'#linked to crs of input
            ))


        #field with section length
        self.addParameter(QgsProcessingParameterField(name = 'lengthField'
                                                      ,description = self.tr('Treat section length as this field.')
                                                      ,optional = True
                                                     ,parentLayerParameterName='INPUT'
                                                     ,type = QgsProcessingParameterField.Numeric
                                                      ))



    def prepareAlgorithm(self, parameters, context, feedback):
    
        self.lengthField = self.field('lengthField',parameters,context)      

        self.resolution = self.parameterAsDouble(parameters,'resolution',context)#converts to crs units.
        self.threshold = self.parameterAsDouble(parameters,'threshold',context)#converts to crs units.

        
        source = self.parameterAsSource(parameters, 'INPUT', context)
        self.sinkFields = self.outputFields(source.fields())
         #sinkProperties
           
        return True


    def inputLayerTypes(self):
        return [QgsProcessing.TypeVectorLine]
        
    #def outputLayerType(self):
  #      return QgsProcessing.TypeVectorLine

   # def outputWkbType(self,inputWkbType):
   #     return QgsWkbTypes.Line 
        
        
    def field(self,name, parameters, context):
        p = self.parameterAsFields(parameters,name,context)
        if len(p)>0:
            return p[0]


    def processFeature(self, feature: QgsFeature, context: QgsProcessingContext, feedback: QgsProcessingFeedback):   

        
        
        
        i = section_interpolator.sectionHandler(feature.geometry())
        
        if i.enoughPoints():#may not have enough points in geometry to calculate curvatures
        
            atts = feature.attributes()#slow
            
            if self.lengthField is None:
                scale = 1
            else:
                scale = feature[self.lengthField]/feature.geometry().length()
            
            ranges = i.radiLessThan(self.threshold,self.resolution)
                        
                        
            return [self.makeFeat(atts,feature.geometry(),r[0],r[1],scale) for r in ranges]
        
        
        else:
            return []
          
            

    
    def outputFields(self, inputFields):
        f = inputFields
        f.append(QgsField('start_chainage', QVariant.Double))
        f.append(QgsField('end_chainage', QVariant.Double))
        return f
    

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'extract_curved'


    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Extract curved')



    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())


    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return ''


    def tr(self, string):
        return QCoreApplication.translate('Processing', string)


    def outputName(self):
        return('Extract curved')


    def createInstance(self):
        return extractCurvedAlg()

		
    def shortHelpString(self):
        return '''<html><body>
        <p>Estimates curvature at distances seperated by resolution along linestring.</p>
        <p>Extracts parts with radius of curvature less than threshold.</p>
        <p>Works feature by feature.</p>

        '''
        
        
        
    def makeFeat(self,atts,geometry,startChain,endChain,scale):
        f = QgsFeature(self.sinkFields)
        f.setAttributes(atts+[float(startChain*scale),float(endChain*scale)])
        f.setGeometry(substring.substring(geometry,startChain,endChain))
        return f 