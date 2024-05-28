import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math
import numpy as np

class Cubo:
    
    def __init__(self, dim, vel, x, y, z):
        #Se inicializa las coordenadas de los vertices del cubo
        self.points = np.array([[-1.0,-1.0, 1.0], [1.0,-1.0, 1.0], [1.0,-1.0,-1.0], [-1.0,-1.0,-1.0],
                                [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0,-1.0], [-1.0, 1.0,-1.0]])

        self.DimBoard = dim
        #Se inicializa una posicion aleatoria en el tablero
        self.Position = [x, y, z]
        self.Direction = []
        self.Direction.append(random.random())
        self.Direction.append(5.0)
        self.Direction.append(random.random())
        #Se normaliza el vector de direccion
        m = math.sqrt(self.Direction[0]*self.Direction[0] + self.Direction[2]*self.Direction[2])
        self.Direction[0] /= m
        self.Direction[2] /= m
        #Se cambia la maginitud del vector direccion
        self.Direction[0] *= vel
        self.Direction[2] *= vel
        

    def update(self):
        new_x = self.Position[0] + self.Direction[0]
        new_z = self.Position[2] + self.Direction[2]
        
        if(abs(new_x) <= self.DimBoard):
            self.Position[0] = new_x
        else:
            self.Direction[0] *= -1.0
            self.Position[0] += self.Direction[0]
        
        if(abs(new_z) <= self.DimBoard):
            self.Position[2] = new_z
        else:
            self.Direction[2] *= -1.0
            self.Position[2] += self.Direction[2]

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
        glScaled(5,5,5)
        glColor3f(1.0, 1.0, 1.0)
        #Activate textures
        glEnable(GL_TEXTURE_2D)
        #up face
        glBindTexture(GL_TEXTURE_2D, texture[id])
        self.drawFace(-1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0)
        #front face
        glBindTexture(GL_TEXTURE_2D, texture[id])
        self.drawFace(-1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0)
        #right face
        glBindTexture(GL_TEXTURE_2D, texture[id])
        self.drawFace(1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0)
        #back face
        glBindTexture(GL_TEXTURE_2D, texture[id])
        self.drawFace(1.0, 1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0)
        #left face
        glBindTexture(GL_TEXTURE_2D, texture[id])
        self.drawFace(-1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

    def chase_player(self, player_pos, speed):
        # Calculate direction vector from cube to player
        dx = player_pos[0] - self.Position[0]
        dy = player_pos[1] - self.Position[1]
        dz = player_pos[2] - self.Position[2]

        # Normalize the direction vector
        distance = math.sqrt(dx**2 + dy**2 + dz**2)
        if distance > 0:
            dx /= distance
            dy /= distance
            dz /= distance

        # Move the cube towards the player
        self.Position[0] += dx * speed
        self.Position[1] += dy * speed
        self.Position[2] += dz * speed

    def check_collision(self, player_pos):
        # Verifica si el jugador está suficientemente cerca del cubo para considerarlo una colisión
        return math.sqrt((self.Position[0] - player_pos[0])**2 + (self.Position[2] - player_pos[2])**2) < 10.0  # Ajusta el 5.0 según el tamaño de tu cubo y jugador