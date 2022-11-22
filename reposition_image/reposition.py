#QgsPointxy

from osgeo import gdal
def reposition(layer,topLeft,topRight,bottomLeft,bottomRight):
    
    layerFile = layer.dataProvider().dataSourceUri()
    
    
    
    

def reposition2(layer,topLeft,topRight,bottomLeft,bottomRight):
    
    layerFile = layer.dataProvider().dataSourceUri()
    
    ds = gdal.Open(layerFile, gdal.GA_Update)
    if ds:
        #ds.SetGeoTransform(None)
        #set gcps
        gcps = []
        gcps.append(gdal.GCP(topLeft.x(),topLeft.y(), 0, 0, 0))
        gcps.append(gdal.GCP(topRight.x(),topRight.y(), 0, layer.width(), 0))
        gcps.append(gdal.GCP(bottomLeft.x(),bottomLeft.y(), 0, 0, layer.height()))
        gcps.append(gdal.GCP(bottomRight.x(),bottomRight.y(), 0, layer.width(), layer.height()))
        
        print(gcps)
        ds.SetGCPs(gcps, ds.GetProjection())
        
        ds.SetProjection('ESPG:27700')
        ds = None


if __name__== '__console__':
    layer = QgsProject.instance().mapLayersByName('to_move')[0]

    points = [QgsPointXY(430548.990,487682.846),
    QgsPointXY(430548.654,487683.601),
    QgsPointXY(430548.235,487678.931),
    QgsPointXY(430553.521,487679.714)]

    reposition(layer,points[0],points[1],points[2],points[3])
