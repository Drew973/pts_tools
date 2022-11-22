# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:22:53 2022

@author: Drew.Bennett
"""
import os
import sys
from pathlib import Path


if __name__ == '__main__':
    p = Path(__file__).parents[3]
    if not p in sys.path:
        sys.path.append(str(p))



from pts_tools.load_hsrr import parse_readings


if __name__ == '__console__' or __name__=='__main__':
    testFolder = os.path.join(os.path.dirname(parse_readings.__file__),'test')

    print(testFolder)
    
    row = r'0.1000	01/09/2022 10:29:03	91	13	120	21	37		-41	5	85.24		-1.63898833	55.06820167	-1.63939833	55.06908167	-	-	-	=HYPERLINK("AREA 14 A1M NB CL1/0.001_1348801.jpg","0.001_1348801.jpg")	=HYPERLINK("AREA 14 A1M NB CL1/0.012_1349301.jpg","0.012_1349301.jpg")	=HYPERLINK("AREA 14 A1M NB CL1/0.023_1349801.jpg","0.023_1349801.jpg")	=HYPERLINK("AREA 14 A1M NB CL1/0.035_1350302.jpg","0.035_1350302.jpg")	=HYPERLINK("AREA 14 A1M NB CL1/0.046_1350802.jpg","0.046_1350802.jpg")	=HYPERLINK("AREA 14 A1M NB CL1/0.057_1351302.jpg","0.057_1351302.jpg")	=HYPERLINK("AREA 14 A1M NB CL1/0.069_1351804.jpg","0.069_1351804.jpg")	=HYPERLINK("AREA 14 A1M NB CL1/0.081_1352306.jpg","0.081_1352306.jpg")	=HYPERLINK("AREA 14 A1M NB CL1/0.092_1352807.jpg","0.092_1352807.jpg")		'
    r = parse_readings.parseRow(row)
    
    
    f = os.path.join(testFolder,'A1M NB RE.xls')
    
    for i,r in enumerate(parse_readings.parseReadings(f)):
        if i<10:
            print(r)
            print(r.isValid())