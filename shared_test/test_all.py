# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 11:28:27 2023

@author: Drew.Bennett



unit test per procossing algorithm. run only that test after changing algorithm.
run all tests after changing shared code.

"""

from unittest import TestLoader, TextTestRunner, TestSuite


from pts_tools.point_from_lrs.test_point_from_lrs import testPointFromLrs
from pts_tools.polygon_from_lrs.test_polygon_from_lrs import testPolygonFromLrs
from pts_tools.line_from_lrs.test import testLineFromLrs
from pts_tools.curvature.test_estimate_curvature import testEstimateCurvature
from pts_tools.curvature.test_extract_curved import testExtractCurved




if __name__ in ("__main__",'__console__'):

    loader = TestLoader()
    tests = [
        loader.loadTestsFromTestCase(test)
        for test in [testPointFromLrs,testPolygonFromLrs,testLineFromLrs,testEstimateCurvature,testExtractCurved]
    ]
    suite = TestSuite(tests)

    runner = TextTestRunner(verbosity=2)
    runner.run(suite)