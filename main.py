#N-player CO-OP TETRIS!

import pygame
from pygamehelper import *
from player import *
from block import *
from controls import *
import sys
from particles import *
#import psyco
#psyco.full()

class NTetris(PygameHelper):
    def __init__(self, numPlayers):
        
        self.numPlayers = numPlayers
        self.players = [Player() for i in range(numPlayers)]
        
        self.score = 0 #score
        
        self.cellsX = numPlayers*7
        self.cellsY = 28
        self.cellSize = 20 #in pixels
        
        self.marginX = 20 #margin for the ddrawing area
        self.marginY = 120 #margin for the ddrawing area
        
        self.w = self.marginX * 2 + self.cellsX * self.cellSize + 150
        self.h = self.marginY * 2 + self.cellsY * self.cellSize
        
        PygameHelper.__init__(self, size=(self.w, self.h), fill=((40,40,40)))
        
        pygame.mixer.music.load('tetris_Mozart.mid')
        pygame.mixer.music.play(-1)
        
        self.scores=None
        self.particleEngine = Particles()
        
        self.reInitGame() #start the game
        
    def reInitGame(self):
        self.screen.fill((40,40,40))
        self.score = 0
        #reinit the map
        self.grid = [[0 for i in range(self.cellsY)] for j in range(self.cellsX)] #indexed as grid[x,y], 0,0 is top left
        
        #reset every player
        for p in self.players:
            self.newBlock(p)
            p.dropped = 0
            p.moveCounter = 0
            p.score = 0
            p.goingDown = False
            p.goingLeft = False
            p.goingRight = False
            
        #load high scores
        self.scores = [int(x) for x in open("scores.txt", 'r').readlines() if x]
        self.drawScore()
            
    def redrawNextBlocks(self):
        for ind, p in enumerate(self.players):
            for i in range(4):
                for j in range(4):
                    if not p.nextBlock == None:
                        
                        if p.nextBlock.block[p.nextBlock.rotation][i,j] == 1:
                            pygame.draw.rect(self.screen, p.nextBlock.colour, pygame.Rect(ind*4*self.cellSize + i*self.cellSize+self.marginX+10,j*self.cellSize+10, self.cellSize, self.cellSize).inflate(-3,-3))
                        else:
                            pygame.draw.rect(self.screen, (40,40,40), pygame.Rect(ind*4*self.cellSize + i*self.cellSize+self.marginX+10,j*self.cellSize+10, self.cellSize, self.cellSize).inflate(-3,-3))
        
    def newBlock(self, p):
        if not p.nextBlock: p.nextBlock = Block()
        
        p.block = p.nextBlock
        p.nextBlock = Block()
        
        #redraw the next block
#        self.redrawNextBlocks()
        
        i = self.players.index(p)
        cw = (self.cellsX/self.numPlayers)
        p.x = randrange(cw*i, cw*i + cw - 5)
        p.y = -2
        
        p.goingDown = False
        
        if self.collideStatic(p, 0, 0):
            #fail
            fontObj = pygame.font.SysFont('arial', 80)
            fontSurf = fontObj.render("YOU FAIL!", True, (255,0,0)) #make players feel bad
            
            self.saveScores()
            
            self.screen.blit(fontSurf, (self.w/4, self.h/3))
            pygame.display.flip()
            
            okd = False
            while not okd:
                for e in pygame.event.get():
                    if e.type == KEYUP and (e.key == K_RETURN or e.key == K_ESCAPE):
                        okd = True
                
            self.reInitGame()
           
    def saveScores(self):
     #save new high scores
        if self.score > self.scores[self.numPlayers]: 
            self.scores[self.numPlayers] = self.score
            f = open("scores.txt", "w")
            for s in self.scores:
                f.write(`s` + "\n")
            f.close()
            
    def update(self):
                   
        #update particle system
        self.particleEngine.tick()
        
        #do all collisions with static objects and also dropping. And movement
        tmp = list(self.players)
        tmp.sort(lambda x, y: x.y > y.y)
        for p in tmp:
            #0->10
            #20->9
            if (self.counter % max(1,(10 - int((p.dropped%40)/8))) == 0 or p.goingDown):
                self.triesDown(p)
            
            if p.goingLeft:
                if p.moveCounter > 10:
                    self.triesLeft(p)
                p.moveCounter += 1
                
            if p.goingRight:
                if p.moveCounter > 10:
                    self.triesRight(p)
                p.moveCounter += 1
        
        #make lines dissapear (if any)
        yline = self.cellsY - 1
        while yline >= 0:
            isline = 0
            for x in range(self.cellsX):   
                if self.grid[x][yline] == 0:
                    isline += 1
            
            if isline <= 1:
                pygame.mixer.Sound('bomb2.wav').play()
        
                #wee! shift all shit down one
                self.score += 1
