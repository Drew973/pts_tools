# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 08:02:43 2023
@author: Drew.Bennett

TODO:
"""
import os

from qgis.core import (QgsProcessingAlgorithm,QgsProcessingParameterField,QgsProcessingParameterFeatureSink,QgsProcessingUtils,
                       QgsProcessingParameterFeatureSource,QgsProcessing,QgsFeatureRequest,QgsWkbTypes,QgsProcessingParameterFile)


from pts_tools.vcs.defect import fields
from pts_tools.shared import splinestring
from pts_tools.vcs import parse_excel
from pts_tools.vcs.check_calamine import checkCalamine


class importVcsSpreadsheetAlg(QgsProcessingAlgorithm):
      
         
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile(name = 'input',description = 'Spreadsheet',fileFilter = '*.xlsx'))
        self.addParameter(QgsProcessingParameterFeatureSource(name = 'network',description = 'Layer with LRS',types = [QgsProcessing.TypeVectorLine] ))
        self.addParameter(QgsProcessingParameterField('networkSec', 'LRS field with id',parentLayerParameterName='network'))
        self.addParameter(QgsProcessingParameterFeatureSink('output', 'OUTPUT', type=QgsProcessing.TypeVectorPolygon))



    def prepareAlgorithm(self,parameters,context,feedback):
        
        checkCalamine()
        
        
        self.input = self.parameterAsFile(parameters,'input',context)
        
        self.networkLayer = self.parameterAsVectorLayer(parameters,'network',context)
        
        if not QgsWkbTypes.hasM(self.networkLayer.wkbType()):
            #raise TypeError('LRS geometry needs M values')
            feedback.reportError('LRS geometry needs M values',fatalError=True)
            return False
        
        self.networkLabelField = self.field('networkSec',parameters,context)
        self.lrs = {}

        return True
    
    
    #parameterAsFields returns [] if field not set by user.
    def field(self,name, parameters, context):
        p = self.parameterAsFields(parameters,name,context)
        if len(p)>0:
            return p[0]  
    
        
    #lookup geometry from network layer
    def networkGeom(self,label):
    #    if isinstance(label,str):
     #       label = "'{lab}'".format(lab=label)
        req = QgsFeatureRequest()
        e = "\"{labelField}\" = '{lab}'".format(labelField = self.networkLabelField,lab = label)
      #  print('e',e)
        req.setFilterExpression(e)
    
        nf = [f.geometry() for f in self.networkLayer.getFeatures(req)]
       
        if len(nf)==1:
            return splinestring.fromQgsGeometry(nf[0])
       
        if len(nf)>1:
            return KeyError('multiple network features with {f} = {lab}'.format(f=self.networkLabelField,lab =label ))
            
        if len(nf)==0:
            return KeyError('no network features with {f} = {lab}'.format(f=self.networkLabelField,lab =label ))


    #see if label in self.lrs.
    #if not trys to find it and adds it or error
    #returns splinestring or raises error
    def lookupNetworkGeom(self,label):
        if not label in self.lrs:
            self.lrs[label] = self.networkGeom(label)
        g = self.lrs[label]
        if isinstance(g,Exception):
            raise g
        else:
            return g


    def processAlgorithm(self, parameters, context, feedback):
       # print(self.output)
        #not loaded if this in prepareAlgorithm. Bug in QGIS?
        self.sink,self.outputId = self.parameterAsSink(parameters,'output',
                                           context,fields = fields,
                                           crs = self.networkLayer.crs(),
                                           geometryType = QgsWkbTypes.Polygon)#(QgsFeatureSink,str)
        
       
        
        for d in parse_excel.parseExcel(self.input,feedback = feedback):
            networkGeom = self.lookupNetworkGeom(d.sec)
            mog = d.moGeom().densifyByDistance(5)
            xyGeom = networkGeom.moGeomToXY(mog)
            f = d.toFeature()
            f.setGeometry(xyGeom)
            self.sink.addFeature(f)
        return {'OUTPUT':self.outputId}
        
    def postProcessAlgorithm(self, context, feedback):
        layer = QgsProcessingUtils.mapLayerFromString(self.outputId, context)
        if layer is not None:
            styleFile = os.path.join(os.path.dirname(__file__),'vcs_style.qml')
           # print('layer',layer)
            layer.loadNamedStyle(styleFile)
            layer.triggerRepaint()
        return {'OUTPUT': self.outputId}
    

    def displayName(self):
        return 'Import VCS Spreadsheet'
    
    
    def name(self):
        return 'importvcsspreadsheet'
    
    
    def groupId(self):
        return 'vcs'    
        
    
    def group(self):
        return 'VCS'
    
    
    def createInstance(self):
        return importVcsSpreadsheetAlg()
    


    def shortHelpString(self):
        return '''<html>
        <body>
       
        <p>Creates new polygon layer from VCS spreadsheet and linear reference system.</p>
        <p>Transverse position is a crude approximation bases on the following assumptions:</p>
        <p>-LRS geometry is left edge of road</p>
        <p>-Lanes are 3.65m wide</p>
        <p>-Hard shoulder is 3.3m wide.</p>
        <p>-Road follows smooth curve between known points.</p>
        <p>Left edge of feature depends on lane and wheelpath. Right edge is width from this.</p>


        <p>LRS layer needs to have linestringM geometry. M values can be added with PTS tools:add_measure.
        Indexing id field can improve performance.</p>

        </body>
        </html>
        '''