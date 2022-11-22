'''
    runs and profiles integration test for convert_route.
    tests reading and writing sec,rte,sr and that output is 
    same as input when 'converting' to same format
'''

import processing


import os
from os.path import dirname

from console.console import _console


from pts_tools.shared_test import test_alg

def folder():
    if __name__=='__console__':
        scriptPath = _console.console.tabEditorWidget.currentWidget().path
        return dirname(scriptPath)
    else:
        return dirname(__file__)
    
    
inputFolder = os.path.join(folder(),'inputs')    
outputFolder = os.path.join(folder(),'outputs')    



network = os.path.join(dirname(dirname(folder())),'shared_test','hapms_network','network_with_nodes.shp')    

    
p = {'section_direction' : 'direc_code',
    'endDate' : 's_end_date',
    'endNode' : 'end_lrp_co',
    'function' : 'funct_name',
    'label' : 'sect_label',
    'length' : 'sec_length',
    'network':test_alg.networkWithNodes,
    'reverseSecFileDirection' : False,
    'startDate' : 'start_date',
    'startNode' : 'start_lrp_' }
    

def testSecToSec():
    inputFile = os.path.join(inputFolder,'test_sec.sec')
    outputFile =os.path.join(outputFolder,'test_sec.sec')
    testSameToSame(inputFile,outputFile)


def testSrToSr():
    inputFile = os.path.join(inputFolder,'test_sr.sr')
    outputFile =os.path.join(outputFolder,'test_sr.sr')
    testSameToSame(inputFile,outputFile)


def testRteToRte():
    inputFile = os.path.join(inputFolder,'test_rte.rte')
    outputFile =os.path.join(outputFolder,'test_rte.rte')
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

def testConversions():
    testSecToSec()
    testSrToSr()
    testRteToRte()



if __name__ == '__console__':
    #suite = unittest.defaultTestLoader.loadTestsFromTestCase(testConvertRoute)
    #unittest.TextTestRunner().run(suite)
    testConversions()

