import pygame
from pygame.locals import *

class PygameHelper:
    def __init__(self, size=(640,480), fill=(255,255,255)):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(fill)
        pygame.display.flip()
        self.running = False
        self.clock = pygame.time.Clock() #to track FPS
        self.counter = 0 #program counter, for funzies
        
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                self.keyDown(event.key)
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.running = False
                self.keyUp(event.key)
            elif event.type == MOUSEBUTTONUP:
                self.mouseUp(event.pos)
            
    #enter the main loop, possibly setting max FPS
    def mainLoop(self, fps=0):
        self.running = True
        
        while self.running:
            self.counter += 1
            if self.counter == 100000: self.counter = 0 #down want overflows
            
            pygame.display.set_caption("FPS: %i" % self.clock.get_fps())
            self.handleEvents()
            self.update()
            self.draw()
            self.clock.tick(fps)
            
    def update(self):
        pass
        
    def draw(self):
        pass
        
    def keyDown(self, key):
        pass
        
    def keyUp(self, key):
        pass
    
    def mouseUp(self, pos):
        pass
        