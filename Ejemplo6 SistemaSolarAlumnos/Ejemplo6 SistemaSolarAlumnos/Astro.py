import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math
import numpy as np

class Astro:
    def __init__(self, dist, esc, color, v_ang):
        self.deg = 0.0
        self.dist = dist
        self.esc = esc
        self.color = np.copy(color)
        self.v_ang = v_ang
        self.sphere = gluNewQuadric()
        
    def update(self):
        #codigo para la actualizacion de variables de control
    
    def draw(self):
        glPushMatrix()

        gluSphere(self.sphere, 1.0, 16, 16)
        glPopMatrix()