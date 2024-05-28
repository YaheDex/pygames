import pygame
from pygame.locals import *
import math

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *



class Player:
    
    def __init__(self):

        
        self.Position = [0, 5, 0]
        self.theta = 0
        self.Direction = []
        self.Direction.append(0)
        self.Direction.append(0)
        self.Direction.append(0)
        self.newDir = [1, 5, 0]
        
        
    def rotating(self):
        dir = [1.0, 0.0, 0.0]

        newx = dir[0]*math.cos(math.radians(self.theta)) + math.sin(math.radians(self.theta))*dir[2]
        newz = dir[0]*math.sin(math.radians(self.theta)) + math.cos(math.radians(self.theta))*dir[2]
        newdir = [(newx), self.Position[1], (newz)]
        return newdir
        
    def update(self):
        print(self.newDir, self.Position, math.sqrt(self.newDir[0]**2 + self.newDir[2]**2))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.newDir = self.rotating()            
            self.Position[0] = self.Position[0] + self.newDir[0]
            self.Position[2] = self.Position[2] + self.newDir[2]
 
        if keys[pygame.K_s]:
            self.newDir = self.rotating()
            self.Position[0] = self.Position[0] - self.newDir[0]            
            self.Position[2] = self.Position[2] - self.newDir[2]

            
        if keys[pygame.K_d]:
            self.theta+=2.5
            self.newDir = self.rotating()
                
        if keys[pygame.K_a]:
            self.theta-=2.5
            self.newDir = self.rotating()
                
