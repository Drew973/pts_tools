
from pts_tools.shared_test.test_alg import profileAlg

params = { 'INPUT' : 'C:/Users/drew.bennett/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/pts_tools/vcs_to_gis/test..csv',
'OUTPUT' : 'TEMPORARY_OUTPUT',
'endChain' : 'end_chain', 
'featureType' : 'feature_type',
'lane' : 'lane',
'network' : 'C:/Users/drew.bennett/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/pts_tools/shared_test/network_with_m.gpkg',
'networkSec' : 'sect_label',
'sec' : 'sec', 
'startChain' : 'start_chain',
'wheelTrack' : 'wheel_track' }

profileAlg(algId = 'pts:vcstogis',params = params)