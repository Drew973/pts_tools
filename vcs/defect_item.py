# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 08:04:44 2024

@author: Drew.Bennett
"""
from PyQt5.QtCore import Qt,QRectF,QLineF
from PyQt5.QtWidgets import QGraphicsRectItem,QGraphicsLineItem
from pts_tools.vcs.defect import defect,left,defectEnum,laneWidths
from PyQt5.QtGui import QBrush,QColor,QPen



BRUSHES = {}
PENS = {defectEnum.LP : QPen(Qt.black,2,Qt.DashDotLine,Qt.SquareCap, Qt.RoundJoin),
        defectEnum.OJ_N: QPen(Qt.green,2,Qt.SolidLine,Qt.SquareCap, Qt.RoundJoin),
        'line': QPen(Qt.blue,1,Qt.DashLine,Qt.SquareCap, Qt.RoundJoin)}

HEIGHT = 10.95
LINES = 100

WIDTH = 500
PIXELS = 500


#offset = L,line = 0
#offset = R,line = LINES
#offset in m
def offsetToLine(offset):
    L = laneWidths['HS'][0]
    R = laneWidths['CL3'][1]
   # offset-L/abs(L-R)
    return LINES * -(offset - L) / abs(L - R)


def chainageToPixel(chainage):
    return PIXELS*chainage/WIDTH


def convertHorizontal(rect):
    L = chainageToPixel(rect.left())
    R = chainageToPixel(rect.right())
    T = offsetToLine(rect.top())
    B = offsetToLine(rect.bottom())   
    return QRectF(L, B, R - L, T - B)


class horizontalDefectItem(QGraphicsRectItem,defect):
    
    
    def __init__(self,sec,lane,wheelTrack,startChain,defectType,severity = '',photo = '',width = None,endChain=None,parent = None):        
        #this works ... somehow
        super().__init__(sec = sec, lane = lane, wheelTrack = wheelTrack, startChain = startChain,
                        defectType = defectType, severity = severity, photo = photo, width = width, endChain = endChain)

        #QGraphicsRectItem.__init__(self,parent)#TypeError: __init__() missing 6 required positional arguments: 'sec', 'lane', 'wheelTrack', 'startChain', 'defectType', and 'severity'
       #WTF?
        #defect.__init__(self,sec = sec, lane = lane, wheelTrack = wheelTrack, startChain = startChain,
                        #defectType = defectType, severity = severity, photo = photo, width = width, endChain = endChain)


        self.updateRect()
        
        
        
    def rect(self):
        return convertHorizontal(QRectF(self.startChain,
                      left(self.lanes,self.wheelTrack),
                      self.endChain-self.startChain,
                      self.width
                      ))

    def updateRect(self):
        self.setRect(self.rect())
        self.setZValue(self.defectType.value)
        if self.defectType in BRUSHES:
            self.setBrush(BRUSHES[self.defectType])
        if self.defectType in PENS:
            self.setPen(PENS[self.defectType])



#print QGraphicsScene to pdf with QGraphicsScene.render(QPainter)
if __name__ in ('__main__','__console__'):
    from PyQt5.QtWidgets import QGraphicsView,QGraphicsScene
    from PyQt5.QtGui import QPainter
    from PyQt5.QtPrintSupport import QPrinter
    from pts_tools.vcs.defect_view import defectView
    import numpy as np
    scene = QGraphicsScene()
    view = defectView(scene)
    
    
   # r = QRectF(0,0,PIXELS,LINES)
   # view.setSceneRect(r)
    #view.fitInView(rect)
    edges = np.unique([v[0] for v in laneWidths.values()] + [v[1] for v in laneWidths.values()] )
    
    
    
    for e in edges:
        v = float(offsetToLine(e))
        print('v',v)
    #    line = QLineF(0,v,9999999999999,v)
    #    print(line)
      #  li = QGraphicsLineItem(line)
       # li.setPen(PENS['line'])
        lineItem = scene.addLine(0.0,v,9999999,v,PENS['line'])#too large a number causes line not to show.
        lineItem.setZValue(0)
    
    
    scene.addSimpleText('HS')
    
    d = horizontalDefectItem(sec = 's',lane = 'CL1,CL2',wheelTrack = 'F',startChain = 10,defectType = 'LP',endChain = 50,severity = '')
    scene.addItem(d)
    print('rect',d.rect())
    scene.addItem(horizontalDefectItem(sec = 's',lane = 'CL1,CL2',wheelTrack = 'F',startChain = 60,defectType = 'OJ',endChain = 70,severity = 'N'))
      
    view.show()
  #  view.fitInView(scene.sceneRect())
    
    #printer = QPrinter(QPrinter.HighResolution);
    #printer.setOutputFormat(QPrinter.PdfFormat);
    #printer.setOutputFileName(r"C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\vcs\test.pdf");
    #painter = QPainter(printer)
    #view.render(painter)
    #painter.end()

    