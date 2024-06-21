# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 10:54:05 2024

@author: Drew.Bennett

only certain combinations of type and severity valid. Enum seems like best way to validate.
"""


from enum import Enum

    
    
fullNames = {'HRA':'Hot Rolled Asphalt','HFSC' : 'High Friction Surface Coating','TSSC': 'Thin Surfacing','OJ_N':'Open Joint(narrow)',
             'OJ_M':'Open Joint(medium)','OJ_W':'Open Joint(wide)','CR_1':'Cracking(minor)','CR_2':'Cracking(major)',
             'TC_1':'Transverse Cracking(minor)','TC_2':'Transverse Cracking(major)','LP':'Loop','CJ':'Construction Joint',
             'BJ': 'Bridge Joint','N':'Nodes','IW':'Ironwork','CZ_1':'Crazing(minor)','CZ_2':'Crazing(major)',
             'FT_1':'Fatting(minor)','FT_2':'Fatting(major)','SD_1':'Surface Defect(minor)','SD_2':'Surface Defect(major)',
             'MP':'Mud Pumping','DEP':'Depression','POT':'Pothole','PA_1':'Patch(acceptable)','PA_2':'Patch(failure)'}
    
defectEnum = Enum('defectEnum',[k for k in fullNames.keys()])


def typeStr(tp:defectEnum) -> str:
    return tp.name.split('_')[0]


def severityStr(tp:defectEnum) -> str:
    v = tp.name.split('_')
    if len(v)>1:
        return v[1]
    return ''


def fullName(tp:defectEnum) -> str:
    return fullNames[tp.name]


def fromStrings(featType:str,sev:str) -> defectEnum:
    a = AZ(featType) 
    b = AZN(sev)
    if b:
        return defectEnum[ a + '_' + b ]
    return defectEnum[ a ]


#charactors from A-Z
def AZ(string:str) -> str:
    n = ''
    for c in string.upper():
        if c.isalpha():
            n += c
    return n


#charactors from A-Z and numbers
def AZN(string:str) -> str:
    n = ''
    for c in string.upper():
        if c.isalpha() or c.isnumeric():
            n += c
    return n
