'''
    runs and profiles integration test for convert_route.
    tests reading and writing sec,rte,sr and that output is 
    same as input when 'converting' to same format
'''

import processing
import cProfile, pstats

import os

from console.console import _console
script = os.path.dirname(_console.console.tabEditorWidget.currentWidget().path)

p = {'section_direction' : 'direc_code',
    'endDate' : 's_end_date',
    'endNode' : 'end_lrp_co',
    'function' : 'funct_name',
    'label' : 'sect_label',
    'length' : 'sec_length',
    'network':r'C:\Users\drew.bennett\Documents\network_with_nodes\network_with_nodes.shp',
    'reverseSecFileDirection' : False,
    'startDate' : 'start_date',
    'startNode' : 'start_lrp_' }
    
def testSecToSec():
    inputFile = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\convert_route\test\inputs\test_sec.sec'
    outputFile = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\convert_route\test\outputs\test_sec.sec'
    testSameToSame(inputFile,outputFile)

def testSrToSr():
    inputFile = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\convert_route\test\inputs\test_sr.sr'
    outputFile = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\convert_route\test\outputs\test_sr.sr'
    testSameToSame(inputFile,outputFile)

def testRteToRte():
    inputFile = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\convert_route\test\inputs\test_rte.rte'
    outputFile = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\convert_route\test\outputs\test_rte.rte'
    testSameToSame(inputFile,outputFile)
    
#check that 'converting' to same format doesn't change file.
def testSameToSame(inputFile,outputFile):

    params = {k:p[k] for k in p}
    params['inputFile'] = inputFile
    params['outputFile'] = outputFile

    processing.run('PTS tools:convert_route',params)

    with open(inputFile,'r') as f:
        a = f.read().strip()

    with open(outputFile,'r') as f:
        b = f.read().strip()
    
    assert a==b

def test():
    testSecToSec()
    testSrToSr()
    testRteToRte()


if __name__=='__console__':

    with cProfile.Profile() as profiler:
        test()
        
    f = os.path.join(script,'convert_route_profile.txt')
   
    profiler.dump_stats(f)
        
    with open(f, 'w') as to:
        stats = pstats.Stats(profiler, stream=to)
        stats.sort_stats('cumtime')
        stats.print_stats()