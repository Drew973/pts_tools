import processing
from qgis.core import QgsField,QgsProcessing
from qgis.core import QgsVectorLayer
from qgis.PyQt.QtCore import QVariant


def dq(s):
    return '"%s"'%(s)
    
def addCombinedField(layer,fields,name='combined'):
    f = [dq(k) for k in fields]
    e='concat(%s)'%(",'|',".join(f))
    field = QgsField(name, QVariant.String )
    return layer.addExpressionField(e, field )#int id of field
    
#returns new layer
def multiFieldJoin(layer,dataLayer,joinFields,output='TEMPORARY_OUTPUT'):
    layerField = 'combined'
    dataField = 'combined'

    layerFieldId = addCombinedField(layer,joinFields.keys(),layerField)
    dataFieldId = addCombinedField(dataLayer,joinFields.values(),dataField)

    p = { 'DISCARD_NONMATCHING' : False, 'FIELD' : layerField, 'FIELDS_TO_COPY' : [], 'FIELD_2' : dataField, 'INPUT' : layer, 'INPUT_2' : dataLayer, 'METHOD' : 0, 'OUTPUT' : output, 'PREFIX' : '' }
    r = processing.run('native:joinattributestable',p)
    
    #remove virtual fields:
    layer.removeExpressionField(layerFieldId)
    dataLayer.removeExpressionField(dataFieldId)

    return r['OUTPUT']

def test1():
    split = QgsProject.instance().mapLayersByName('split layer')[0]
    data = QgsProject.instance().mapLayersByName('example_data')[0]
    atts = {'sect_label':'SectionID','subsection_id':'Sample Unit Id'}

    #add to map and legend
    QgsProject.instance().addMapLayer(multiFieldJoin(split,data,atts), True)
    
def test2():
    split = QgsProject.instance().mapLayersByName('split layer')[0]
    data = QgsProject.instance().mapLayersByName('example_data')[0]
    atts = {'sect_label':'SectionID','subsection_id':'Sample Unit Id'}

    #add to map and legend
    QgsProject.instance().addMapLayer(multiFieldJoin(split,data,atts), True)
    



def processFile(file,splitLayer,fields,output=QgsProcessing.TEMPORARY_OUTPUT):

    data = QgsVectorLayer(file,"data","ogr")

    #check fields of data.
    #split fields will exist because using fieldcombobox
    dataFields = data.fields().names()
    for f in fields.values():
        if not f in dataFields:
            print('error: {file} is missing field {field}'.format(field=f,file=file))
            return
    
    return multiFieldJoin(splitLayer,data,fields,output)

    
if __name__=='__console__':
    from qgis.core import QgsProject

    test1()
