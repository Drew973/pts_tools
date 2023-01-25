# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 08:42:44 2022

@author: Drew.Bennett
"""

import processing
import cProfile, pstats

import os

from pts_tools import shared_test


#profile = file to save profile to
def profileAlg(algId,params,profile=None):
    
    pr = cProfile.Profile()
    pr.enable()
   # with cProfile.Profile() as profiler:#context manager not in earlier versions of cProfile
    r = processing.runAndLoadResults(algId,params)
    pr.disable()

   
    if profile:
        with open(profile, 'w') as to:
            stats = pstats.Stats(pr, stream=to)
            stats.sort_stats('cumtime')
            stats.print_stats()
            
    return r



#generate filepath for profile given module.
def profilePath(module):
    return os.path.normpath(os.path.join(os.path.dirname(module.__file__),'profile.prof'))
    


import unittest
#from pts_tools import add_measure
import pts_tools



#run and profile algorithms.
#haven't added them all yet.
class testAlg(unittest.TestCase):
    
    def setUp(self):
        pass
    
    
    #test and profile split_by_chainage
    def testAddMeasure(self):
        params = { 'INPUT' : shared_test.networkWithNodes,
        'OUTPUT' : 'TEMPORARY_OUTPUT',
        'endMeasureField' : 'sec_length',
        'start_measure_field' : '' }
        
        pp = profilePath(pts_tools.add_measure)
        
        profileAlg(algId = 'PTS tools:add_measure',params = params,profile = pp)
        

if __name__ == '__console__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testAlg)
    unittest.TextTestRunner().run(suite)