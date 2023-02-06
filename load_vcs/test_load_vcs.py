# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 09:55:07 2023

@author: Drew.Bennett
"""

from pts_tools.shared_test import test_alg
from pts_tools import shared_test

from pts_tools.load_vcs import load_vcs_alg
import processing

import unittest
import os


#run and profile algorithms.
#haven't added them all yet.
class testAlg(unittest.TestCase):
    
    def setUp(self):
        pass
    
    
    #test and profile split_by_chainage
    def testloadVcs(self):
        
        folder = os.path.dirname(load_vcs_alg.__file__)
        shared_test.networkWithMeasure
        
        params = { 'INPUT' : os.path.join(folder,'MFV2_044 Plotter.csv'),
          'OUTPUT' : 'TEMPORARY_OUTPUT',
          'end_label_field' : 'end Section ID',
          'end_measure_field' : 'end Chainage (m)',
          'end_offset_field' : 'end offset',
          #'network' : shared_test.networkWithMeasure,
          'network' : shared_test.networkDbWithMeasure,
          'network_label_field' : 'sect_label',
          'start_label_field' : 'start Section ID',
          'start_measure_field' : 'start Chainage (m)',
          'start_offset_field' : 'start offset',
          'width' : 'width' }

        
        pp = os.path.join(folder,'load_vcs.prof')
        
        test_alg.profileAlg(algId = 'PTS tools:load_vcs',params = params,profile = pp)
        
        
        
    #test and profile split_by_chainage
    def testInvalidNetwork(self):
        
        folder = os.path.dirname(load_vcs_alg.__file__)
        shared_test.networkWithMeasure
        
        params = { 'INPUT' : os.path.join(folder,'MFV2_044 Plotter.csv'),
          'OUTPUT' : 'TEMPORARY_OUTPUT',
          'end_label_field' : 'end Section ID',
          'end_measure_field' : 'end Chainage (m)',
          'end_offset_field' : 'end offset',
          'network' : shared_test.networkWithNodes,
          'network_label_field' : 'sect_label',
          'start_label_field' : 'start Section ID',
          'start_measure_field' : 'start Chainage (m)',
          'start_offset_field' : 'start offset',
          'width' : 'width' }

        
        #pp = os.path.join(folder,'load_vcs.prof')
        
        r = processing.runAndLoadResults('PTS tools:load_vcs',params)

if __name__ == '__console__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testAlg)
    unittest.TextTestRunner().run(suite)