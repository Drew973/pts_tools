# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:24:59 2024

@author: Drew.Bennett


import os
import sys
folder = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
#print(folder)
if not folder in sys.path:
    sys.path.append(folder)

"""





from pts_tools.vcs.defect import defect, defectEnum
from pts_tools.vcs.lanes import lanes

#from PyQt5.QtPrintSupport import QPrinter
#from PyQt5.QtGui import QPainter

from matplotlib.patches import Rectangle
#from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np

LENGTH = 500



def toPatches(d,roadLanes = lanes.fromString('HS,CL1,CL2,CL3')):
    left = d.leftOffset(roadLanes = roadLanes) 
    if d.defectType == defectEnum.OJ_N:
        return [Rectangle((d.startChain, left - d.width), d.endChain, d.width, edgecolor = 'green', linewidth=2,facecolor='none',zorder=d.defectType.value)]
   # higher zorder = on top
    return [Rectangle((d.startChain, left - d.width), d.endChain, d.width,zorder=d.defectType.value)]



def setupAxis(axes , subplotNumber , roadLanes = lanes.fromString('HS,CL1,CL2,CL3')):
        
    edges = roadLanes.roadEdges(roadLanes)
    
    centers = [(edges[i] + edges[i+1])/2 for i,v in enumerate(edges[:-1])]
    
    axes.set_xlim((subplotNumber*LENGTH, subplotNumber*LENGTH+LENGTH))
    axes.set_ylim(0,max(edges))
    axes.set_yticks(centers, minor=False)
    axes.set_yticks(edges, minor=True)
    axes.set_yticklabels(roadLanes.names(), minor=False)
#    axes.xaxis.grid(True, which='minor')
    axes.set_xticks(np.arange(subplotNumber * LENGTH,subplotNumber*LENGTH + LENGTH,10),minor = True)
    axes.set_xticks(np.arange(subplotNumber * LENGTH,subplotNumber*LENGTH + LENGTH+100,100),minor = False)

    axes.yaxis.grid(True, which='minor')
    axes.xaxis.grid(True, which='major')#zorder ignored here for some reason.
    axes.set_axisbelow(False)

    

def plotDefects(defects,fig,plotNumber,section = 'unknown section'):
    axes = fig.get_axes()#list of axes
   # print('axes',axes)
    for i,ax in enumerate(axes):    
        ax.cla()
        setupAxis(ax,plotNumber*len(axes)+i)
        for d in defects:
            for p in toPatches(d):
                ax.add_patch(p)
    fig.suptitle(section,fontsize = 12 )
    fig.tight_layout(rect=[0, 0, 1, 0.95])
   # for d in defects:
     #   for p in toPatches(d):
       #     for ax in axes:
        #        ax.add_patch(p)


class defectWidget(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.sec = ''
        self.defects = {}
        self.fig, axes = plt.subplots(4)
        super(FigureCanvasQTAgg, self).__init__(self.fig)
        self.setParent(parent)
        self.number = 0
        self.setNumber(0)


    def addDefects(self, defects):
        for d in defects:
            if d.sec in self.defects:
                self.defects[d.sec].append(d)
            else:
                self.defects[d.sec] = [d]
        
        
    def setNumber(self, number):
        if number != self.number:
            self.number = number
            self.setSection(self.sec)


    def setSection(self, section):
        self.sec = section
        if section in self.defects:
            plotDefects(self.defects[section],self.fig,self.number,section = self.sec)
        else:
            plotDefects([],self.fig,self.number,section = self.sec)
        self.updateGeometry()
        self.draw()


    def save(self,file):
        self.fig.savefig(file)
        '''
        printer =  QPrinter(QPrinter.ScreenResolution)
       # printer =  QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(file)
        painter = QPainter()
        if painter.begin(printer):
            self.render(painter)
            painter.end()
        else:
            raise ValueError('could not begin painting')
        '''
            

if __name__ in ('__console__','__main__'):
    import os
    from pts_tools.vcs import test
    w = defectWidget(width=5, height=4, dpi=100)
    defects = [defect(sec='s', lane='CL2', wheelTrack='F', startChain=10, defectType='OJ', endChain=125, severity='N',width = 1),
               defect(sec='s', lane='CL1,CL2', wheelTrack='F', startChain=90, defectType='HFSC', endChain=200, severity = '' , width = 3.65*2)]
    w.addDefects(defects)
    w.setSection('s')
    w.setNumber(0)
    w.show()
    f = os.path.join(os.path.dirname(test.__file__),'test_plot.pdf')
    print(f)
    w.save(f)