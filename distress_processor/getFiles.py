import os

#ext is file extention like .csv
#finds all files in folder and subfolder. if ext set only returns files with extention of ext

def getFiles(folder,ext=None):
    for root, dirs, files in os.walk(folder, topdown=False):
        for f in files:
            if os.path.splitext(f)[1]==ext or ext is None:
                yield os.path.join(root,f)
