# -*- coding: utf-8 -*-


__author__ = 'drew'
__date__ = '2021-09-09'
__copyright__ = '(C) 2021 by drew'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os


from qgis.PyQt.QtCore import QCoreApplication
from PyQt5.QtCore import QVariant


from qgis.core import (QgsProcessing,
                       QgsFeature,
                       QgsProcessingContext,
                       QgsFields,
                       QgsField,
                       QgsProcessingFeedback,
                       QgsProcessingFeatureBasedAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterField,
                       QgsProcessingParameterDistance,
                       QgsProcessingParameterBoolean,
                       )


from . import substring,split


#import logging# logging doesn't seem to work well with this

class splitByChainageAlgorithm(QgsProcessingFeatureBasedAlgorithm):


    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    #OUTPUT = 'OUTPUT'
    #INPUT = 'INPUT'
    #FIELD = None
    #STEP = 'step'
    
    
    def initParameters(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """


   

        self.addParameter(
            QgsProcessingParameterDistance(
                name = 'STEP'
                ,description = self.tr('step between start and end chainages. Negative for reverse direction.')
                ,defaultValue = 10.0
                ,parentParameterName = 'INPUT'#linked to crs of input
            )
        )
                                                      

        #field with section length
        self.addParameter(QgsProcessingParameterField(name = 'FIELD'
                                                      ,description = self.tr('Treat section length as this field. Same units as step.')
                                                      ,optional = True
                                                     ,parentLayerParameterName='INPUT'
                                                     ,type = QgsProcessingParameterField.Numeric
                                                      ))



#: : Dict[str, Any],QgsProcessingContext,QgsProcessingFeedback
    def prepareAlgorithm(self, parameters, context, feedback):
    
        fieldsParam = self.parameterAsFields({},'FIELD',context)
        
        self.includeSubsectionID = True

        #parameterAsString
        if fieldsParam:
            self.field = fieldsParam[0]
        else:
            self.field = None    

        if self.field is None:
            self.step = self.parameterAsDouble(parameters,'STEP',context)#converts to crs units.
        else:
            self.step = float(self.parameterAsString(parameters,'STEP',context))#unchanged spinbox value

        
        source = self.parameterAsSource(parameters, 'INPUT', context)
        self.sinkFields = self.outputFields(source.fields())
         #sinkProperties
           
        return True


    def processFeature(self, feature: QgsFeature, context: QgsProcessingContext, feedback: QgsProcessingFeedback):   
        

        if self.field is None:
            length = feature.geometry().length()
            scale = 1
        else:
            length = feature[self.field]
            scale = feature.geometry().length()/length
                
        #geometry chainage = geometry length*nominal chainage/nominal length
            
        atts = feature.attributes()  #feature.attributes() is slow
        
        fid = feature.id()
          
        def makeFeat(startChain,endChain,subsection):
            f = QgsFeature(self.sinkFields)
            extraAtts = [fid,float(startChain),float(endChain)]
            
            if self.includeSubsectionID:
                extraAtts.append(subsection)
            
            f.setAttributes(atts+extraAtts)
            f.setGeometry(substring.substring(feature.geometry(),startChain*scale,endChain*scale))
            return f
          
        return [makeFeat(startChain,endChain,subsect+1) for startChain,endChain,subsect in split.split(length=length,step=self.step)]
          
            
     
    
    def outputFields(self, inputFields):
        f = inputFields
        f.append(QgsField('source_id', QVariant.Int))
        f.append(QgsField('start_chainage', QVariant.Double))
        f.append(QgsField('end_chainage', QVariant.Double))
        
        if self.includeSubsectionID:
            f.append(QgsField('subsection_id', QVariant.Int))
        return f
    

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'split_by_chainage'


    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Split by chainage')



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
        return('split layer')


    def createInstance(self):
        return splitByChainageAlgorithm()


    def helpUrl(self):
        help_path = os.path.join(os.path.dirname(__file__),'help','split_by_chainage.html')
        return 'file:/'+os.path.abspath(help_path)
        
        
