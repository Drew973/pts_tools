# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 16:02:34 2022

@author: Drew.Bennett
"""


import unittest
import os


from pts_tools import load_cateyes
from pts_tools.shared_test import test_alg

testFile = os.path.normpath(os.path.join(os.path.dirname(load_cateyes.__file__),'test.csv'))

class testLoadCateyes(unittest.TestCase):
    
    def setUp(self):
        pass
    
    
    #test and profile split_by_chainage
    def test1(self):
        params = {'inputFile':testFile,'OUTPUT':'TEMPORARY_OUTPUT'}
        print(params)
        test_alg.testAlg('PTS tools:load_cateyes',params)
        
        

if __name__ == '__console__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testLoadCateyes)
    unittest.TextTestRunner().run(suite)