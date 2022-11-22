# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 08:42:44 2022

@author: Drew.Bennett
"""

import processing
import cProfile, pstats

import os


sharedTestFolder = os.path.join(os.path.dirname(__file__))
networkWithNodes = os.path.join(sharedTestFolder,'hapms_network','network_with_nodes.shp')


#profile = file to save profile to
def testAlg(algId,params,profile=None):
  
    with cProfile.Profile() as profiler:
        r = processing.runAndLoadResults(algId,params)
   
    if profile:
        with open(profile, 'w') as to:
            stats = pstats.Stats(profiler, stream=to)
            stats.sort_stats('cumtime')
            stats.print_stats()
            
    return r