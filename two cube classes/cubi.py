#Autor: Ivan Olmos Pineda


import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math
import numpy as np

class Cubi:
    
    def __init__(self, dim, vel):
        #vertices del cubo
        self.points = np.array([[-1.0,-1.0, 1.0], [1.0,-1.0, 1.0], [1.0,-1.0,-1.0], [-1.0,-1.0,-1.0],
                                [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0,-1.0], [-1.0, 1.0,-1.0]])
        
        self.DimBoard = dim
        #Se inicializa una posicion aleatoria en el tablero
        self.Position = [random.randint(-dim,dim), 5,random.randint(-dim,dim)]
        #...
        #Se inicializa un vector de direccion aleatorio
        self.Direction = [random.randint(1,10),0,random.randint(1,10)]
        #...
        #Se normaliza el vector de direccion
        mag = np.linalg.norm(self.Direction)
        #...
        #Se cambia la maginitud del vector direccion
        self.Direction = self.Direction / mag
        self.Direction = self.Direction*vel
        
        #...
        self.deg=0.0
        self.deg_delta = -1.0

    def update(self):
        if(self.deg > 10.0):
            deg_delta = -1.0
        elif(self.deg < -10.0):
            deg_delta = 1.0
                
        self.deg += self.deg_delta
        
        rads = math.radians(self.deg)
        dir_x = math.cos(rads)*self.Direction[0] + math.sin(rads)*self.Direction[2]
        dir_z = -math.sin(rads)*self.Direction[0] + math.cos(rads)*self.Direction[2]
        self.Direction[0] = dir_x
        self.Direction[2] = dir_z
                
        new_x = self.Position[0] + self.Direction[0]
        new_z = self.Position[2] + self.Direction[2]
        if (np.abs(new_x) >= 200):
            new_x = self.Position[0] + (self.Direction[0]*-1)
            self.Direction[0] *= -1
            self.Position = [new_x,5,new_z]
            
            
        elif (np.abs(new_z) >= 200):
            new_z = self.Position[2] + (self.Direction[2]*-1)
            self.Direction[2] *= -1
            self.Position = [new_x,5,new_z]
            
        else:
            self.Position = [new_x,5,new_z]
        
        #detecc de que el objeto no se salga del area de navegacion
        #...

    def drawFaces(self):
        glBegin(GL_QUADS)
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[3])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[7])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[4])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[5])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[3])
        glVertex3fv(self.points[7])
        glVertex3fv(self.points[6])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[3])
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[7])
        glEnd()
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(5,5,5)
        glColor3f(1.0, 0.0, 0.0)
        self.drawFaces()
        glPopMatrix()