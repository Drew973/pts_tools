import numpy as np


if __name__ =='__console__':
    import sys
    folder = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\extract_by_curvature'
    if not folder in sys.path:
        sys.path.append(folder)
        
    import section_interpolator

else:
    from . import section_interpolator
    from . import clumpArray


def processFeature(feature,threshold,resolution=5,lengthField=None):
    i = section_interpolator.sectionHandler(feature.geometry())
    ranges = i.radiLessThan(threshold,resolution)
    print(ranges)


#find ranges where condition met.
#range from first chainage where condition met t

if __name__ =='__console__':
    layer = QgsProject.instance().mapLayersByName('network')[0]
    feats = layer.selectedFeatures()
    for feat in feats:
        processFeature(feat,5000,lengthField='secLen')
        
        
        