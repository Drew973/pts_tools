
__author__ = 'drew'
__date__ = '2021-09-09'
__copyright__ = '(C) 2021 by drew'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


import os
import math

from PyQt5.QtCore import QVariant


from qgis.PyQt.QtCore import QCoreApplication


from qgis.core import (QgsProcessing, QgsFeatureSink, QgsProcessingAlgorithm,QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,QgsProcessingParameterField,QgsProcessingParameterDistance,QgsField,
    QgsSpatialIndex,QgsFeature,QgsFeatureRequest,QgsCoordinateTransform,QgsProject,QgsGeometry,QgsRectangle)


#import logging# logging doesn't seem to work well with this
#import sys




class pointToChainageAlgorithm(QgsProcessingAlgorithm):


    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    #OUTPUT = 'OUTPUT'
    #INPUT = 'INPUT'
    #FIELD = None
    #STEP = 'step'
    
    
    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """


        self.addParameter(
            QgsProcessingParameterFeatureSource(
                #self.INPUT,
                name = 'INPUT'
                ,description = self.tr('Input layer')
                ,types = [QgsProcessing.TypeVectorPoint]
            ))


        self.addParameter(
            QgsProcessingParameterFeatureSource(
                #self.INPUT,
                name = 'NETWORK'
                ,description = self.tr('Layer or data source with network')
                ,types = [QgsProcessing.TypeVectorLine]
                ,defaultValue=r'L:\SharedDocs\HAPMS shapefile\latest_network.shp'))
            


        #field with section length
        self.addParameter(QgsProcessingParameterField(name = 'LABEL FIELD'
                                                      ,description = self.tr('Field with section label.')
                                                      ,optional = False
                                                     ,parentLayerParameterName='NETWORK'
                                                      ,defaultValue='sect_label')
                                                      )
                                                      


        self.addParameter(QgsProcessingParameterDistance(
                name = 'TOLERANCE'
                ,description = self.tr('Maximum distance')
                ,defaultValue = 20.0
                ,parentParameterName = 'NETWORK'#linked to crs of input
                ))



        #field with section length
        self.addParameter(QgsProcessingParameterField(name = 'LENGTH FIELD'
                                                      ,description = self.tr('Treat section length as this field.')
                                                      ,optional = True
                                                     ,parentLayerParameterName='NETWORK'
                                                     ,type = QgsProcessingParameterField.Numeric
                                                     ,defaultValue='sec_length')
                                                      )


        self.addParameter(
            QgsProcessingParameterFeatureSink(
                name = 'OUTPUT'
                ,description = 'Output layer'
            ))


        

    def processAlgorithm(self, parameters, context, feedback):

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        source = self.parameterAsSource(parameters, 'INPUT', context)
        
        fields = source.fields()
        fields.append(QgsField('section', QVariant.String))
        fields.append(QgsField('chainage', QVariant.Double))
        
        
        (sink, dest_id) = self.parameterAsSink(parameters, 'OUTPUT',
                context, fields, source.wkbType(), source.sourceCrs())

        tol = self.parameterAsDouble(parameters,'TOLERANCE',context)#converts to crs units.
        
        labelField = self.parameterAsFields(parameters,'LABEL FIELD',context)[0]
        
        
        if self.parameterAsFields(parameters,'LENGTH FIELD',context):
            lengthField = self.parameterAsFields(parameters,'LENGTH FIELD',context)[0]
        else:
            lengthField = None
                           
        
        network = self.parameterAsSource(parameters, 'NETWORK', context)
        
        transform = QgsCoordinateTransform(source.sourceCrs(),network.sourceCrs(),QgsProject.instance())#transform from source to network coordinates

        index = QgsSpatialIndex(network)

        
        # Compute the number of steps to display within the progress bar and
        # get features from source
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        for current, feature in enumerate(source.getFeatures()):
           
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break
          
            f = QgsFeature(fields)
            
            pt = transform.transform(feature.geometry().asPoint())#qgsPointXY
            networkFeature = nearestFeature(network,index,pt,tol)

            
            if networkFeature is None:
                f.setAttributes(feature.attributes()+[None,None])
            else:
                f.setAttributes(feature.attributes()+[networkFeature[labelField],chainage(QgsGeometry.fromPointXY(pt),networkFeature,lengthField)])
                
            f.setGeometry(feature.geometry())
            sink.addFeature(f, QgsFeatureSink.FastInsert)

            # Update the progress bar
            feedback.setProgress(int(current * total))

        return {'OUTPUT': dest_id}


    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'point_to_chainage'


    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Point to chainage ')
    

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
        return pointToChainageAlgorithm()


    def helpUrl(self):
        help_path = os.path.join(os.path.dirname(__file__),'help','point_to_chainage.html')
        return 'file:/'+os.path.abspath(help_path)


'''
chainage of qgsPointXY pt.
'''
def chainage(pt,feature,lengthField):
    #if pt is None or feature is None:
       # return
    if lengthField:
        return feature[lengthField]*feature.geometry().lineLocatePoint(pt)/feature.geometry().length()
    else:
        return feature.geometry().lineLocatePoint(pt)

       
    
#source of index,qgsSpatialIndex,QgsGeometry
'''
returns nearest feature of source to QgsPointXyt pt and within tol.

index is qgsSpatialIndex containing only features of source.
using index.intersects because qgsSpatialIndex.nearestNeibor uses bounding box rather than proper distance.

'''
def nearestFeature(source,index,pt,tol=20):
    rect = QgsRectangle.fromCenterAndSize(pt,2*tol,2*tol)#square centered on pt
    request = QgsFeatureRequest()
    request.setFilterFids(index.intersects(rect))
    
    nearestFeature = None
    nearestDistance = math.inf
    p = QgsGeometry.fromPointXY(pt)
    
    for f in source.getFeatures(request):
        d = f.geometry().distance(p)
        if d<nearestDistance and d<tol:
            nearestDistance = d
            nearestFeature = f
        
    return nearestFeature
    

