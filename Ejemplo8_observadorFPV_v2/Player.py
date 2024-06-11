import pygame
from pygame.locals import *
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Player:
    def __init__(self):
        self.Position = [0, 5, 0]
        self.theta = 0
        self.Direction = [0, 0, 0]
        self.newDir = [1, 5, 0]
        self.jump_speed = 0.4
        self.gravity = 0.009
        self.on_ground = True
        self.y_velocity = 0
        self.prevPos = []
        self.preEyeY = 0
        self.pr = None

    def rotating(self):
        dir = [1.0, 0.0, 0.0]
        newx = dir[0] * math.cos(math.radians(self.theta)) + math.sin(math.radians(self.theta)) * dir[2]
        newz = dir[0] * math.sin(math.radians(self.theta)) + math.cos(math.radians(self.theta)) * dir[2]
        newdir = [newx, self.Position[1], newz]
        return newdir

    def update(self):
        self.prevPos = self.Position.copy()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.newDir = self.rotating()
            self.Position[0] += self.newDir[0]
            self.Position[2] += self.newDir[2]
        if keys[pygame.K_s]:
            self.newDir = self.rotating()
            self.Position[0] -= self.newDir[0]
            self.Position[2] -= self.newDir[2]
        if keys[pygame.K_d]:
            self.theta += 4
            self.newDir = self.rotating()
        if keys[pygame.K_a]:
            self.theta -= 4
            self.newDir = self.rotating()
        if keys[pygame.K_SPACE] and self.on_ground:
            self.preEyeY = self.Position[1]
            self.on_ground = False
            self.y_velocity = self.jump_speed
        if not self.on_ground:
            self.Position[1] += self.y_velocity
            self.y_velocity -= self.gravity
            if self.Position[1] <= self.preEyeY:  # En vez de fijar una altura máxima y mínima para cuando llegue al suelo, sólo un if que en cuanto
                self.Position[1] = self.preEyeY   # detecte la altura del jugador, se reestablezca todo
                # CENTER_Y = self.Position[1]
                self.on_ground = True
                self.y_velocity = 0
                # print('DEPURASAO')


    def checkCol(self, cubos):
        for obj in cubos:
        # Lógica de colisión con la plataforma
            if math.sqrt((obj.Position[0] - self.Position[0])**2 + (obj.Position[2] - self.Position[2])**2) < 10.0:
                if self.Position[1] < obj.height:  # Altura de la plataforma
                    # El personaje choca con la plataforma
                    self.Position[0] = self.prevPos[0]  # Restablece a la última posición segura
                    self.Position[2] = self.prevPos[2]
                    print('FUAaaaaaaaaaaaaaaaaaa')
                elif obj.height <= self.Position[1] <= (obj.height+5):
                    # El personaje está sobre la plataforma
                    self.pr = obj
                    self.preEyeY = obj.height + 5
                    print('FUuuuuuuuuuuuUUUUUUUUUUUUUUUUUUUUUUUU')
            elif (self.pr != None):
                if (math.sqrt((self.pr.Position[0] - self.Position[0])**2 + (self.pr.Position[2] - self.Position[2])**2) >= 10): #el personaje sale del área de colisión de la plataforma
                    print("WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                    if self.Position[1] > obj.height:  # Altura de la plataforma
                        # El personaje cae de la plataforma
                        self.on_ground = False
                        self.preEyeY = 5
                        print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
                        self.pr = None
        

                    
                    
                    
