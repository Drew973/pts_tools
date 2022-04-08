# -*- coding: utf-8 -*-


__author__ = 'drew'
__date__ = '2022-27-01'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import csv

from PyQt5.QtCore import QVariant

from qgis.PyQt.QtCore import QCoreApplication


from qgis.core import QgsVectorLayer
from qgis.utils import iface

def copyLayer(layer):
	return QgsVectorLayer(layer.source(), layer.name(), layer.providerType())



from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterField,
                       QgsProcessingParameterString,
                       #QgsProcessingParameterFeatureSource,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterVectorLayer,
                       QgsField,
                       QgsExpression
                       )




#import logging# logging doesn't seem to work well with this
#import sys


'''


'''

class concatenateFieldsAlgorithm(QgsProcessingAlgorithm):
    
    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(QgsProcessingParameterVectorLayer(name = 'INPUT',description = self.tr('Input layer')))
        self.addOutput(QgsProcessingOutputVectorLayer(name = 'OUTPUT',description = self.tr('Output layer')))

        #field with group
        self.addParameter(QgsProcessingParameterField(name = 'FIELDS'
                                                      ,description = self.tr('Fields to combine')
                                                     ,parentLayerParameterName='INPUT'
                                                     ,allowMultiple=True
                                                      ))
                                                 
                                                 
        self.addParameter(QgsProcessingParameterString(name = 'FIELDNAME'
                                                      ,description = self.tr('Name for new field')
                                                     ,defaultValue = 'combined'
                                                      ))

        self.addParameter(QgsProcessingParameterString(name = 'SEPERATOR'
                                                      ,description = self.tr('seperator')
                                                     ,defaultValue = '_'
                                                      ))        
        
        
    def prepareAlgorithm(self, parameters, context, feedback):
        self.layer = self.parameterAsVectorLayer(parameters, 'INPUT', context)#        layer2 = copyLayer(layer)
        self.fields = self.parameterAsFields(parameters,'FIELDS',context)
        self.fieldName = self.parameterAsString(parameters,'FIELDNAME',context)
        self.sep = self.parameterAsString(parameters,'SEPERATOR',context)
        return True

    def processAlgorithm(self, parameters, context, feedback):
        print(self.layer,self.fields,self.fieldName,self.sep)
        feedback.setProgress(0)
        addCombinedFields(layer=self.layer,fields=self.fields,sep=self.sep,name=self.fieldName)
        feedback.setProgress(1)
        
        return {'OUTPUT': self.layer.id()}


    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'concatenate_fields'


    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Concatenate fields')



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


    def createInstance(self):
        return concatenateFieldsAlgorithm()


    def helpUrl(self):
        help_path = os.path.join(os.path.dirname(__file__),'help','combine_fields.html')
        return 'file:/'+os.path.abspath(help_path)
        
        
    def shortHelpString(self):
        return '''Adds virtual field to layer. This will be a string containing concatenated fields and seperator.
        
        '''


    #adds virtual string field with fields seperated by sep
def addCombinedFields(layer,fields,sep='_',name='combined'):
    field = QgsField(name, QVariant.String )
    s = ','+QgsExpression.quotedString(sep)+','
    e = 'concat(%s)'%(s.join([QgsExpression.quotedColumnRef(f) for f in fields]))
    print(e)
    layer.addExpressionField( e, field )