import processing
import cProfile, pstats

import os

from console.console import _console
script = os.path.dirname(_console.console.tabEditorWidget.currentWidget().path)


def test1():
    
    p = { 'convertTo' : 2,
    'direction' : 'direc_code',
    'endDate' : 's_end_date',
    'endNode' : 'end_lrp_co',
    'function' : 'funct_name',
    'inputFolder' : 'C:\\Users\\drew.bennett\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\pts_tools\\convert_route\\test\\inputs',
    'label' : 'sect_label',
    'length' : 'sec_length',
    #'network' : 'S:/Drew/hapms network/network_with_nodes/network_with_nodes.shp',
    'network':r'C:\Users\drew.bennett\Documents\network_with_nodes\network_with_nodes.shp',
    'outputFolder' : 'C:\\Users\\drew.bennett\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\pts_tools\\convert_route\\test\\outputs\\\convert_folder',
    'reverseSecFileDirection' : False,
    'startDate' : 'start_date',
    'startNode' : 'start_lrp_' }

    r = processing.run('PTS tools:convert_route_folder',p)
    print(r)


if __name__=='__console__':

    with cProfile.Profile() as profiler:
        test1()
        
    f = os.path.join(script,'convert_folder_profile.txt')
   
    profiler.dump_stats(f)
        
    with open(f, 'w') as to:
        stats = pstats.Stats(profiler, stream=to)
        stats.sort_stats('cumtime')
        stats.print_stats()
        
  