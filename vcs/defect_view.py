# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 08:31:00 2024

@author: Drew.Bennett
"""


from PyQt5.QtCore import Qt,QRectF

from PyQt5.QtWidgets import QGraphicsScene,QGraphicsView
from pts_tools.vcs.defect_item import LINES,PIXELS




class defectView(QGraphicsView):
    
    
    def __init__(self,scene,parent=None):
        super().__init__(scene,parent)
        #self.addLine
        self.setPlotNumber(0)
        
        

    #0 indexed
    def setPlotNumber(self,number):
        self.number = number
        self.fit()
        
        
    def fit(self):
        rect = QRectF(self.number*PIXELS,0,PIXELS,LINES)
        self.fitInView(rect)


    def resizeEvent(self,event):
        #event.size()
        self.fit()