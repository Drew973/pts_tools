from qgis.core import QgsFields,QgsField,QgsFeature,QgsCoordinateTransform,QgsCoordinateReferenceSystem,QgsProject,QgsGeometry,QgsPointXY
#from datetime import datetime
from PyQt5.QtCore import QVariant


'''
loading readings:

	need <=1 point per run chainage

	1st data line at 0m.
	add 100m per line after that. valid or not.

    extra 100m after gap between geometries
	run name = full filename. saves need to track file:run
	adjust run selecting widgets to display this nicely.

'''

transform = QgsCoordinateTransform(QgsCoordinateReferenceSystem("EPSG:4326"),
                                   QgsCoordinateReferenceSystem("EPSG:27700"), QgsProject.instance())
                                   
                                   
fields = QgsFields()
fields.append(QgsField('run',QVariant.String))
fields.append(QgsField('s_ch',QVariant.Double))
fields.append(QgsField('e_ch',QVariant.Double))
fields.append(QgsField('f_line',QVariant.Int))
#fields.append(QgsField('time',QVariant.DateTime))
fields.append(QgsField('time',QVariant.String))
fields.append(QgsField('rl',QVariant.Double))

#Qgis doesn't handle timestamps well.


#row to QgsFeature. wkt column for loading to databases.
def parseRow(row):
   
    try:
        row = row.lower().strip().split('\t')
        f = QgsFeature(fields)
       # f['time'] = datetime.strptime(row[1],r'%d/%m/%Y  %H:%M:%S')
        f['time'] = row[1]
        f['rl'] = row[2]
        g = QgsGeometry.fromPolylineXY([ QgsPointXY(float(row[12]),float(row[13])),QgsPointXY(float(row[14]),float(row[15]))])
        g.transform(transform)
        f.setGeometry(g)
        return f
        
    
    except Exception as e:
        return e
        
        
        
'''
    readings spreadsheet to QgsFeature(s)
'''
def parseReadings(readings):
    with open(readings,'r',encoding='utf-8',errors='ignore') as f:
        
        i = 1
        ch = 0
        last = None
        
        for line in f.readlines():
            r = parseRow(line)
           
            if isinstance(r,QgsFeature):
                    
                #add extra to chainage after gap between geometry. want 1 chainage:1 point.
                if isinstance(last,QgsFeature):
                    if last.geometry().distance(r.geometry())>100:
                        ch += 0.1
                    
                r['run'] = readings
                r['s_ch'] = ch
                r['e_ch'] = ch+0.1
                r['f_line'] = i
                
                if 'wkt' in fields.names():
                    r['wkt'] = r.geometry().asWkt()
                
                yield r
                
            i += 1
            ch += 0.1
            last = r
        
        
        




