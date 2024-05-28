import pygame
from pygame.locals import *
import math

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Player:
    
    def __init__(self):

        
        self.Position = [0, 0, 0]
        
        self.Direction = []
        self.Direction.append(0)
        self.Direction.append(0)
        self.Direction.append(0)
        
        
    def rotating(self, theta):
        dir = [1.0, 0.0, 0.0]

        newx = dir[0]*math.cos(math.radians(theta)) + math.sin(math.radians(theta))*dir[2]
        newz = dir[0]*math.sin(math.radians(theta)) + math.cos(math.radians(theta))*dir[2]
        newdir = [(newx), self.Position[1], (newz)]
        return newdir
        
    def update(self, dir):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
                self.Position = self.rotating(theta)
 
        if keys[pygame.K_DOWN]:
                self.Position = self.rotating(theta)
                
        if keys[pygame.K_RIGHT]:
                theta+=2.5
                self.Position = self.rotating(theta)
                
        if keys[pygame.K_LEFT]:
                theta-=2.5
                self.Position = self.rotating(theta)
                
