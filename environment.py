#Space Discover: Genetic Algorithms - Environment File 

import numpy as np
import pygame as pg

class Planet():
    
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

class Environment():
    
    def __init__(self):
        
        self.width = 800
        self.height = 800
        self.planetRadius = 10
        
        self.planets = list()
        
        self.connections = list()
        
        self.screen = pg.display.set_mode((self.width, self.height))
        
        self.origSpriteRocket = pg.image.load(r'data\rocket.png')
        self.spriteRocket = self.origSpriteRocket
        self.rocketWidth = self.spriteRocket.get_rect().size[0]
        self.rocketHeight = self.spriteRocket.get_rect().size[1]
        self.rotation = 0
        
        self.spriteBackground = pg.image.load(r'data\space.jpg')
        self.spriteBackground = pg.transform.smoothscale(self.spriteBackground, (self.width, self.height))
        
        
        self.rocketSpeed = 10
        self.rocketPos = [-50] * 2
        
        self.currentPos = 0
        
        self.drawScreen('none')
        
        self.edit()
        
    def drawScreen(self, view):
        self.screen.fill((0, 0, 0))
        
        self.screen.blit(self.spriteBackground, (0,0))
        
        if view == 'normal':
            for i in range(0, len(self.connections)):
                pg.draw.line(self.screen, (255, 255, 0), self.connections[i][0], self.connections[i][1], 3)
        elif view == 'beautiful':
            for i in range(0, len(self.connections) - 1):
                pg.draw.line(self.screen, (255, 255, 0), self.connections[i][0], self.connections[i][1], 3)
        
        if len(self.planets) > 0 and self.rocketPos[0] > 0 and view == 'beautiful':
           pg.draw.line(self.screen, (255, 255, 0), (self.planets[self.currentPos].pos[0], self.planets[self.currentPos].pos[1]), (self.rocketPos[0], self.rocketPos[1]), 3)
        
        
        for planet in self.planets:
            pg.draw.circle(self.screen, planet.color, planet.pos, self.planetRadius)
    
        self.screen.blit(self.spriteRocket, (self.rocketPos[0] - self.rocketWidth/2, self.rocketPos[1] - self.rocketHeight/2))
        
        pg.display.flip()
        
        
    def edit(self):
        while True:
            position = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
                    planet = Planet(position, color)
                    self.planets.append(planet)
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        return
                    
            self.drawScreen('none')
    
    def rotateCenter(self, sprite, angle):
    
        spriteRect = sprite.get_rect()
        
        rotSprite = pg.transform.rotate(sprite, angle)
        
        spriteRect.center = rotSprite.get_rect().center
        
        rotSprite = rotSprite.subsurface(spriteRect)
        
        return rotSprite
    
    def step(self, action, view):
        
        p1X = self.planets[self.currentPos].pos[0]
        p1Y = self.planets[self.currentPos].pos[1]
        
        p2X = self.planets[action].pos[0]
        p2Y = self.planets[action].pos[1]
        
        distance = pow(pow(p1X - p2X, 2) + pow(p1Y - p2Y, 2), 0.5)
        
        if view == 'normal' or view == 'beautiful':
            self.connections.append([(p1X, p1Y), (p2X, p2Y)])
            self.drawScreen(view)
            
            
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
        
        
        if view == 'beautiful':
            reached = False
            self.rocketPos[0] = p1X
            self.rocketPos[1] = p1Y
            diffX = p1X - p2X
            diffY = p1Y - p2Y
            t = diffY/(diffX + 1e-12)
            x = pow(pow(self.rocketSpeed, 2) / (pow(t, 2) + 1), 0.5)
            y = x * abs(t) 
            if diffY > 0:
                y = -y
            if diffX > 0:
                x = -x
            
            if (x <= 0 and y <= 0) or (x <= 0 and y >= 0):
                angle = np.rad2deg(np.arctan(-t) + np.pi/2)
            else:
                angle = np.rad2deg(np.arctan(-t) - np.pi/2)
            
            if diffX == 0:
                angle += 180
                
            
            self.spriteRocket = self.origSpriteRocket
            self.spriteRocket = self.rotateCenter(self.spriteRocket, angle)
            
            
            while not reached:
                self.rocketPos[0] += x
                self.rocketPos[1] += y
                distance = pow(pow(self.rocketPos[0] - p2X, 2) + pow(self.rocketPos[1] - p2Y, 2), 0.5)
                if distance < self.planetRadius or (diffX == 0 and diffY == 0):
                    self.rocketPos[0] = p2X
                    self.rocketPos[1] = p2Y
                    reached = True
                pg.time.wait(50)
                self.drawScreen(view)
        
        self.currentPos = action
        
        return distance
    
    def reset(self):
        
        self.connections.clear()
        self.currentPos = 0
        self.rocketPos = [-50] * 2
        
        
if __name__ == '__main__': 
    env = Environment()   