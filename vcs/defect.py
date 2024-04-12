# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 08:05:10 2024

@author: Drew.Bennett
"""



from qgis.core import QgsGeometry,QgsRectangle,QgsFields,QgsField,QgsFeature
from PyQt5.QtCore import QVariant


from enum import Flag,Enum


class lanesFlag(Flag):
    
    HS = 1
    CL1 = 2
    CL2 = 4
    CL3 = 8

    @staticmethod 
    def fromString(s):
        r = lanesFlag(0)
        for v in s.upper().replace('&',',').replace('+',',').split(','):
            c = lanesFlag.laneFromStr(v)
            if c:                
                r = r|c
        return r
            
    def __str__(self):
        r = []
        for lane in lanesFlag:
          if self & lane:
              r.append(lane.name)
        return ','.join(r)
    
    @staticmethod 
    def laneFromStr(s):
        try:
            return lanesFlag[s]
        except ValueError:
            return None

    def left(self):
        return laneWidths[lanesFlag.leftmost(self).name][0]
     
    def right(lanes):
         if lanes & lanesFlag.CL3:
             return laneWidths['CL3'][1]
         if lanes & lanesFlag.CL2:
             return laneWidths['CL2'][1]
         if lanes & lanesFlag.CL1:
             return laneWidths['CL1'][1]
         if lanes & lanesFlag.HS:
             return laneWidths['HS'][1]

    def leftmost(self):
        for lane in lanesFlag:
          if self & lane:
              return lane
          
    
            
#xsp,left,right
laneWidths = {'CL1':(0.0,3.65),
         'CL2':(3.65,7.3),
         'CL3':(7.3,10.95),
         'HS':(-3.3,0.0)
         }


def lanesFromString(s):
    s = s.upper().replace('&',',').replace('+',',')
    return sorted([v for v in s.split(',') if v in laneWidths])
    



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


#wheelTrack:left fraction,right fraction
wheelTracks = {'L':(3/20,7/20),'R':(13/20,17/20),'F':(0,1),'N':(7/20,13/20),'B':(3/20,17/20)}


def left(lanes,wheelTrack):
    l = lanes.left()
    #r = lanes.right()
    r = laneWidths[lanes.leftmost().name][1]
    w = r - l#width
    return -l - wheelTrack.left() * w
    
    
def right(lanes,wheelTrack):
    l = lanes.left()
    r = lanes.right()
    w = r - l#width
    return -l - wheelTrack.right() * w
    


fields = QgsFields()
fields.append(QgsField('sec',QVariant.String))
fields.append(QgsField('lane',QVariant.String))
fields.append(QgsField('wheelTrack',QVariant.String))
fields.append(QgsField('width',QVariant.Double))
fields.append(QgsField('startChain',QVariant.Int))
fields.append(QgsField('endChain',QVariant.Double))
fields.append(QgsField('defectType',QVariant.String))
fields.append(QgsField('photo',QVariant.String))


class defect:
    
    
    def __init__(self,sec,lane,wheelTrack,startChain,defectType,photo,width = None,endChain=None):
        
        self.sec = str(sec)
        
        self.lanes = lanesFlag.fromString(lane)
        if not self.lanes:#no bits set
            raise ValueError('invalid lane:' + lane)
            
            
        self.wheelTrack = wheelTrackEnum.fromString(wheelTrack)        
        if self.wheelTrack is None:
            raise KeyError('Invalid wheel track "{wt}"'.format(wt = self.wheelTrack))
        
        if width is None:
            width = right(self.lane,self.wheelTrack) - left(self.lane,self.wheelTrack)
        self.width = abs(float(width))
        
        self.startChain = int(startChain)
        
        if endChain == '' or endChain is None:
            self.endChain = self.startChain + 0.5
        else:
            self.endChain = float(endChain)
        
        self.defectType = str(defectType)
        self.photo = str(photo)
        
        
    #change this to every x meters? xy geom not curved as only 4 points.
    def moGeom(self):
        lef = left(self.lanes,self.wheelTrack)
        #print(self.lanes,self.wheelTrack,'left',lef)
        return QgsGeometry.fromRect(QgsRectangle(self.startChain,lef - self.width,self.endChain,lef))
        
    
    #does not set geom
    def toFeature(self):
        f = QgsFeature(fields)
        f['sec'] = self.sec
        f['lane'] = str(self.lanes)
        f['wheelTrack'] = str(self.wheelTrack)
        f['startChain'] = self.startChain
        f['endChain'] = self.endChain
        f['defectType'] = self.defectType
        f['width'] = self.width
        f['photo'] = self.photo
        return f
        
    
    
    def __repr__(self):
        return 'defect:'+str(vars(self))
        
    
def testLanesFromString():
    s = 'CL1,CL2'
    r = lanesFromString(s)
    print(r)
    
    
def testLanesFlagFromString():
    s = 'CL1,CL2'
    r = lanesFlag.fromString(s)
    print(r)
    print('left',r.left())
    
    
if __name__ == '__console__':
    #testLanesFromString()
    testLanesFlagFromString()