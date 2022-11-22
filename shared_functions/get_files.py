# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 15:57:09 2022

@author: Drew.Bennett
"""
import os



def getFiles(folder,exts=None):
    for root, dirs, files in os.walk(folder, topdown=False):
        for f in files:
            if os.path.splitext(f)[1] in exts or exts is None:
                yield os.path.join(root,f)
