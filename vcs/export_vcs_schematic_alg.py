# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 08:02:43 2023
@author: Drew.Bennett

TODO:
get number of lanes. Assume each lane has at least 1 feature (should at least have surface)
    

"""

from qgis.core import (QgsProcessingAlgorithm,QgsProcessingParameterField,
                       QgsProcessingParameterFeatureSource,QgsProcessing,QgsProcessingParameterFileDestination)

from pts_tools.vcs.defect import defect
from pts_tools.vcs.plot_schematic import plotSections

#from pts_tools.vcs.defect import fields,lanesClass


class exportVcsSchematicAlg(QgsProcessingAlgorithm):
      
         
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(name = 'input' , description = 'Layer with defects' , types = [QgsProcessing.TypeVectorPolygon] ))
        self.addParameter(QgsProcessingParameterField('sec', 'Field with section label' , parentLayerParameterName='input' , defaultValue = 'sec' , type = QgsProcessingParameterField.String ))
        self.addParameter(QgsProcessingParameterField('tp', 'Field with defect type' , parentLayerParameterName='input' , defaultValue = 'defectType' , type = QgsProcessingParameterField.String ))
        self.addParameter(QgsProcessingParameterField('lane', 'Field with lanes. Values should be like "HS,CL1,CL2"' , parentLayerParameterName='input' , defaultValue = 'lane' , type = QgsProcessingParameterField.String ))
        self.addParameter(QgsProcessingParameterField('wheelTrack', 'Field with wheel track. Values should be one of L,R,F,N,B' , parentLayerParameterName='input' , defaultValue = 'wheelTrack' , type = QgsProcessingParameterField.String ))
        self.addParameter(QgsProcessingParameterField('startChain', 'Field with start chainage' , parentLayerParameterName='input' , defaultValue = 'startChain' , type = QgsProcessingParameterField.Numeric ))
        self.addParameter(QgsProcessingParameterField('endChain', 'Field with end chainage' , parentLayerParameterName='input' , defaultValue = 'endChain' , type = QgsProcessingParameterField.Numeric ))
        self.addParameter(QgsProcessingParameterField('width', 'Field with width' , parentLayerParameterName='input' , defaultValue = 'width' , type = QgsProcessingParameterField.Numeric ))
     #   self.addParameter(QgsProcessingParameterField('moGeom', 'Field with WKT of chainage,offset geometry' , parentLayerParameterName='input' , defaultValue = 'MOgeom' , type = QgsProcessingParameterField.String ))
        self.addParameter(QgsProcessingParameterField('severity', 'Field with severity' , parentLayerParameterName='input' , defaultValue = 'severity' , type = QgsProcessingParameterField.Numeric|QgsProcessingParameterField.String ))

        self.addParameter(QgsProcessingParameterFileDestination(name = 'outputfile',description = 'Save to',fileFilter = '*.pdf'))


    def prepareAlgorithm(self,parameters,context,feedback):
        self.outputFile = self.parameterAsFile(parameters,'outputfile',context)
        self.secField = self.field('sec',parameters,context)
        self.tpField = self.field('tp',parameters,context)
        self.laneField = self.field('lane',parameters,context)
    #    self.moField = self.field('moGeom',parameters,context)
        self.wheelTrackField = self.field('wheelTrack',parameters,context)
        self.startChainField = self.field('startChain',parameters,context)
        self.endChainField = self.field('endChain',parameters,context)
        self.layer = self.parameterAsSource(parameters,'input',context)
        self.widthField = self.field('width',parameters,context)
        self.severityField = self.field('severity',parameters,context)

        return True
    
        
    #parameterAsFields returns [] if field not set by user.
    def field(self,name, parameters, context):
        p = self.parameterAsFields(parameters,name,context)
        if len(p)>0:
            return p[0]  
    


    def processAlgorithm(self, parameters, context, feedback):
        count = self.layer.featureCount()
        
        defects = []
        for i,f in enumerate(self.layer.getFeatures()):
            try:
                
                sec = f[self.secField]
                d = defect(sec = sec,
                           lane = f[self.laneField],
                           wheelTrack = f[self.wheelTrackField],
                           startChain = f[self.startChainField],
                           endChain = f[self.endChainField],
                           defectType = f[self.tpField],
                           width = f[self.widthField],
                           severity = f[self.severityField] )

                defects.append(d)
     
                
            except Exception as e:
                print(e)
                feedback.reportError(str(e))
            feedback.setProgress(100 * i /count)
            
        plotSections(defects = defects ,file = self.outputFile)
            
        return {'OUTPUT':self.outputFile}
        

    def displayName(self):
        return 'Export VCS Schematic'
    
    
    def name(self):
        return 'exportvcsschematic'
    
    
    def groupId(self):
        return 'vcs'    
        
    
    def group(self):
        return 'VCS'
    
    
    def createInstance(self):
        return exportVcsSchematicAlg()
    


    def shortHelpString(self):
        return '''<html>
        <body>
       
        <p>Makes VCS Schematic from layer.</p>

        </body>
        </html>
        '''