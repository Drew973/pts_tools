# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 15:32:52 2022

@author: Drew.Bennett
"""
from qgis.core import (QgsProcessingAlgorithm,QgsProcessingParameterFeatureSink,QgsProcessingParameterString,QgsProcessingParameterMultipleLayers,
                       QgsWkbTypes,QgsProcessingParameterFile)


from . import parse_cateyes


from PyQt5.QtCore import Qt

from processing.gui.wrappers import WidgetWrapper
from qgis.PyQt.QtWidgets import QDateTimeEdit
from qgis.PyQt.QtCore import QCoreApplication, QDate



class DateTimeWidget(WidgetWrapper):
    """
    QDateTimeEdit widget with calendar pop up
    """

    def createWidget(self):
        self._combo = QDateTimeEdit()
        self._combo.setCalendarPopup(True)

        today = QDate.currentDate()
        self._combo.setDate(today)

        return self._combo

    def value(self):
        date_chosen = self._combo.dateTime()
        return date_chosen.toString(Qt.ISODate)
    
    


'''

would be good if could merge multiple files into 1 layer. 
or didn' overwrite output

'''


class loadCateyes(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile('inputFile', 'File to load',fileFilter='csv(*.csv)'))
        
       # p = QgsProcessingParameterMultipleLayers('inputFile', 'Files to load',optional=False)
        #p.createFileFilter('csv(*.csv)')
        #self.addParameter(p)

        
        self.addParameter(QgsProcessingParameterFeatureSink('OUTPUT',description='output layer',createByDefault=False,optional=False,defaultValue='TEMPORARY_OUTPUT'))

     #   param = QgsProcessingParameterString('test', 'Initial Date')
        #param.setMetadata({
       #     'widget_wrapper': {
       #         'class': DateTimeWidget}})

       # self.addParameter(param)




    def prepareAlgorithm(self, parameters, context, feedback):
        self.inputFile = self.parameterAsFile(parameters,'inputFile',context)
        self.sink,self.destId =  self.parameterAsSink(parameters,'OUTPUT',context,parse_cateyes.fields,QgsWkbTypes.LineString,parse_cateyes.outputCrs)
        return True
        

    def processAlgorithm(self, parameters, context, feedback):
        for f in parse_cateyes.parseReadings(self.inputFile):
            self.sink.addFeature(f)
        return {'OUTPUT':self.destId}
  
    
    def name(self):
        return 'load_cateyes'


    def displayName(self):
        return 'Load cateye readings'


    def group(self):
        return 'PTS tools'


    def groupId(self):
        return ''


    def createInstance(self):
        return loadCateyes()


    def shortHelpString(self):
        return  r'''<html><body>
        <p>Load cateye readings to layer.</p>
        </body></html>
        '''
        