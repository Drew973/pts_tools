import numpy as np

#clusters bool array where true
#returns list of turples.
#turples indexes of start and end of cluster
def clumpArray(vals):
    ranges = []

    s = None

    for i, v in enumerate(vals):
        
        if v:
            if s is None:
                s = i
                
        else:
            if not s is None:
                ranges.append((s,i-1))
                s = None
            
    if not s is None:
        ranges.append((s,i))

    return ranges

if __name__ =='__console__' or __name__ =='__main__':
    chainages = np.arange(0,21.0,1)
    radi = np.random.rand(len(chainages))
    threshold = 0.5

    print(chainages)
    vals = radi>threshold#bool array
    print(vals)

    print(clumpArray(vals))







