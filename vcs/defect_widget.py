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





from pts_tools.vcs.defect import defect, laneWidths, defectEnum
from matplotlib.patches import Rectangle
#from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np

LENGTH = 500



def toPatches(d):
   # return [Rectangle((d.startChain, d.left() - d.width), d.endChain, d.width, edgecolor='orange',facecolor='none', linewidth=2)]
       
    if d.defectType == defectEnum.OJ_N:
        return [Rectangle((d.startChain, d.left() - d.width), d.endChain, d.width, edgecolor = 'green', linewidth=2,facecolor='none',zorder=d.defectType.value)]
   
   
    return [Rectangle((d.startChain, d.left() - d.width), d.endChain, d.width,zorder=d.defectType.value)]



#2 = 
def setupAxis(axes,subplotNumber):
    axes.set_xlim((subplotNumber*LENGTH, subplotNumber*LENGTH+LENGTH))
    axes.set_ylim((laneWidths['CL3'][1], laneWidths['HS'][0]))
    edges = [laneWidths['HS'][0], 0, laneWidths['CL1'][1],
              laneWidths['CL2'][1], laneWidths['CL2'][0]]
    centers = [0.5 * (v[0] + v[1]) for v in laneWidths.values()]
    axes.set_yticks(centers, minor=False)
    axes.set_yticks(edges, minor=True)
    axes.set_yticklabels(laneWidths.keys(), minor=False)
    axes.yaxis.grid(True, which='minor')
    axes.xaxis.grid(True, which='major')
#    axes.xaxis.grid(True, which='minor')
    axes.set_xticks(np.arange(subplotNumber * LENGTH,subplotNumber*LENGTH + LENGTH,10),minor = True)



def plotDefects(defects,fig,plotNumber,section = 'unknown section'):
    axes = fig.get_axes()#list of axes
    print('axes',axes)
    fig.suptitle(section)
    
    for i,ax in enumerate(axes):    
        ax.cla()
        setupAxis(ax,plotNumber+i)
        for d in defects:
            for p in toPatches(d):
                ax.add_patch(p)
                
   # for d in defects:
     #   for p in toPatches(d):
       #     for ax in axes:
        #        ax.add_patch(p)





class defectWidget(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        #self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig, axes = plt.subplots(4)

        super(FigureCanvasQTAgg, self).__init__(self.fig)
        self.setParent(parent)
        self.number = None
        self.setNumber(0)


    def addDefects(self, defects):
        plotDefects(defects,self.fig,self.number)
        self.updateGeometry()
        self.draw()


    def setNumber(self, number):
        if number != self.number:
            self.number = number


    def setSection(self, section):
        pass


if __name__ in ('__console__','__main__'):
    
    w = defectWidget(width=5, height=4, dpi=100)

    defects = [defect(sec='s', lane='CL1,CL2', wheelTrack='F', startChain=10, defectType='OJ', endChain=70, severity='N'),
               defect(sec='s', lane='CL1,CL2', wheelTrack='F', startChain=50, defectType='HFSC', endChain=90, severity='')]

    w.addDefects(defects)
    w.show()
