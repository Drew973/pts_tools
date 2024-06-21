# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 08:02:43 2023
@author: Drew.Bennett

TODO:
get number of lanes. Assume each lane has at least 1 feature (should at least have surface)
    

"""
import os

from qgis.core import (QgsProcessingAlgorithm,QgsProcessingParameterField,QgsProcessingParameterFeatureSink,QgsProcessingUtils,
                       QgsProcessingParameterFeatureSource,QgsProcessing,QgsFeatureRequest,QgsWkbTypes,QgsProcessingParameterFile)


from pts_tools.vcs.defect import fields,lanesClass
from pts_tools.shared import splinestring
from pts_tools.vcs import parse_excel
from pts_tools.vcs.check_imports import checkCalamine


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
    def lookupNetworkGeom(self,label):
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
            raise KeyError('multiple network features with {f} = {lab}'.format(f=self.networkLabelField,lab =label ))
            
        if len(nf)==0:
            raise KeyError('no network features with {f} = {lab}'.format(f=self.networkLabelField,lab =label ))


    def processAlgorithm(self, parameters, context, feedback):
       # print(self.output)
        #not loaded if this in prepareAlgorithm. Bug in QGIS?
        self.sink,self.outputId = self.parameterAsSink(parameters,'output',
                                           context,fields = fields,
                                           crs = self.networkLayer.crs(),
                                           geometryType = QgsWkbTypes.Polygon)#(QgsFeatureSink,str)
        
        #{section:[defect]}
        sections = {}
        for d in parse_excel.parseExcel(self.input,feedback = feedback):
            if d.sec in sections:
                sections[d.sec].append(d)#add to defects
            else:
                sections[d.sec] = [d]#add new entry
            
        #print('sections',sections)
        for k,v in sections.items():
            try:
                networkGeom = self.lookupNetworkGeom(k)
                
                lanes = lanesClass()
                for d in v:
                    lanes |= d.lanes
                        
               # print('lanes',lanes)
                
                invalid = lanes.invalidRoad()
                if invalid:
                    raise ValueError(invalid)
                    
                for d in v:
                    f = d.toFeature(roadLanes = lanes , networkGeom = networkGeom)
                    self.sink.addFeature(f)
                     
            except KeyError as e:
                feedback.reportError(str(e))
                
                
                
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
        <p>-Section has same lanes throughout length, all or which appear in spreadsheet.<p>
        <p>-Lanes are 3.65m wide</p>
        <p>-Hard shoulder is 3.3m wide.</p>
        <p>-Road follows smooth curve between known points.</p>
        <p>Left edge of feature depends on lane and wheelpath. Right edge is width from this.</p>


        <p>LRS layer needs to have linestringM geometry. M values can be added with PTS tools:add_measure.
        Indexing id field can improve performance.</p>

        </body>
        </html>
        '''