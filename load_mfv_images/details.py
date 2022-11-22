from pts_tools.load_mfv_images import generate_details,group_functions


from qgis.core import QgsProject
from qgis.core import QgsRasterLayer,QgsCoordinateReferenceSystem

#ORM would be better for this. sqlachemy not included with qgis.

class imageDetails:
    
    def __init__(self,filePath,run=None,imageId=None,name=None,groups=None):
        
        self.filePath = filePath
        
        if run is None:
            self.run = generate_details.generateRun(filePath)
        else:
            self.run = run
           
        if imageId is None:
            self.imageId = generate_details.generateImageId(filePath)
        else:
            self.imageId = imageId
            
        if name is None:
            self.name = generate_details.generateLayerName(filePath)
        else:
            self.name = name
            
        if groups is None:
            groups = generate_details.generateGroups2(self.run,generate_details.generateType(filePath))
        
        if isinstance(groups,str):
            self.groups = stringToList(groups)
            
        if isinstance(groups,list):
            self.groups =groups
    
    
    
    def __getitem__ (self,key):
        if key == 'filePath':
            return self.filePath
            
        if key == 'run':
            return self.run
       
        if key == 'imageId':
            return self.imageId   
    
        if key == 'name':
            return self.name   

        if key == 'groups':
            return self.groups
        
        if key =='extents':
            return None
            #return self.boundingBoxWkb()#slow due to osgeo._gdal.Dataset_GetGeoTransform being slow

        raise KeyError('imageDetails has no item {0}'.format(key))



    def __eq__(self,other):
        return self.filePath==other.filePath and self.layerName==other.self.layerName and self.groups==other.groups and self.run==other.run and self.imageId==other.imageId
    
    
    
    #self<other
    #order by run,imageId
    def __lt__(self,other):
        if self.run<other.run:
            return True
    
        if self.imageId<other.imageId:
            return True


    def __repr__(self):
        d = {'filePath':self.filePath,'run':self.run,'imageId':self.imageId,'name':self.name,'groups':self.groups}
        return '<imageDetails:{}>'.format(d)



    #load layer. expand expands group. show renders image.
    def load(self,show=True,expand=False,crs=QgsCoordinateReferenceSystem('EPSG:27700')):
              
        layer = self.getLayer(crs)
        
        group = group_functions.getGroup(self.groups)#0.146/28
        group.addLayer(layer)
                
        QgsProject.instance().addMapLayer(layer,False)#don't immediatly add to legend
        #addMapLayer
            
        node = group.findLayer(layer)
        node.setItemVisibilityChecked(show)#fast
        node.setExpanded(expand)
                
        
   #slow. no easy way to speed up.
    def getLayer(self,crs=QgsCoordinateReferenceSystem('EPSG:27700')):
        layer = QgsRasterLayer(self.filePath, self.name)
        layer.setCrs(crs)
        return layer
                
  
import json

#csv and database contain string.
def stringToList(text):
    try:
        return json.loads(text)
    except:
        print('Could not read list from {t}. Reverting to empty list.'.format(t=text))
        return []
    

#def fromDict(d):
   # return imageDetails(filePath=d['filePath'],run=find(d,'run'),imageId=find(d,'imageId'),name=find(d,'name'),groups=find(d,'groups'))



 #lookup value from dict, returning None if not present
def find(d,k):
    if k in d:
        return d[k]
        
        
if __name__=='__console__':
    file = r'C:\Users\drew.bennett\Documents\mfv_images\LEEMING DREW\TIF Images\MFV2_01\ImageInt\MFV2_01_ImageInt_000003.tif'
    data = [imageDetails(file)]
