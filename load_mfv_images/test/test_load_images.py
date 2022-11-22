from pts_tools.shared_test.test_alg import testAlg



if __name__=='__console__':
    params = { 'inputFolder' : 'C:\\Users\\drew.bennett\\Documents\\mfv_images\\LEEMING DREW\\TIF Images\\MFV2_01',
    'step' : 10 }

    #processing.runAndLoadResults('PTS tools:load_mfv_images',params)
    f = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\pts_tools\load_mfv_images\test\load_images_profile.txt'
    testAlg('PTS tools:load_mfv_images',params,f)