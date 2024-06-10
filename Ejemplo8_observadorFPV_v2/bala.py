import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math
import numpy as np
sphere = gluNewQuadric()
class Bala:
    
    def __init__(self, vel, playerPos, playerDir):

        
        self.Position = [playerPos[0]+playerDir[0], playerPos[1]-2, playerPos[2]+playerDir[2]]
        
        self.Direction = [playerDir[0], 0, playerDir[2]]
        
        self.vel = vel
        
        self.vida = 150
        
        self.vive = True
        
        
    
    def drawBala(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glColor3f(255,255,0)
        glScalef(0.25,0.25,0.25)
        glRotatef(90,1,0,0)
        gluSphere(sphere, 5.0, 32, 16)
        glPopMatrix()

    def update(self):
        newPos = [0,0,0]
        for i in range(len(self.Position)):
            newPos[i] = (self.Position[i] + self.Direction[i])
        newPos[1] = self.Position[1]
        self.Position = newPos
        
        self.vida -= 1
        
        if self.vida <= 0:
            self.vive = False
        
            
    def checkCol(self, dan):
        return math.sqrt((self.Position[0] - dan.Position[0])**2 + (self.Position[2] - dan.Position[2])**2) < 10.0

            