# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 08:56:14 2024

@author: Drew.Bennett

shows message box to install python_calamine if not found

"""

import subprocess
from PyQt5.QtWidgets import QMessageBox


def checkCalamine():
    try:
        import python_calamine
    except ImportError:
        m = QMessageBox()
        m.setText("Calamine library not found. Install it now?")
        m.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        response = m.exec_()
        if response == QMessageBox.Yes:
            c = 'pip install python-calamine'
            subprocess.run(c)
   
       
if __name__ in ('__main__','__console__'):
    checkCalamine()