#                self.drawScore()
                
                for yy in range(yline, 1, -1):
                    for xx in range(self.cellsX):
                        self.grid[xx][yy] = self.grid[xx][yy-1]
                
                yy = yline - 1
                for xx in range(self.cellsX):
                    self.particleEngine.addEffect(xx*self.cellSize+self.marginX, (yy+1)*self.cellSize+self.marginY, colourDict[self.grid[xx][yy]], self.cellSize, rand = False, STEP = 4)
            
            else:
                yline -= 1 #next line up
                
    def drawScore(self):
        #draw score
        fontObj = pygame.font.SysFont('arial', 20)
        pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(self.w-150,0,150,self.h))
        fontSurf = fontObj.render("SCORE: %i" % self.score, True, (255,255,255))
        self.screen.blit(fontSurf, (self.w - 140, self.h/2))
        
        #draw player score (dropped blocks)
        fontObj = pygame.font.SysFont('arial', 15)
        for i in range(self.numPlayers):
            fontSurf = fontObj.render("PLAYER %i: %i %i" % (i, int(self.players[i].score*100)/(self.players[i].dropped+1), self.players[i].dropped), True, (255,255,255))
            self.screen.blit(fontSurf, (self.w - 140, self.h/2 + 25*(i+2)))
        
        #draw top score for this number of players
        fontSurf = fontObj.render("HIGHEST SCORE: %i" % self.scores[self.numPlayers], True, (255,255,255))
        self.screen.blit(fontSurf, (self.w - 140, self.h/2 + 25*(i+2) + 100))
        
                    
    def keyUp(self, key):
        for i, rule in enumerate(playerControls[self.numPlayers-1]):
            #LEFT, RIGHT, ROTATE, DOWN
            if key == rule[0]: 
                self.players[i].goingLeft = False
                self.players[i].moveCounter = 0
            if key == rule[1]: 
                self.players[i].goingRight = False
                self.players[i].moveCounter = 0
            if key == rule[2]: self.triesRotate(self.players[i])
            if key == rule[3]: 
                self.players[i].goingDown = False
                
                if self.counter - self.players[i].lastDownPressed < 7:
                    #super drop this playersd
                    self.superDrop(self.players[i])
                    
                self.players[i].lastDownPressed = self.counter
                
    
        if key == K_r: self.reInitGame()
        if key == K_p:
            #pause
            okd = False
            while not okd:
                for e in pygame.event.get():
                    if e.type == KEYUP and e.key == K_p:
                        okd = True
            
        if key == K_MINUS:
            self.numPlayers -= 1
            self.__init__(self.numPlayers)
            self.running = True
            
        if key == K_EQUALS:
            self.numPlayers += 1
            self.__init__(self.numPlayers)
            self.running = True
            
                        
    def keyDown(self, key):
        for i, rule in enumerate(playerControls[self.numPlayers-1]):
            if key == rule[3]: self.players[i].goingDown = True
            if key == rule[0]: 
                self.players[i].goingLeft = True
                self.triesLeft(self.players[i])
            if key == rule[1]: 
                self.players[i].goingRight = True
                self.triesRight(self.players[i])
                
    #player is trying to go left
    def triesLeft(self, player):
        if not self.collideStatic(player, -1, 0):
            player.x -= 1
            if self.collidesOthers(player):
                player.x += 1 #correct his position. he collided with other player
        
    def triesRight(self, player):
        if not self.collideStatic(player, 1, 0):
            player.x += 1
            if self.collidesOthers(player):
                player.x -= 1
    
    def triesRotate(self, player):
        player.block.rotate(1)
        if self.collidesOthers(player) or self.collideStatic(player, 0, 0):
            player.block.rotate(-1)
    
    #returns true if player overlaps with some other player
    def collidesOthers(self, player):
        
        for p in self.players:
            if p != player:
                #collide player against p
                collides = False
                for i in range(4):
                    for j in range(4):
                        if p.getBit(i,j) == 1 and player.getBit(p.x - player.x + i, p.y - player.y + j) == 1:
                            collides = True
                if collides: return True
                
        return False
    
    
    #p's block just crashed. Get its score and play nice sound
    #in addition increase p's score based on percentage of contacts he/she made
    def blockScore(self, p):
        t=0
        y=0
        for i in range(-1, 5):
            for j in range(-1, 5):
                if p.getBit(i,j) == 0 and (p.getBit(i-1,j) or p.getBit(i+1, j) or p.getBit(i, j-1) or p.getBit(i, j+1)):
                    #this offset is a contact position of our block
                    t+=1
                    #now, is this position in the grid covered by something?
                    tx = p.x + i
                    ty = p.y + j
                    if tx<0 or tx>=self.cellsX or ty<0 or ty>=self.cellsY or self.grid[tx][ty] != 0 :
                        y+=1
                        
        p.score += 1.0*y/t
        
    def triesDown(self, player, superDrop = False):
        
        if self.collideGround(player) or self.collideStatic(player, 0, 1):
            p=player
            self.blockScore(p) #get score of this drop, and play a sound or something, for funzies
            p.dropped += 1
            pygame.mixer.Sound('thump.wav').play()
            for i in range(4):
                    for j in range(4):
                        if p.block.block[p.block.rotation][i,j] == 1:
                            self.grid[p.x+i][p.y+j] = p.block.numblock
            
            #reset block for this player
            p.lastDownPressed = self.counter - 100
            self.newBlock(p)
            return False
        else:
            player.y += 1
            if self.collidesOthers(player):
                player.y -= 1
                return False
            return True
    
    def superDrop(self, p):
        #drop player p all the way down as far as possible
        while self.triesDown(p, True):
            pass
        
    #returns true if player p has blocks on offsetX, offestY
    def collideStatic(self, player, offsetX, offsetY):
        for i in range(4):
            for j in range(4):
                if player.block.block[player.block.rotation][i,j] == 1:
                    #test contact with other blocks
                    tx = player.x + i + offsetX
                    ty = player.y + j + offsetY
                    
                    if tx < self.cellsX and tx >= 0 and ty < self.cellsY and ty >= 0:
                        if self.grid[tx][ty] != 0:
                            return True
                        
                    if tx < 0 or tx >= self.cellsX: #collision on sides
                        return True
        return False
    
    #returns true if player p has ground under his block
    def collideGround(self, player):
        for i in range(4):
            for j in range(4):
                if player.block.block[player.block.rotation][i,j] == 1:
                    if player.y + j == self.cellsY - 1:
                        return True
        return False    
        
    def draw(self):
        
        pygame.draw.rect(self.screen, (40,40,40), pygame.Rect(0, 0, self.w - 150, self.h))
        self.redrawNextBlocks()
        self.drawScore()
        
        #draw static blocks
        for x in range(self.cellsX):
            for y in range(self.cellsY):
                pygame.draw.rect(self.screen, colourDict[self.grid[x][y]], pygame.Rect(x*self.cellSize+self.marginX,y*self.cellSize+self.marginY, self.cellSize, self.cellSize).inflate(-3,-3))
                
        #draw active block
        for p in self.players:
            for i in range(4):
                for j in range(4):
                    if not p.block == None:
                        if p.block.block[p.block.rotation][i,j] == 1 and p.y+j>=0:
                            pygame.draw.rect(self.screen, p.block.colour, pygame.Rect((p.x+i)*self.cellSize+self.marginX,(p.y+j)*self.cellSize+self.marginY, self.cellSize, self.cellSize).inflate(-3,-3))
        
        #draw particles, if applicable
        self.particleEngine.draw(self.screen)
        
        pygame.display.flip()
        
if __name__ == "__main__":
    print 'controls:'
    print 'r: reset'
    print 'p: pause'
    print '-: decrease number of players'
    print '=: increase number of players'
    
    num = 3
    if len(sys.argv) > 1:
        num = int(sys.argv[1])
    n = NTetris(num)
    n.mainLoop(40)
