import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math

class Pacman:
    
    def __init__(self, dim, dim2, dim3, vel):
        #Se inicializa las coordenadas de los vertices del cubo
        self.vertexCoords = [  
                   1,1,1,   1,1,-1,   1,-1,-1,   1,-1,1,
                  -1,1,1,  -1,1,-1,  -1,-1,-1,  -1,-1,1  ]
        #Se inicializa los colores de los vertices del cubo
        self.vertexColors = [ 
                   1,1,1,   1,0,0,   1,1,0,   0,1,0,
                   0,0,1,   1,0,1,   0,0,0,   0,1,1  ]
        #Se inicializa el arreglo para la indexacion de los vertices
        self.elementArray = [ 
                  0,1,2,3, 0,3,7,4, 0,4,5,1,
                  6,2,1,5, 6,5,4,7, 6,7,3,2  ]

        #Limites de movimiento del pacman
        self.Limit1 = dim
        self.Limit2 = dim2
        self.Limit3 = dim3
        #Se inicializa una posicion aleatoria en el tablero
        self.Position = []
        self.Position.append(200)
        self.Position.append(5.0)
        self.Position.append(206)
        #Se inicializa un vector de direccion aleatorio
        self.Direction = []
        self.Direction.append(0)
        self.Direction.append(5.0)
        self.Direction.append(0)
        #Se normaliza el vector de direccion
        # m = math.sqrt(self.Direction[0]*self.Direction[0] + self.Direction[2]*self.Direction[2])
        # self.Direction[0] /= m
        # self.Direction[2] /= m
        #Se cambia la maginitud del vector direccion
        self.Direction[0] *= vel
        self.Direction[2] *= vel
        

    def update(self, dir):
        if dir == "right":
            self.Direction[0] = 1
            new_x = self.Position[0] + self.Direction[0]
            if(abs(new_x) <= self.Limit2):
                self.Position[0] = new_x
            else:
                self.Direction[0] = 0
        elif dir == "left":
            self.Direction[0] = -1
            new_x = self.Position[0] + self.Direction[0]
            if((new_x) >= self.Limit1):
                self.Position[0] = new_x
            else:
                self.Direction[0] = 0
        elif dir == "up":
            self.Direction[2] = -1
            new_z = self.Position[2] + self.Direction[2]
            if((new_z) >= self.Limit1):
                self.Position[2] = new_z
            else:
                self.Direction[2] = 0
        elif dir == "down":
            self.Direction[2] = 1
            new_z = self.Position[2] + self.Direction[2]
            if(abs(new_z) <= self.Limit3):
                self.Position[2] = new_z
            else:
                self.Direction[2] = 0
        

    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(10,10,10)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertexCoords)
        glColorPointer(3, GL_FLOAT, 0, self.vertexColors)
        glDrawElements(GL_QUADS, 24, GL_UNSIGNED_INT, self.elementArray)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glPopMatrix()

    def drawFace(self, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4):
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x1, y1, z1)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x2, y2, z2)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(x3, y3, z3)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x4, y4, z4)
        glEnd()
        
    def drawCube(self, texture, id):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(7,7,7)
        glColor3f(1.0, 1.0, 1.0)
        #Activate textures
        glEnable(GL_TEXTURE_2D)
        #up face
        glBindTexture(GL_TEXTURE_2D, texture[id])
        self.drawFace(-1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()