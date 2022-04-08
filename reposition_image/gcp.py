class gcp:
    def __init__(self,pixel,line,x,y):
        self.imageX = pixel
        self.imageY = line
        self.mapX = x
        self.mapY = y


    def command(self):
        return '-gcp {imageX} {imageY} {x} {y}'.format(imageX=self.imageX,imageY=self.imageY,x=self.mapX,y=self.mapY)

    
    def __repr__(self):
        return 'gcp({imageX},{imageY},{x},{y})'.format(imageX=self.imageX,imageY=self.imageY,x=self.mapX,y=self.mapY)
