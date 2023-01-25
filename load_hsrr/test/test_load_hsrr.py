# -*- coding: utf-8 -*-
"""
Created on Wed May  4 09:02:34 2022

@author: Drew.Bennett
"""
import os
import unittest

from pts_tools.shared_test import test_alg
from pts_tools.load_hsrr import load_hsrr

folder = os.path.dirname(load_hsrr.__file__)
testFolder = os.path.join(folder,'test')


def profile():
    params = { 'inputFile' : os.path.join(testFolder,'A1M NB RE.xls'), 
    'OUTPUT' : 'TEMPORARY_OUTPUT',
    }
    
    f = os.path.join(testFolder,'load_hsrr_profile.txt')
    print(params)
    test_alg.testAlg('PTS tools:load_hsrr',params,f)


class testLoadHsrr(unittest.TestCase):
    
    def setUp(self):
        pass
    
    
    #test and profile split_by_chainage
    def testProfile(self):
        profile()
    
    

if __name__ == '__console__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testLoadHsrr)
    unittest.TextTestRunner().run(suite)