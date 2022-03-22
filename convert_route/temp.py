# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 08:40:12 2022

@author: Drew.Bennett
"""


import os
import sys

toolsFolder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

if not toolsFolder in sys.path:
    sys.path.append(toolsFolder)
    
    
from rte import read


class loadRteTest:
    
    
#f is file like object with readlines() method
#returns number of rows added.
#inserts new rows at row. Clears if None.
    def loadRte(self,f,row=None):
                
        if row is None:
            self.clear()
            #self.setHorizontalHeaderLabels(self.headerLabels)
            row = 0


        R2_1s = []
       # R4_1s = []
        sectionDirections = {}

        for i,line in enumerate( f.readlines()):
            if i==0:
                n = int(line[63:69])

            if i>0 and i<=n+1:
                R2_1s.append(read.readR2_1(line))

            if i>n+2:
                r = read.readR4_1(line)
                sectionDirections[r['section_label']] = r['section_direction']
              #  R4_1s.append(read.readR4_1(line))


        
        
        for r in R2_1s:
            sec = r['section_label']
            
            if sec:
                sectionDirection = sectionDirections[sec]
                self.addRow(row,r['section_label'],isReversed = sectionDirection!=r['direction'])
        
            else:
                self.addDummy(row)
        
            row +=1
                
        #4.1s are sorted alphabetically
        #2.1s are in order of route
        
        

    def clear(self):
        pass
    
    def setHorizontalHeaderLabels(self,labels):
        pass
    
    
    def addDummy(self,row):
        pass
    
t = loadRteTest()

file = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\convert_route\test\inputs\test_rte.rte'

with open(file,'r') as f:
    t.loadRte(f)
    