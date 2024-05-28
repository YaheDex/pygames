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
        self.jump_speed = 0.4  # Velocidad del salto predeterminada
        self.gravity = 0.009  # Velocidad de la gravedad para poder lograr el descenso suave, se lo voy restando al salto
        self.on_ground = True # is jumping pero mi lógica me puso mejor a detectar el suelo equide
        self.y_velocity = 0 # en vez de restar dos valores diferentes, sí se pudo con el mismo valor al volverlo negativo
        self.prevPos = []

        
        
    def rotating(self):
        dir = [1.0, 0.0, 0.0]

        newx = dir[0]*math.cos(math.radians(self.theta)) + math.sin(math.radians(self.theta))*dir[2]
        newz = dir[0]*math.sin(math.radians(self.theta)) + math.cos(math.radians(self.theta))*dir[2]
        newdir = [(newx), self.Position[1], (newz)]
        return newdir
        
    def update(self):
        print(self.newDir, self.Position, math.sqrt(self.newDir[0]**2 + self.newDir[2]**2))
        self.prevPos = self.Position
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
            
        if keys[pygame.K_SPACE] and self.on_ground:
            # print("LOL")
            self.on_ground = False
            self.y_velocity = self.jump_speed
            
        if not self.on_ground:
            # print("DEPURASAO")

            # sumo la velocidad de salto hasta que se vuelve negativa a la misma razón de cambio, así puedo formar la parábola sin dos variables
            self.Position[1] += self.y_velocity
            print(self.Position[1])
            self.y_velocity -= self.gravity
            # print("EQUISDE") # usado para depuración
            if self.Position[1] <= 5 or self.on_ground:  # En vez de fijar una altura máxima y mínima para cuando llegue al suelo, sólo un if que en cuanto
                self.on_ground = True
                self.y_velocity = 0
                # print('DEPURASAO')
