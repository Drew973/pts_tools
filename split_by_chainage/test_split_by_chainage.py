from qgis.core import QgsProject
import cProfile,pstats


def test1():
    print('test1')
    from qgis import processing
    layer = QgsProject.instance().mapLayersByName('test_network')[0]
    r = processing.run('PTS tools:split_by_chainage', { 'FIELD' : '', 'INPUT' : layer, 'OUTPUT' : 'TEMPORARY_OUTPUT', 'STEP' : 100 })
    QgsProject.instance().addMapLayer(r['OUTPUT'])
    


def test():
    with cProfile.Profile() as profiler:
        test1()
        
    f = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\tests\split_by_chainage_profile.txt'
    f2 = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\tests\split_by_chainage_profile.prof'
   
    profiler.dump_stats(f2)
    with open(f, 'w') as to:
        stats = pstats.Stats(profiler, stream=to)
        stats.sort_stats('cumtime')
        stats.print_stats()




if __name__ == '__console__':
    test()