from scipy import interpolate
import numpy as np

from qgis.core import QgsLineString,QgsGeometry,QgsPointXY,QgsProject
import math
import sys
import matplotlib.pyplot as plt



if __name__ =='__console__':
    folder = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\extract_by_curvature'
    if not folder in sys.path:
        sys.path.append(folder)
    import clumpArray
    
else:
    from pts_tools.curvature import clumpArray

    
class sectionHandler:
    
    def __init__(self,geom):
        self.xSpline = None
        self.ySpline = None
        

        #get points dist apart at most.
        dist = min([geom.length()/4,10])#need at least 4 points
        geom = geom.densifyByDistance(dist)
        
        self.x,self.y,self.ch = zip(*vertices(geom))
        
        self.geomLength = geom.length()
        
        weights = [1 for c in self.ch]
        weights[0] = 10
        weights[-1] = 10
    
        s = len(self.ch)/32 #smaller = less smoothing. default is len(weights)
        
        
        if len(self.ch)>3:#need 4+ points to fit cublic spline
            self.xSpline = interpolate.UnivariateSpline(self.ch, self.x, weights, s=s, ext=2)
            self.ySpline = interpolate.UnivariateSpline(self.ch, self.y, weights, s=s, ext=2)
            
           # bc = 'natural' ‘clamped’:
           # bc = 'not-a-knot'
           # self.xSpline = interpolate.CubicSpline(self.ch,self.x,bc_type = bc)
            #self.ySpline = interpolate.CubicSpline(self.ch,self.y,bc_type = bc)


    def enoughPoints(self):
        return not self.xSpline is None
        
    #Interpolates geometry from Spline. Smoothing means this may be different to input geometry.
    def interpolatedGeom(self,spacing):
        ch = np.append(np.arange(0,self.geomLength,spacing),self.length)
        return QgsGeometry(QgsLineString(self.xSpline(ch),self.ySpline(ch)))
        
        
#https://www.math24.net/curvature-radius
#curvature=1/radius of curvature
    def curvature(self,ch):
       
        x1 = self.xSpline.derivative(1)(ch)#x'
        x2 =  self.xSpline.derivative(2)(ch)#x''
        y1 = self.ySpline.derivative(1)(ch)#y'
        y2 =  self.ySpline.derivative(2)(ch)#y''
        return abs((x1*y2-y2*x2))*math.pow(x1*x1+y1*y1,-3/2)
    
    
    
    def radi(self,chainages):
        x1 = self.xSpline(chainages,1)#x'
        x2 =  self.xSpline(chainages,2)#x''
        y1 = self.ySpline(chainages,1)#y'
        y2 =  self.ySpline(chainages,2)#y''
    
        return np.divide(np.power(x1*x1+y1*y1,1.5),np.absolute(x1*y2-y1*x2)) # * short for as np.multiply  - for np.subtract
    
    
    
    #gets curvatures at chainages.
    #curvature=1/radius of curvature
    #https://www.math24.net/curvature-radius
    def curvatures(self,chainages):
        x1 = self.xSpline(chainages,1)#x'
        x2 =  self.xSpline(chainages,2)
        y1 = self.ySpline(chainages,1)#y'
        y2 =  self.ySpline(chainages,2)#y''
                
        return np.multiply(np.absolute(np.subtract(np.multiply(x1,y2),np.multiply(y2,x2))),
        np.power(np.add(np.multiply(x1,x1),np.multiply(y1,y1)),-3/2))
        
      
    #returns radius of curvature at chainages.
 #   def radi(self,chainages):
    #    return np.divide(1,self.curvatures(chainages))


    def interpolateX(self,chainages):
        return self.xSpline(chainages)
        #return interpolate.splev(chainages,self.xSpline,ext=2)


    def interpolateY(self,chainages):
        return self.ySpline(chainages)

        #return interpolate.splev(chainages,self.ySpline,ext=2)
        
        
    #interpolated points.
    def points(self,chainages):
        xVals = self.interpolateX(chainages)
        yVals = self.interpolateY(chainages)
        return [QgsGeometry.fromPointXY(QgsPointXY(x,yVals[i])) for i,x in enumerate(xVals)]



   #
    #def point(self,ch):
     #   self.checkChainage(ch)
      #  return QgsGeometry.fromPointXY(QgsPointXY(self.interpolate.splev(ch),self.ySpline(ch)))

    def radiLessThan(self,threshold,resolution=5):
        
        chainages = np.arange(0,self.geomLength,resolution)
        if chainages[-1]<self.geomLength:
            chainages = np.append(chainages,[self.geomLength])
        
        radi = self.radi(chainages)
        indexes = clumpArray.clumpArray(radi<threshold)
        
        chainageRanges = [(chainages[s],chainages[e]) for s,e in indexes]
        return chainageRanges
        
        #scipy.interpolate.sproot(tck, mest=10) gets roots.
 
 

    #useful for debugging.
    def plot(self):
        
        fig1, (ax1,ax2) = plt.subplots(nrows=2, ncols=1)
        ax1.plot(self.x,self.y,'x',label='points')
        chainages = np.arange(0,max(self.ch))
        
        x = self.xSpline(chainages)#scipy.interpolate.interpolate.interp1d
        y = self.ySpline(chainages)
        #plt.plot(self.interpolateX(chainages),self.interpolateX(chainages),label='fit')
        ax1.plot(x,y,label='fit')
        
        ax1.set_xlabel('x')
        ax2.set_ylabel('y')
        
        ax2.set_ylim(top=1000)
        
        fig1.legend()
        ax2.set_xlabel('chainage')
        ax2.set_ylabel('roc(m)')
        #fig2, ax2= plt.subplots()
        ax2.plot(chainages,self.radi(chainages),label='radi')
        
        
        
        
        
#returns turple of (x,y,ch) of vertices.
#ch is cartesian chainage
def vertices(geom):
    ch = 0
    last = None
    
    for v in geom.vertices():#iterator of QgsPoint
        if last:
            ch += v.distance(last)
        yield (v.x(),v.y(),ch)
        last = v
        

if __name__ =='__console__':
    layer = QgsProject.instance().mapLayersByName('network')[0]
    for feat in layer.getFeatures():
        #interpolator = section_interpolator.sectionInterpolator(feat.geometry())
        h = sectionHandler(feat.geometry())
        break
        
