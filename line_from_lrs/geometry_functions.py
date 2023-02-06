#make rectangle from bottom left corner, top right corner,width
#QgsPointXY
import numpy


from qgis.core import QgsGeometry,QgsPointXY

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

#finds other corners of rectangle given 2 opposite corners and width
# bottom left -> top right
def otherCorners(s,e,width,reverseDirection=False):
   # dx = e[0]-s[0]
   # dy = e[1] - s[1]
    se = pointToVector(e)-pointToVector(s)

    #D = distance between corners.
    #h^2 = D^2 - w^2
    height = numpy.sqrt(se[0]*se[0]+se[1]*se[1]-width*width)
    #print(height)
    
    a = numpy.arctan(width/height)
    if reverseDirection:
        a = - a
    
    uv = unitVector(rotateVector(se,a))
   
    c1 = vectorToPointXY(s+height*uv)
    c2 = vectorToPointXY(e-height*uv)

    return QgsGeometry.fromPolygonXY([[s,c1,e,c2]])
    

def test1():
    s = QgsPointXY(1,1)
    e = QgsPointXY(10,10)
    print(otherCorners(s,e,9,True))#solution is square
    print(otherCorners(s,e,1,True))

test1()