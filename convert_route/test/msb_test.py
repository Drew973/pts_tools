import unittest


import importlib

    
import pts_tools




class TestModel(unittest.TestCase):
    
    def setUp(self):
        
        self.layer = QgsProject.instance().mapLayersByName('network_with_nodes')[0]

        self.fields = {'label': 'sect_label', 'section_direction': 'direc_code', 'length': 'sec_length',
        'start_node': 'start_node', 'end_node': 'end_node', 'start_date': 'start_date', 'end_date': '',
        'function': 'funct_name'}
    
    def testSecToSec(self):
        m = manual_sec_builder.msbModel.msbModel()
       
        inputFile = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\convert_route\test\inputs\test_sec.sec'
        with open(i,'r') as f:
            m.loadSec(f,False)

        outputFile = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\convert_route\test\outputs\test_sec.sec'
        with open(i,'w') as f:
            m.save(f,self.layer,self.fields)
            
        with open(inputFile,'r') as f:
            a = f.read()
            
        with open(outputFile,'r') as f:
            b = f.read()
            
        self.assertEqual(a,b)
        
        
   # def run(self,result):
       # self.testSecToSec()
        
        
unittest.main()
        