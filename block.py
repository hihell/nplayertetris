from numpy import array
from random import randrange

#colors of block.s the 0th color is the empty color
colourDict = {0:(0,0,0), 1:(0,255,0),2:(255,0,0),3:(0,100,0),4:(255,255,0),5:(0,0,255),6:(255,255,255),7:(255,0,255)}
class Block:
    def __init__(self, block=None, colour=None):
        rightL =[array([[0,0,0,0],
                [0,1,0,0],
                [0,1,0,0],
                [0,1,1,0]]),
        
            array( [[0,0,0,0],
                [0,0,0,0],
                [1,1,1,0],
                [1,0,0,0]]),
        
            array( [[0,0,0,0],
                [1,1,0,0],
                [0,1,0,0],
                [0,1,0,0]]),
        
            array( [[0,0,0,0],
                [0,0,1,0],
                [1,1,1,0],
                [0,0,0,0]])]
        
        leftL = [array([[0,0,0,0],
                [0,1,0,0],
                [0,1,0,0],
                [1,1,0,0]]),
        
            array( [[0,0,0,0],
                [1,0,0,0],
                [1,1,1,0],
                [0,0,0,0]]),
        
            array( [[0,0,0,0],
                [0,1,1,0],
                [0,1,0,0],
                [0,1,0,0]]),
        
            array( [[0,0,0,0],
                [0,0,0,0],
                [1,1,1,0],
                [0,0,1,0]])]
        
        
        square =[array([[0,0,0,0],
                [0,1,1,0],
                [0,1,1,0],
                [0,0,0,0]])]
        
        line = [array( [[0,1,0,0],
                [0,1,0,0],
                [0,1,0,0],
                [0,1,0,0]]),
        
            array( [[0,0,0,0],
                [1,1,1,1],
                [0,0,0,0],
                [0,0,0,0]])]
        
        
        t = [array(    [[0,0,0,0],
                [0,1,0,0],
                [1,1,0,0],
                [0,1,0,0]]),
        
            array( [[0,0,0,0],
                [0,0,0,0],
                [1,1,1,0],
                [0,1,0,0]]),
        
            array( [[0,0,0,0],
                [0,1,0,0],
                [0,1,1,0],
                [0,1,0,0]]),
        
            array( [[0,0,0,0],
                [0,1,0,0],
                [1,1,1,0],
                [0,0,0,0]])]
        
        
        leftZ= [array( [[0,0,0,0],
                [0,1,0,0],
                [1,1,0,0],
                [1,0,0,0]]),
        
            array( [[0,0,0,0],
                [0,0,0,0],
                [1,1,0,0],
                [0,1,1,0]]),
        
            array( [[0,0,0,0],
                [0,0,1,0],
                [0,1,1,0],
                [0,1,0,0]]),
    
            array( [[0,0,0,0],
                [1,1,0,0],
                [0,1,1,0],
                [0,0,0,0]])]
        
        rightZ= [array([[0,0,0,0],
                [1,0,0,0],
                [1,1,0,0],
                [0,1,0,0]]),
        
            array( [[0,0,0,0],
                [0,0,0,0],
                [0,1,1,0],
                [1,1,0,0]]),
        
            array( [[0,0,0,0],
                [0,1,0,0],
                [0,1,1,0],
                [0,0,1,0]]),
        
            array( [[0,0,0,0],
                [0,1,1,0],
                [1,1,0,0],
                [0,0,0,0]])]
        
        self.numblock = randrange(7) + 1
        if block: self.block = block
        else: self.block = {1:rightL,2:leftL,3:square,4:line,5:t,6:leftZ,7:rightZ}[self.numblock]
        
        if colour:
            self.colour = colour
        else:
            self.colour = colourDict[self.numblock]
            self.rotNeed = {1:4,2:4,3:1,4:2,5:4,6:2,7:2}[self.numblock]
            
        self.rotation = 0#randrange(len(self.block))
        
    def getCurrentGrid(self):
        return self.block[self.dir]

    def rotate(self,dir):
        self.rotation = (self.rotation + dir)%len(self.block)
