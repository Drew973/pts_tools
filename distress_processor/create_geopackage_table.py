from qgis.core import QgsWkbTypes
from qgis.core import QgsVectorFileWriter,QgsCoordinateReferenceSystem,QgsCoordinateTransformContext


 #requires QgsWkbTypes.Type
def createGpkgLayer(gpkg, name,crs, fields,geomType=QgsWkbTypes.MultiLineString):
                                
    # To add a layer to an existing GPKG file, pass 'append' as True
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    options.layerName = name
    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer

    writer = QgsVectorFileWriter.create(
        gpkg,
        fields,
        geomType,
        QgsCoordinateReferenceSystem(crs),
        QgsCoordinateTransformContext(),
        options)
    del writer

    return True
   
if __name__ == '__console__':
    from qgis.core import QgsWkbTypes
    split = QgsProject.instance().mapLayersByName('split')[0]
    dest = r'C:\Users\drew.bennett\Documents\area 14 tool\geopackage approach\testImport.gpkg'

    data = QgsProject.instance().mapLayersByName('data')[0]
    fields = split.fields()
    fields.extend(data.fields())
    createGpkgLayer(dest, 'temp', split.crs(), fields,QgsWkbTypes.MultiLineString)
   