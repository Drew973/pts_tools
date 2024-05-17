# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 08:05:10 2024

@author: Drew.Bennett
"""

from enum import Flag,Enum,auto
from PyQt5.QtCore import QVariant
from qgis.core import QgsGeometry,QgsRectangle,QgsFields,QgsField,QgsFeature

from pts_tools.vcs.lanes import lanes as lanesClass


#xsp,left,right
laneWidths = {'HS':(3.3,0.0),
        'CL1':(0.0,-3.65),
         'CL2':(-3.65,-7.3),
         'CL3':(-7.3,-10.95)
         }




'''
valid patern is : 
    HS
    CL1 - CL6
    CR1 - CR6
'''



    

#wheelTrack:left fraction,right fraction
wheelTracks = {'L':(3/20,7/20),'R':(13/20,17/20),'F':(0,1),'N':(7/20,13/20),'B':(3/20,17/20)}

class wheelTrackEnum(Enum):
    L = 1
    R = 2
    F = 3
    N = 4
    B = 5
    
    @staticmethod
    def fromString(s):
        s = s.strip().replace(' ','').upper()
        if s == 'L-R' or s=='R-L':
            return wheelTrackEnum['B']
        try:
            return wheelTrackEnum[s]
        except:
            pass


    def left(self):
        return wheelTracks[self.name][0]


    def right(self):
        return wheelTracks[self.name][1]


    def __str__(self):
        return self.name



# +ve         HS,CL1,CL2,CLN     centerline/0    CR1,CR2,CRN    -ve
def leftOffset(lanes,wheelTrack,roadLanes,laneWidth = 3.65,hsWidth = 3.3):
   
    l = lanes.leftOffset(roadLanes)
    
    if lanes.leftmost == 'HS':
        w = 3.3
    else:
        w = 3.65
    return l - wheelTrack.left() * w
    
    
def rightOffset(lanes,wheelTrack,roadLanes):
    return 0.0
    l = lanes.left()
    r = lanes.right()
    w = abs(r - l)#width
    return l - wheelTrack.right() * w
    

#charactors from A-Z
def AZ(string):
    n = ''
    for c in string.upper():
        if c.isalpha():
            n += c
    return n


#charactors from A-Z and numbers
def AZN(string):
    n = ''
    for c in string.upper():
        if c.isalpha() or c.isnumeric():
            n += c
    return n
    

fields = QgsFields()
fields.append(QgsField('sec',QVariant.String))
fields.append(QgsField('lane',QVariant.String))
fields.append(QgsField('wheelTrack',QVariant.String))
fields.append(QgsField('width',QVariant.Double))
fields.append(QgsField('startChain',QVariant.Int))
fields.append(QgsField('endChain',QVariant.Double))
fields.append(QgsField('defectType',QVariant.String))
fields.append(QgsField('severity',QVariant.String))
fields.append(QgsField('photo',QVariant.String))

    
'''
only certain combinations of type and severity valid. Enum seems like best way to validate.
'''
    
    
class defectEnum(Enum):
    HRA = auto()
    HFSC = auto()    
    TSSC = auto()
    OJ_N = auto()
    OJ_M = auto()
    OJ_W = auto()
    CR_1 = auto()
    CR_2 = auto()
    TC_1 = auto()
    TC_2 = auto()
    LP = auto()
    CJ = auto()
    BJ = auto()
    N = auto()
    IW = auto()
    CZ_1 = auto()
    CZ_2 = auto()
    FT_1 = auto()
    FT_2 = auto()
    PA_1 = auto()
    PA_2 = auto()
    POT = auto()
    TF_1 = auto()
    TF_2 = auto()
    SD_1 = auto()
    SD_2 = auto()
    MP = auto()
    DEP = auto()

    #->str
    def typeStr(self):
        return self.name.split('_')[0]
    
    
    #any part following _ in name
    #->str
    def severityStr(self):
        v = self.name.split('_')
        if len(v)>1:
            return v[1]
        return ''
    
    @staticmethod 
    def fromStrings(featType,sev):
        a = AZ(featType) 
        b = AZN(sev)
        if b:
            return defectEnum[ a + '_' + b ]
        return defectEnum[ a ]



    
class defect:
    
    def __init__(self,sec,lane,wheelTrack,startChain,defectType,severity,photo = '',width = 0.0,endChain=None):
        
        self.sec = str(sec)
        
        self.lanes = lanesClass.fromString(lane)
        if not self.lanes:#no bits set
            raise ValueError('invalid lane:' + lane)
            
            
        self.wheelTrack = wheelTrackEnum.fromString(wheelTrack)        
        if self.wheelTrack is None:
            raise KeyError('Invalid wheel track "{wt}"'.format(wt = self.wheelTrack))
        
        self.width = abs(float(width))
        
        self.startChain = int(startChain)
        
        if endChain == '' or endChain is None:
            self.endChain = self.startChain + 0.5
        else:
            self.endChain = float(endChain)
        
       # self.defectType = featureType.featureTypeFromString(defectType)
        
        if isinstance(severity,float):
            severity = int(severity)
        #self.severity = severityEnum.fromStr(str(severity))
        
        self.defectType = defectEnum.fromStrings(defectType,str(severity))

        self.photo = str(photo)
        
    
    
    #change this to every x meters? xy geom not curved as only 4 points.
    def moGeom(self,roadLanes):
        lef = leftOffset(lanes = self.lanes , wheelTrack = self.wheelTrack, roadLanes = roadLanes)
        return QgsGeometry.fromRect(QgsRectangle(self.startChain,lef - self.width,self.endChain,lef))
        
    
    #does not set geom
    def toFeature(self):
        f = QgsFeature(fields)
        f['sec'] = self.sec
        f['lane'] = str(self.lanes)
        f['wheelTrack'] = str(self.wheelTrack)
        f['startChain'] = self.startChain
        f['endChain'] = self.endChain
        f['defectType'] = self.defectType.typeStr()
        f['severity'] = self.defectType.severityStr()
        f['width'] = self.width
        f['photo'] = self.photo
        return f
        
    
    
    def __repr__(self):
        return 'defect:'+str(vars(self))
        
    

if __name__ == '__console__':
    pass
    
    
    
    
    
    
    
    