import os


from pts_tools.shared_test import test_alg
from pts_tools import split_by_chainage

#folder = os.path.dirname(split_by_chainage.__file__)


def profile():
    network  = test_alg.networkWithNodes
    params ={ 'FIELD' : '', 'INPUT' : network, 'OUTPUT' : 'TEMPORARY_OUTPUT', 'STEP' : 100 }
    test_alg.testAlg('PTS tools:split_by_chainage',params)



if __name__ == '__console__':
    profile()