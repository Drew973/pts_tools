# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 10:13:56 2023

@author: Drew.Bennett
"""


from pts_tools.shared_functions import geometry_functions
from qgis.core import QgsGeometry,QgsPointXY,QgsPoint


import unittest


testMultilinestringM = QgsGeometry.fromWkt('MultiLineStringM ((615324.83299999998416752 228161.17700000002514571 0, 615369.1909999999916181 228184.81699999998090789 50.26412004599870187, 615712.10499999998137355 228374.31400000001303852 442.05376310079560653, 615826.76000000000931323 228436.71500000002561137 572.58978811308088552, 615899.15599999995902181 228471.625 652.9632222564030144, 615968.67700000002514571 228500.70100000000093132 728.31959701666630735, 616039.34199999994598329 228526.58600000001024455 803.57632728040607617, 616111.26399999996647239 228549.018999999971129 878.91565016693857615, 616189.20100000000093132 228568.80599999998230487 959.32523503096967943, 616258.11699999996926636 228582.78499999997438863 1029.64470244217386607, 616332.39099999994505197 228594.57000000000698492 1104.84784932444972583, 616417.38500000000931323 228603.3879999999771826 1190.2980521329302519, 616502.81099999998696148 228607.65500000002793968 1275.83055335320682389, 616879.53000000002793968 228617.79899999999906868 1652.68610352731548119, 616985.15800000005401671 228620.90799999999580905 1758.35984797221294684, 617057.7780000000493601 228626.99200000002747402 1831.23425675883504482))')




#run and profile algorithms.
#haven't added them all yet.
class testGeomFunctions(unittest.TestCase):
    
    def setUp(self):
        pass
    
    
    #test and profile split_by_chainage
    def testBetweenMeasures(self):
        r = geometry_functions.betweenMeasures(testMultilinestringM,100,1000)
        print(r)
     
     
    def testInterpolateBetweenPoints(self):
        s = QgsPoint(10,10,10,10)#xyzm
        e = QgsPoint(20,20,20,20)
        r = geometry_functions.interpolateBetweenPoints(s,e,0.5)
        self.assertEqual(r.x(),15)
        self.assertEqual(r.y(),15)
        self.assertEqual(r.z(),15)
        self.assertEqual(r.m(),15)



    def testOtherCorners(self):
        s = QgsPointXY(1,1)
        e = QgsPointXY(10,10)
        print(geometry_functions.otherCorners(s,e,9,True))#solution is square
        print(geometry_functions.otherCorners(s,e,1,True))


if __name__ == '__console__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testGeomFunctions)
    unittest.TextTestRunner().run(suite)