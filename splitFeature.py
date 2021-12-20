from PyQt5.QtCore import QVariant

import numpy

from qgis.core import QgsField,QgsFeature,QgsGeometry
from . substring import substring


def splitFeature(feature,step=10,field=None):
    
    fields=feature.fields()
    fields.append(QgsField('start_chainage', QVariant.Double))
    fields.append(QgsField('end_chainage', QVariant.Double))
    
    g = QgsGeometry(feature.geometry())
    g.convertToSingleType()
    
    geomLength = g.length()
    
    if field:
        length = feature[field]
    else:
        length = geomLength
    
    #print('length:',length,'step:',step)
    
    chainages = numpy.arange(0,length,step)
    
    if chainages[-1] < length:
        chainages = numpy.append(chainages,length)
            
    for i,v in enumerate(chainages[0:-1]):
        f = QgsFeature(fields)
        f.setAttributes(feature.attributes()+[float(v),float(chainages[i+1])])
        
        f.setGeometry(substring(g
            ,v*geomLength/length
            ,chainages[i+1]*geomLength/length))
        yield f
        

if __name__ == '__console__':

    layer = iface.activeLayer()   
    feature = layer.selectedFeatures()[0]
    print([f['start_chainage'] for f in splitFeature(feature)])
    
