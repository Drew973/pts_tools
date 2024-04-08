# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 08:02:43 2023
@author: Drew.Bennett

TODO:
"""

from qgis.core import (QgsProcessingFeatureBasedAlgorithm,QgsProcessingParameterField,QgsFeature,
                       QgsProcessingParameterFeatureSource,QgsProcessing,QgsFeatureRequest,QgsWkbTypes,
                       
                       )



from pts_tools.vcs_to_gis.defect import defect,fields
from pts_tools.shared import splinestring



class vcsToGisAlg(QgsProcessingFeatureBasedAlgorithm):
      
    def initParameters(self, config):
        #delimited text fields treated as str until loaded into QGIS.
         self.addParameter(QgsProcessingParameterField('sec', 'Field with section label',parentLayerParameterName='INPUT',defaultValue='sec'))
         self.addParameter(QgsProcessingParameterField('lane', 'Field with lane',parentLayerParameterName='INPUT',defaultValue='lane'))
         self.addParameter(QgsProcessingParameterField('wheelTrack', 'Field with wheel track',parentLayerParameterName='INPUT',defaultValue='wheel_track'))
         self.addParameter(QgsProcessingParameterField('startChain', 'Field with start section chainage', parentLayerParameterName='INPUT',defaultValue='start_chain'))
         self.addParameter(QgsProcessingParameterField('endChain', 'Field with end section chainage' , parentLayerParameterName='INPUT',defaultValue='end_chain'))
         self.addParameter(QgsProcessingParameterField('featureType', 'Field with feature type' , parentLayerParameterName='INPUT',defaultValue='feature_type'))

         self.addParameter(QgsProcessingParameterFeatureSource(name = 'network',description = 'Layer with LRS',types = [QgsProcessing.TypeVectorLine] ))
         self.addParameter(QgsProcessingParameterField('networkSec', 'LRS field with id',parentLayerParameterName='network'))
         


    def prepareAlgorithm(self,parameters,context,feedback):
        self.networkLayer = self.parameterAsVectorLayer(parameters,'network',context)
        
        if not QgsWkbTypes.hasM(self.networkLayer.wkbType()):
            #raise TypeError('LRS geometry needs M values')
            feedback.reportError('LRS geometry needs M values',fatalError=True)
            return False
        
        self.networkLabelField = self.field('networkSec',parameters,context)
        
        self.secField = self.field('sec',parameters,context)
        self.laneField = self.field('lane',parameters,context)
        self.wheelTrackField = self.field('wheelTrack',parameters,context)

        self.startChainField = self.field('startChain',parameters,context)
        self.endChainField = self.field('endChain',parameters,context)
        self.typeField = self.field('featureType',parameters,context)


        self.lrs = {}
        
        return True
    
    
    #parameterAsFields returns [] if field not set by user.
    def field(self,name, parameters, context):
        p = self.parameterAsFields(parameters,name,context)
        if len(p)>0:
            return p[0]  
    
    
    #crap documentation for this. QgsProcessing enum seems to be working.
    def inputLayerTypes(self):
        return [QgsProcessing.TypeVector]
        
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


    def featureToDefect(self,feature):
        return defect(sec = feature[self.secField],
               lane = feature[self.laneField],
               wheelTrack = feature[self.wheelTrackField],
               startChain = feature[self.startChainField],
               endChain = feature[self.endChainField],
               defectType = feature[self.typeField])


  # def processFeature(self, feature: QgsFeature, context: QgsProcessingContext, feedback: QgsProcessingFeedback) → object
    def processFeature(self, feature, context, feedback):
        try:
            d = self.featureToDefect(feature)
           # print('defect',d)
            mog = d.moGeom().densifyByDistance(5)
      #      print('mo geom',mog)
            
            networkGeom = self.lookupNetworkGeom(d.sec)
        #    print('networkGeom',networkGeom)
            
            xyGeom = networkGeom.moGeomToXY(mog)
          #  print('xyGeom',xyGeom)
            
            f = d.toFeature()
            f.setGeometry(xyGeom)
  
            return [f]
        
        except Exception as e:
            message = 'Skipped feature. {m}'.format(m = str(e))
            feedback.reportError(message,fatalError = False)
            #print(e)
            return []
     
    #outputFields(self, inputFields: QgsFields) → QgsFields

    def outputFields(self, inputFields):
     #   print('fields',fields)
        return fields
    
    
    def displayName(self):
        return 'VCS To GIS'
    
    
    def name(self):
        return 'vcstogis'
    
    
    def groupId(self):
        return 'vcs'    
        
    
    def group(self):
        return 'VCS'
    
    
    def createInstance(self):
        return vcsToGisAlg()
    
        
    def inputParameterDescription(self):
        return 'File/layer with VCS Data. Usually has no geometry'
    
    
    def outputName(self):
        return 'VCS'
      #  return self.networkLayer.name()
    
    
    #->QgsProcessing.SourceType
    def outputLayerType(self):
        return QgsProcessing.TypeVectorPolygon
       # return QgsProcessing.TypeVectorAnyGeometry
    
    
    def outputCrs(self,inputCrs):
        return self.networkLayer.crs()
      
  
    def outputWkbType(self,inputWkbType):
        return QgsWkbTypes.Polygon


    def shortHelpString(self):
        return '''<html>
        <body>
       
        <p>Creates new polygon layer from distress data and linear reference system.</p>
        <p>Treats LRS geometry as left edge of road. Assumes 3.65m wide lanes.</p>
        <p>Transverse position is a crude approximation.</p>

        
        <p>LRS layer needs to have linestringM geometry. m values can be added with PTS tools:add_measure.</p>
        <p>Faster when LRS is indexed on label field.</p>
        

        </body>
        </html>
        '''