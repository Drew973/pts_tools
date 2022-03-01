import numpy

#generator yielding start,end
#counts down for negative step
def split(length,step):
    if step>0:
        chainages = numpy.arange(0,length,step)
    else:
        chainages = numpy.arange(length,0,step)
    
    if len(chainages)>0:
        if chainages[-1] < length and step>0:
            chainages = numpy.append(chainages,length)
            
        if chainages[-1] > 0 and step<0:
            chainages = numpy.append(chainages,0)
            
        for i,v in enumerate(chainages[0:-1]):
            yield v,chainages[i+1],i
   

if __name__ == '__console__':

    for p in split(105.1,-10.0):
        print(p)
