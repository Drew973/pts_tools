# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 13:31:56 2023

@author: Drew.Bennett
"""

import os


sharedTestFolder = os.path.join(os.path.dirname(__file__))
networkWithNodes = os.path.join(sharedTestFolder,'hapms_network','network_with_nodes.shp')

networkWithMeasure = os.path.join(sharedTestFolder,'A12_with_measure.shp')

networkDbWithMeasure = os.path.join(sharedTestFolder,'A12_with_measure.sqlite|layername=a12_with_measure')

testDistresses = os.path.join(sharedTestFolder,'test_distresses.csv')
