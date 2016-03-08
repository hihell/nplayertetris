class Player:
    def __init__(self):
        
        self.block = None #block ownership
        self.nextBlock = None #next blook
        
        self.x = 0 #position of block of this player
        self.y = 0
        
        self.dropped = 0 #how many blocks has this player dropped? will be used for speed increase
        self.score = 0 #score
        self.goingDown = False
        self.goingLeft = False
        self.goingRight = False
        self.moveCounter = 0 #dont even ask
        
        self.lastDownPressed = 0 #the iteration number when the lastdown button was pressed for this player (for quick placing of pieces)
        
    #get 1 or 0 depending on whether or not this players block is solid on x,y index (x,y are 0...3). If not, return 0
    #just to hanve shorthand
    def getBit(self, x ,y):
        if x >= 0 and x < 4 and y >= 0 and y < 4:
            return self.block.block[self.block.rotation][x,y]
        else:
            return 0
    