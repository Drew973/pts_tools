# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 08:42:44 2022

@author: Drew.Bennett
"""

import processing
import cProfile, pstats
import os


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
def profilePath(module,name='profile.prof'):
    return os.path.normpath(os.path.join(os.path.dirname(module.__file__),name))
    
