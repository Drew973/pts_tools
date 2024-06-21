# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 08:05:10 2024

@author: Drew.Bennett
"""

from enum import Enum
from typing import List,Dict,Tuple
from PyQt5.QtCore import QVariant
from qgis.core import QgsGeometry,QgsRectangle,QgsFields,QgsField,QgsFeature

from pts_tools.vcs.lanes import lanes as lanesClass
from matplotlib.patches import Rectangle,Circle,Patch,PathPatch
from matplotlib.path import Path
from pts_tools.vcs.defect_types import fromStrings,defectEnum,typeStr,severityStr,fullName
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

    #->float fraction from 0 to 1
    def left(self):
        return wheelTracks[self.name][0]

    #->float fraction from 0 to 1
    def right(self):
        return wheelTracks[self.name][1]


    def __str__(self):
        return self.name




    

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
fields.append(QgsField('MOGeom',QVariant.String))
fields.append(QgsField('leftOffset',QVariant.Double))


    


# For plotting schematics CL3 is bottom of plot. offset of 0.

w = 3.65
HSWidth = 3.3

defaultRoadLanes = {
                    'CL3': (0 , w),
                    'CL2':(w , w*2),
                    'CL1': (w*2 , w*3),
                    'HS':(w*3 , w*3 + HSWidth)
                    }





def leftOffset(lanes: List[str] , wheelTrack: wheelTrackEnum , roadLanes: Dict [str,Tuple[float,float]] = defaultRoadLanes) -> float:
    a = {k: v for k, v in roadLanes.items() if k in lanes}
    
    if a:
        minLane = max(a, key = lambda k: a[k][0])
      #  print(minLane)
        return a[minLane][0] - w * wheelTrack.left()
    
    return 0.0


def testLeftOffset():
    lane = ['CL1','CL2']
    wheelTrack = wheelTrackEnum['L']
    r = leftOffset(lane,wheelTrack)
    print(r)
    


def patch(defectType):
    args = {}
    
    if defectType == defectEnum['HFSC']:
        args = {'facecolor':(0.585,0.585,0.585)}#grey
                       
    if defectType == defectEnum['TSSC']:
        args = {'facecolor':(0.5,0.5,0.5)}#light grey

    if defectType == defectEnum['TC_1']:
        args = {'facecolor':'none','linewidth':2,'linestyle':'--','edgecolor': 'red'}

    if defectType == defectEnum['TC_2']:
        args = {'facecolor':'none','linewidth':2,'edgecolor': 'red'}
        
    if defectType == defectEnum['SD_1']:
        args = {'facecolor':'#f3a6b2'}#pink
        
    if defectType == defectEnum['SD_2']:
        args = {'facecolor':'#f600ea'}#purple   

    if defectType == defectEnum['PA_1']:
        args = {'facecolor':'black'} 
        
    if defectType == defectEnum['PA_2']:
        args = {'facecolor':'white','hatch':'/','edgecolor':'#0162ff'}#blue hatched
        
    if defectType == defectEnum['OJ_N']:
        args = {'facecolor':'none','linewidth':2,'edgecolor': 'green'}

    if defectType == defectEnum['OJ_M']:
        args = {'facecolor':'none','linewidth':2,'edgecolor': 'red'}

    if defectType == defectEnum['OJ_W']:
        args = {'facecolor':'none','linewidth':4,'edgecolor': 'red'}
    
    if defectType == defectEnum['LP']:
        args = {'facecolor':'none','linewidth':2,'edgecolor': 'black','linestyle':'--'}
   
    if defectType == defectEnum['CZ_1']:
        args = {'facecolor':'#fc9a1a'}#orange

    if defectType == defectEnum['CZ_2']:
        args = {'facecolor':'#fad102'}#yellowy orange

    if defectType == defectEnum['CR_1']:
        args = {'facecolor':'white','hatch':'\\','edgecolor':'red'}#red hatched

    if defectType == defectEnum['CR_2']:
        args = {'facecolor':'white','edgecolor':'red','linewidth':2}#red hatched
         
    if defectType == defectEnum['IW']:
        args = {'facecolor':'blue','edgecolor':'black','linewidth':2}
                 
    if defectType == defectEnum['FT_1']:
        args = {'facecolor':'#948A54'}#olive
                         
    if defectType == defectEnum['FT_2']:
        args = {'facecolor':'#953735'}#dark brown
                
    if not args:
        print('unknown defectType',defectType)
        
    return Rectangle(xy = (0,0),width = 0,height = 0,zorder = defectType.value,label = fullName(defectType),**args)
    
    
    
def toPatch(defectType:defectEnum , wheelTrack: wheelTrackEnum = wheelTrackEnum['F'], startChain:float = 0.0 , endChain:float = 1.0 , lane:List[str] = [] ,
            width: float = 1.0,roadLanes: Dict [str,Tuple[float,float]] = defaultRoadLanes) -> Patch:
    
    bottom = leftOffset(lanes = lane , wheelTrack = wheelTrack , roadLanes = roadLanes)
    left = min(startChain,endChain)
    
    if defectType == defectEnum['POT']:
        return Circle((left,bottom),radius = 0.5*width, facecolor = 'red',zorder = defectType.value,label = fullName(defectType))

    if defectType == defectEnum['CJ']:
        pth = Path([(left,bottom),(left,bottom+width)])
        return PathPatch(pth,edgecolor = 'purple',linewidth = 4,zorder = defectType.value,label = fullName(defectType))
    
    p = patch(defectType)

    if isinstance(p,Rectangle):
        #set_bounds(left, bottom, width, height)
        p.set_bounds(left , bottom , abs(endChain-startChain) , width)
        
    return p



def testToPatch():
    lane = ['CL1','CL2']
    wt = wheelTrackEnum['L']
    p = toPatch(defectType = defectEnum['TSSC'], startChain = 100, endChain = 200 , lane = lane , wheelTrack = wt , width = 0.5)
    print(p)

    
class defect:
    
    def __init__(self,sec,lane,wheelTrack,startChain,defectType,severity ,photo = '',width = 0.0,endChain=None):
        
        self.sec = str(sec)
        
        self.lanes = lanesClass.fromString(lane)
        if not self.lanes:#no bits set
            raise ValueError('invalid lane:' + lane)
            
            
        self.wheelTrack = wheelTrackEnum.fromString(wheelTrack)        
        if self.wheelTrack is None:
            raise KeyError('Invalid wheel track "{wt}"'.format(wt = self.wheelTrack))
        
        self.width = abs(float(width))
        
        self.leftEdge = 0
        
        self.startChain = int(startChain)
        
        if endChain == '' or endChain is None:
            self.endChain = self.startChain + 0.5
        else:
            self.endChain = float(endChain)
        
       # self.defectType = featureType.featureTypeFromString(defectType)
        
        if isinstance(severity,float):
            severity = int(severity)
        #self.severity = severityEnum.fromStr(str(severity))
        
        self.defectType = fromStrings(defectType,str(severity))

        self.photo = str(photo)
        
    
    
    #change this to every x meters? xy geom not curved as only 4 points.
    def moGeom(self,roadLanes):
        lef = self.leftOffset(roadLanes = roadLanes)
        return QgsGeometry.fromRect(QgsRectangle(self.startChain,lef - self.width,self.endChain,lef))
        
    
    #does not set geom
    def toFeature(self , roadLanes , networkGeom):
        f = QgsFeature(fields)
        f['sec'] = self.sec
        f['lane'] = str(self.lanes)
        f['wheelTrack'] = str(self.wheelTrack)
        f['startChain'] = self.startChain
        f['endChain'] = self.endChain
        f['defectType'] = typeStr(self.defectType)
        f['severity'] = severityStr(self.defectType)
        f['width'] = self.width
        f['leftOffset'] =  self.leftOffset(roadLanes = roadLanes)
        f['photo'] = self.photo
        mog = self.moGeom(roadLanes = roadLanes)
        xyGeom = networkGeom.moGeomToXY(mog.densifyByDistance(5))

        f.setGeometry(xyGeom)
        f['MOGeom'] = mog.asWkt()
                    
        return f
        
    #road layput like:  
    #+ve         HS,CL1,CL2,CLN     centerline/0    CR1,CR2,CRN    -ve
    def leftOffset(self,roadLanes):
        l = self.lanes.leftOffset(roadLanes)
        
        if self.lanes.leftmost == 'HS':
            w = 3.3
        else:
            w = 3.65
        return l - self.wheelTrack.left() * w
    
    
    
    def __repr__(self):
        return 'defect:'+str(vars(self))
        
    
    
    #top is left edge of road.
    def toPatch(self,roadLanes: Dict [str,Tuple[float,float]] = defaultRoadLanes) -> Patch:
        return toPatch(defectType = self.defectType,startChain = self.startChain,endChain = self.endChain,
                       lane = self.lanes.data,wheelTrack = self.wheelTrack,width = self.width,roadLanes = roadLanes)
      


if __name__ in ('__main__','__console__'):
    testToPatch()

    
    
    
    
    
    
    