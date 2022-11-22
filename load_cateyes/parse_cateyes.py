# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 15:38:36 2022

@author: Drew.Bennett
"""

from PyQt5.QtCore import QVariant

from qgis.core import QgsGeometry,QgsPointXY,QgsFeature,QgsField,QgsFields,QgsCoordinateTransform,QgsCoordinateReferenceSystem,QgsProject


fields = QgsFields()
fields.append(QgsField('run',QVariant.String))
fields.append(QgsField('s_ch',QVariant.Double))
fields.append(QgsField('e_ch',QVariant.Double))
fields.append(QgsField('raw_ch',QVariant.Double))
fields.append(QgsField('timestamp',QVariant.String))
#fields.append(QgsField('timestamp',QVariant.DateTime))
fields.append(QgsField('eye_count',QVariant.Double))
fields.append(QgsField('f_line',QVariant.Int))


outputCrs = QgsCoordinateReferenceSystem("EPSG:27700")

transform = QgsCoordinateTransform(QgsCoordinateReferenceSystem("EPSG:4326"),
                                   QgsCoordinateReferenceSystem("EPSG:27700"), QgsProject.instance())

#fields = [r]
#[raw_ch,timestamp,eyecount,geom]

def parseRow(line):
    
    try:
        split = line.strip().split('\t')
        p1 = QgsPointXY(float(split[3]),float(split[4]))
        p2 = QgsPointXY(float(split[5]),float(split[6]))
        f = QgsFeature(fields)
        
        if p1.x()!=p2.x() and p1.y()!=p2.y():
            
            f['raw_ch'] = float(split[0])
            f['timestamp'] = str(split[1])
            f['eye_count'] = int(split[2])
            
            g = QgsGeometry().fromPolylineXY([p1,p2])
            g.transform(transform)
            f.setGeometry(g)
            return f
      
       #     return [float(split[0]),#raw_ch
       #                 str(split[1]),#timestamp
      #                  int(split[2]),#eye_count
    #                    QgsGeometry().fromPolylineXY([p1,p2])#geom
        #                ]
        
    except Exception as e:
        pass
        
        
                
'''
    cateyes spreadsheet to QgsFeature(s)
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
            
            

