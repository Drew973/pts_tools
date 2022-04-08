
from qgis.core import QgsPoint,QgsGeometry

#how does qgis not have this?!
#is in expression generator but how to use?

#shapely version too old for shapely.substring.

#QgsGeometry,start distance, end distance
def substring(geometry,start,end):
            
    if start<end:
        s = start
        e = end
    else:
        s = end
        e = start
        
    points = []
    
    # geometry.interpolate returns QgsGeometry. 
    for v in geometry.interpolate(s).vertices():
        points.append(v)
        
    points += [p for p,ch in chainages(geometry) if s<ch and ch<e]
  
    #interpolate and add end
    for v in geometry.interpolate(e).vertices():
        points.append(v)

    if end < start:
        points.reverse()
    
    return QgsGeometry.fromPolyline(points)#qgspoints



#generator returning vertex and chainage for geom vertices
def chainages(geom):
    ch = 0
    last = None
    
    for v in geom.vertices():
        if not last is None:
            ch += v.distance(last)
        last = v
        yield v,ch



if __name__ == '__console__':
    layer = iface.activeLayer()
        #fields = layer.fields()
        #fields.append(QgsField('start_chainage', QVariant.Double))
        #fields.append(QgsField('end_chainage', QVariant.Double))
        
    feature = layer.selectedFeatures()[0]
    print(substring(feature.geometry(),0,10))