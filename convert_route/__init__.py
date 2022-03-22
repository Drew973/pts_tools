# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 09:25:18 2022

@author: Drew.Bennett
"""

import os
import sys

folder = os.path.dirname(os.path.realpath(__file__))

if not folder in sys.path:
    sys.path.append(folder)
