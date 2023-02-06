#make rectangle from bottom left corner, top right corner,width
#QgsPointXY
import numpy


from qgis.core import QgsGeometry,QgsPointXY,QgsPoint

#numpy array
def unitVector(vector):
    return vector/(vector**2).sum()**0.5

#angle in radians. negative for clockwise rotation.
#https://en.wikipedia.org/wiki/Rotation_matrix
def rotateVector(vector,angle):
    return numpy.matmul(vector,numpy.array([[numpy.cos(angle),-numpy.sin(angle)],[numpy.sin(angle),numpy.cos(angle)]]))


def pointToVector(p):
    return numpy.array([p.x(),p.y()])


def vectorToPointXY(v):
    return QgsPointXY(v[0],v[1])



#makes rectangle given 2 opposite corners and width
#2 possible ways to fit rectangle between pair of points.
#startLeft returns solution where start point s is bottom left and e is top right, otherwise bottom right -> top left

#def otherCorners (s : QgsPointXY, e : QgsPointXY,width : float, startLeft : bool) -> QgsGeometry:
def otherCorners(s,e,width,startLeft=True):
    sv = pointToVector(s)
    ev = pointToVector(e)

    se = ev-sv
    #D = distance between corners.
    #h^2 = D^2 - w^2
    height = numpy.sqrt((se**2).sum()-width*width)
    #print(height)
    
    a = numpy.arctan(width/height)
    if startLeft:
        a = - a
    
    uv = unitVector(rotateVector(se,a))
   
    c1 = vectorToPointXY(sv+height*uv)
    c2 = vectorToPointXY(ev-height*uv)
    
    return QgsGeometry.fromPolygonXY([[vectorToPointXY(sv),c1,vectorToPointXY(ev),c2,vectorToPointXY(sv)]])
    #last point needs to be same as 1st point
    #otherwise QGIS treats geometry as polygonM for some buggy reason
    

#linestringM.
#supports z dimension
#offset in crs units. negative for left
#returns QgsPoint
def interpolatePoint(geometry,measure,offset=0):
    p = None
    n = None
    for v in geometry.vertices():
        if p is None or v.m()< measure:
            p = v
        
        if v.m()>measure:
            n = v
            break
            
    if n is None:
        n = v
        
    #vector notation
    #p = previous vertex or startPoint.
    #n = next vertex or end.
    #o = origin
    
    op =  numpy.array([p.x(),p.y(),p.z()]) 
    on =  numpy.array([n.x(),n.y(),p.z()]) 
    pn = on-op
    
    if n.m()-p.m()==0:
        print('next point',n)
        print('previous point',p)
        print(geometry)
        return QgsPoint()
    
    frac = (measure-p.m())/(n.m()-p.m())
   # print(pn[0:2])
    
    left = numpy.array([ pn[1],-pn[0]]) #(x,y) -> (y,-x)
    leftUnitVector = left/numpy.sqrt(numpy.sum(left**2))

   # print(leftUnitVector)

    v = op + frac * pn + numpy.append(leftUnitVector,0) * offset
    return QgsPoint(x=v[0],y=v[1],z=v[2],m=measure)




#QgsPoint
def interpolateBetweenPoints(s,e,fraction):
    sv = numpy.array([s.x(),s.y(),s.z(),s.m()])
    ev = numpy.array([e.x(),e.y(),e.z(),e.m()])
    v = sv + fraction * (ev-sv)
    return QgsPoint(v[0],v[1],v[2],v[3])
    


#def betweenMeasures(geom:QgsGeometry(linestringm),s:float,e:float -> QgsGeometry(linestringm))
def betweenMeasures(geom,s,e):
    
    if s>e:
        s,e = e,e
        flip = True
    else:
        flip = False
    
    points = []
    
    last = QgsPoint()
   # last = geom.vertexAt(0)
    
    
    for v in geom.vertices():
        #interpolate start point
        if last.m() < s and s < v.m():
            f = (s-last.m()) / (v.m()-last.m())            
            points.append(interpolateBetweenPoints(last,v,f))
            
            
        if s < v.m() and v.m() < e:
            points.append(v)
        
        #interpolate end point
        if last.m() < e and e < v.m():
            f = (e-last.m()) / (v.m()-last.m())
            points.append(interpolateBetweenPoints(last,v,f))
        
        if last.m()>e:
            break
        
            
        last = v
        
    if flip:
        points = reversed(points)
        
    return QgsGeometry.fromPolyline(points)
    

    
    
    