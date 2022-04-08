# -*- coding: utf-8 -*-


__author__ = 'drew'
__date__ = '2021-09-09'
__copyright__ = '(C) 2021 by drew'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


from qgis.PyQt.QtCore import QCoreApplication
from PyQt5.QtCore import QVariant


from qgis.core import (
                       QgsFeature,
                       QgsProcessingContext,
                       QgsField,
                       QgsProcessingFeedback,
                       QgsProcessingFeatureBasedAlgorithm,
                       QgsProcessingParameterField,
                       QgsProcessingParameterDistance,
                       )


from pts_tools.shared_functions import substring,split


#import logging# logging doesn't seem to work well with this

class splitByChainageAlgorithm(QgsProcessingFeatureBasedAlgorithm):

    
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


   # def helpUrl(self):
    #    help_path = os.path.join(os.path.dirname(__file__),'help','split_by_chainage.html')
     #   return 'file:/'+os.path.abspath(help_path)
        
    
    def shortHelpString(self):
        return r'''<html><body>
		<p>Algorithm to split features into equal lengths and remainder.</p>

		<p>Creates new layer:</p>
			<li>-Containing 1 or more features per input feature.</li>
			<li>-With additional fields source_id,start_chainage and end_chainage (source_id is feature id of input feature).</li>
		
        <p>If "Section length field" is set section length is treated as this,otherwise length of geometry is used. </p>
    
    
    	<h3> Examples:</h3>
    
    		<li> 25 m feature with step of +10m will become 0-10 10-20,20-25 m pieces.</li>
    		<li> 25 m feature with step of -10m will become 25-15,15-5,5-0 m pieces.</li>
    
    
    	<h3>2D vs 3D geometry</h3>
    
    		<li> Split by chainage can work with 2D and 3D geometries.</li>
    		<li> Networks supplied by clients usually have 2D geometries(no altitude).</li>
    		<li> Section lengths calculated from 2D geometry will be shorter than the actual 3D length of the road.</li>
    		<li> Chainage measured along 3D road will be different to chainage calculated as the crow flies from 2D geometry.</li>
            </body></html>
        '''        
