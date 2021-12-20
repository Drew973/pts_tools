
from qgis.core import QgsPoint,QgsGeometry

#how the hell does qgis not have this?!
#is in expression generator but how to use?

#shapely version too old for shapely.substring.

#QgsGeometry,start distance, end distance
def substring(geometry,start,end):
    
    #print('start:',start,'end:',end)
    #geometry.convertToSingleType()
        
    length = geometry.length()
   
    if start>length:
        raise ValueError('start > geometry length')

    if end<0:
        raise ValueError('end < 0')
        
    ch = 0
    last = None
    points = []
    
    s = QgsPoint()
    s.fromWkt(geometry.interpolate(start).asWkt())
    points.append(s)
  
    for v in geometry.vertices():
        if not last is None:
            ch += v.distance(last)
        last = v
        
        if start<ch and ch<end:
            points.append(v)
            #print(v,ch)

        if ch>=end:
            break
        
    if end>length:
        end = length
        
    e = QgsPoint()
    e.fromWkt(geometry.interpolate(end).asWkt())
    points.append(e)
        
    #print(points)
    return QgsGeometry.fromPolyline(points)#qgspoints
    #QgsLineString(points)

if __name__ == '__console__':
    layer = iface.activeLayer()
        #fields = layer.fields()
        #fields.append(QgsField('start_chainage', QVariant.Double))
        #fields.append(QgsField('end_chainage', QVariant.Double))
        
    feature = layer.selectedFeatures()[0]
    print(substring(feature.geometry(),0,10))