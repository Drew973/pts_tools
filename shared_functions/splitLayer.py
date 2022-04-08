
from pts_tools import split
from pts_tools import substring
from qgis.core import QgsField,QgsFeature
from PyQt5.QtCore import QVariant


#source is QgsFeatureSource. 
#sink is QgsFeatureSink. 
#QgsVectorLayer is subclass of QgsFeatureSource and QgsFeatureSink. 
#feedback is QgsProcessingFeedback

def splitLayer(source,sink,step,field=None,feedback=None):
	
    # Compute the number of steps to display within the progress bar and
    # get features from source
    total = 100.0 / source.featureCount() if source.featureCount() else 0
    features = source.getFeatures()
    fields = sinkFields(source)    
        
    for current, feature in enumerate(features):
           
        # Stop the algorithm if cancel button has been clicked
        if not feedback is None:
            if feedback.isCanceled():
                break

        if field is None:
            length = feature.geometry().length()
            scale = 1
        else:
            length = feature[field]
            scale = feature.geometry().length()/length
                
        #geometry chainage = geometry length*nominal chainage/nominal length
            
        atts = feature.attributes()  #feature.attributes() is slow
        fid = feature.id()
            
        for startChain,endChain in split.split(length=length,step=step):
            f = QgsFeature(fields)
            f.setAttributes(atts+[fid,float(startChain),float(endChain)])
            f.setGeometry(substring.substring(feature.geometry(),startChain*scale,endChain*scale))
            sink.addFeatures([f])


        # Update the progress bar
        if not feedback is None:
            feedback.setProgress(int(current * total))
            
            
def sinkFields(source):
    fields = source.fields()
    fields.append(QgsField('source_id', QVariant.Int))
    fields.append(QgsField('start_chainage', QVariant.Double))
    fields.append(QgsField('end_chainage', QVariant.Double))
    return fields