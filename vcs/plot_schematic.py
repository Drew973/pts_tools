# -*- coding: utf-8 -*-
r"""
Created on Fri May 24 13:58:16 2024

@author: Drew.Bennett


mypy C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\vcs\plot_schematic.py
python C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\vcs\plot_schematic.py

"""
#from qgis.core import QgsGeometry
#print('qgis imported')



#from matplotlib.patches import Rectangle # type: ignore
from matplotlib.backends.backend_pdf import PdfPages # type: ignore
import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore
#from pts_tools.vcs.defect import defectEnum # type: ignore
#from pts_tools.shared_functions.intervals import intervals
#from pts_tools.vcs.lanes import lanes # type: ignore
from pts_tools.vcs.defect import defect , defaultRoadLanes, defectEnum , toPatch

YSCALE = 100#pixels per meter of road
#want HS at top of graph.


from typing import List,Dict,Tuple


def plotLegend(fig):
    patches = [toPatch(d) for d in defectEnum]
    #print('patches' , patches)
    fig.legend(handles = patches , loc = 'top' , ncol = 6,fontsize = 5,markerscale = 2)
    

#dict of sec:(type,xy)
def plotSections(defects :List[defect], file:str = '' , subplotLength: int = 500 , n:int = 4 , roadLanes: Dict [str,Tuple[float,float]] = defaultRoadLanes):
    #print('defects',defects)
    sections = {}
    for d in defects:
        if d.sec in sections:
            sections[d.sec].append(d)
        else:
            sections[d.sec] = [d]
    
    #print('sections',sections)
    fig , axes = plt.subplots(n)
    plotLegend(fig)
    edges = [10.95, 7.3, 3.65, 0.0 , -3.3]
    centers = [(edges[i] + edges[i+1])/2 for i,v in enumerate(edges[:-1])]
    #print('centers' , centers , 'edges' , edges)
    maxOffset = max(edges)
    minOffset = min(edges)
    
    for ax in axes:
        ax.set_ylim(minOffset,maxOffset)
        ax.set_yticks(centers, minor=False)
        ax.set_yticks(edges, minor=True)
        ax.set_yticklabels(reversed([k for k in roadLanes.keys()]), minor=False)
        ax.yaxis.grid(True, which='minor')
        ax.xaxis.grid(True, which='major')#zorder ignored here for some reason.
        ax.set_axisbelow(False)
         
    #    fig.subplots_adjust(top=0.2)
        
    with PdfPages(file) as pdf:

        for sec,defects in sections.items():
            maxChainage = np.max([[d.endChain , d.startChain] for d in defects])
            for d in defects:
                for ax in axes:
                    ax.add_patch(d.toPatch(roadLanes = roadLanes))
                    
            fig.suptitle(sec,fontsize = 8, y = 0.8)
            fig.tight_layout(rect = [0, 0, 1, 0.8])
            lower = 0
            while lower < maxChainage:
                for a in axes:
                    a.set_xlim(lower,lower + subplotLength)
                    lower += subplotLength
                
            #fig.savefig(file)
            pdf.savefig(fig)
    
    
    