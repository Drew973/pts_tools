# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 08:05:10 2024

@author: Drew.Bennett
"""



from qgis.core import QgsGeometry,QgsRectangle,QgsFields,QgsField,QgsFeature
from PyQt5.QtCore import QVariant

    
#xsp,left,right
lanes = {'CL1':(0.0,3.65),'CL2':(3.65,7.3),'CL3':(7.3,10.95)}


#wheelTrack:left fraction,right fraction
wheelTracks = {'L':(3/20,7/20),'R':(13/20,17/20),'F':(0,1),'N':(7/20,13/20),'B':(3/20,17/20)}


def left(lane,wheelTrack):
    l,r = lanes[lane]
    w = r-l#width
    return -l - wheelTracks[wheelTrack][0]*w
    
    
def right(lane,wheelTrack):
    l,r = lanes[lane]
    w = r-l#width
    return -l - wheelTracks[wheelTrack][1]*w
    


fields = QgsFields()
fields.append(QgsField('sec',QVariant.String))
fields.append(QgsField('lane',QVariant.String))
fields.append(QgsField('wheelTrack',QVariant.String))
fields.append(QgsField('startChain',QVariant.Int))
fields.append(QgsField('endChain',QVariant.Double))
fields.append(QgsField('defectType',QVariant.String))


class defect:
    
    
    def __init__(self,sec,lane,wheelTrack,startChain,endChain,defectType):
        
        self.sec = str(sec)
        
        self.lane = str(lane).upper()
        if not self.lane in lanes:
            raise KeyError('Invalid lane "{lane}"'.format(lane = self.lane))
            
        self.wheelTrack = str(wheelTrack).upper()
        if not self.wheelTrack in wheelTracks:
            raise KeyError('Invalid wheel track "{wt}"'.format(wt = self.wheelTrack))
        
        self.startChain = int(startChain)
        self.endChain = float(endChain)
        self.defectType = str(defectType)
        
        
    #change this to every x meters? xy geom not curved as only 4 points.
    def moGeom(self):
        l = left(self.lane,self.wheelTrack)
        r = right(self.lane,self.wheelTrack)
        return QgsGeometry.fromRect(QgsRectangle(self.startChain,l,self.endChain,r))
        
    
    #does not set geom
    def toFeature(self):
        f = QgsFeature(fields)
        f['sec'] = self.sec
        f['lane'] = self.lane
        f['wheelTrack'] = self.wheelTrack
        f['startChain'] = self.startChain
        f['endChain'] = self.endChain
        f['defectType'] = self.defectType
        return f
        
        