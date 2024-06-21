# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:33:06 2024

@author: Drew.Bennett
"""



#tuple of lower,upper for inclusive range
def intervals(start,stop,interval):
    
    if interval == 0:
        raise ValueError('interval should be non zero')
    
    if stop - start > 0 and interval > 0:
        lower = start
        upper = start + interval
        while upper < stop:
            yield (lower,upper)
            lower += interval
            upper += interval
        yield (lower,min(upper,stop))
        return
        
    else:
        raise ValueError('need start < stop and interval > 0')


if __name__ in ('__main__', '__console__'):
    for lower,upper in intervals(0,100.8,10):
        print(lower,upper)