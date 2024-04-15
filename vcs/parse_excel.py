# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 15:11:05 2024

@author: Drew.Bennett


python_calamine documentation horribly out of date.

"""


#0 indexed
#replace with json config file?
T = {'lane':0,'startChain':1,'endChain':2,'width':4,'defectType':6,'wheelTrack':8,'photo':9,'minRow':20,'maxRow' : 42,'secRow':8,'secCol':5}

from pts_tools.vcs.defect import defect
import traceback

#['CL2', 20.0, '', 0.5, 0.5, 0.25, 'IW', '', 'R', '', -348.0, '', '', '', '', '', '', '']


def parseExcel(filePath,feedback):
    try:
        import python_calamine
        names = python_calamine.get_sheet_names(filePath)
        #print('names',names)
        
        
        #errorLog = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\vcs\errors.txt'
        #log = open(errorLog,'w')
        for sheetNumber,sheetName in enumerate(names):
            
            feedback.setProgress(100*sheetNumber/len(names))
            if feedback.isCanceled():
                return
            
            if 'VCS' in sheetName.upper():
                d = python_calamine.get_sheet_data(filePath,sheetNumber)#list of lists                
                sec = d[T['secRow']][T['secCol']]
                
                #for row in d[T['minRow']:T['maxRow']]:
                #empty rows not in d?
                for row in d:
                    #print('row',row)
                    try:
                        yield defect(lane = row[T['lane']],
                                      startChain = row[T['startChain']],
                                      endChain = row[T['endChain']],
                                      width = row[T['width']],
                                      wheelTrack = row[T['wheelTrack']],
                                      photo = row[T['photo']],
                                      defectType = row[T['defectType']],
                                      sec = sec
                                      )
                        
                    except Exception as e:
                        pass
                        #log.write(sheetName +' '+ str(row))
                   #     print(sheetName,row)
                        #traceback.print_exc(file = log)
                       #]pass
       # log.close()
            
    except ImportError:
        m = 'Could not import Calamine. If you just installed it try restarting QGIS.'
        #print(m)
        raise ImportError(m)
    

    
    
def test():
    f = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\vcs_to_gis\M18 - Site Sheets.xlsx'
    for d in parseExcel(f):
        print(d)
        break
    
if __name__ in ('__main__','__console__'):
    test()